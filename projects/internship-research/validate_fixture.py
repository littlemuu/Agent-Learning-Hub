from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import CandidateProfile, DecisionCard


FIXTURE_DIR = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "jd_001"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_evidence_refs(value: Any) -> list[str]:
    refs: list[str] = []

    if isinstance(value, dict):
        for key, child in value.items():
            if key == "evidence_refs":
                if not isinstance(child, list) or not all(
                    isinstance(ref, str) for ref in child
                ):
                    raise ValueError(
                        "evidence_refs must be a list of strings"
                    )

                refs.extend(child)
            else:
                refs.extend(collect_evidence_refs(child))

    elif isinstance(value, list):
        for child in value:
            refs.extend(collect_evidence_refs(child))

    return refs


def build_expected_card(
    candidate: CandidateProfile,
    expected: dict[str, Any],
) -> DecisionCard:
    return DecisionCard.model_validate(
        {
            "candidate_id": candidate.candidate_id,
            "source_path": "job.txt",
            "evidence": expected["evidence"],
            "job_snapshot": expected["expected_job_snapshot"],
            "unknown_fields": expected[
                "expected_unknown_fields"
            ],
            "constraints": expected["expected_constraints"],
            "dimensions": expected["expected_dimensions"],
            "verdict": expected["expected_verdict"],
        }
    )


def validate_fixture(fixture_dir: Path) -> None:
    job_text = (
        fixture_dir / "job.txt"
    ).read_text(encoding="utf-8")

    candidate = CandidateProfile.model_validate(
        load_json(fixture_dir / "candidate.json")
    )
    expected = load_json(fixture_dir / "expected.json")
    expected_card = build_expected_card(candidate, expected)

    evidence_ids: list[str] = []

    for item in expected_card.evidence:
        evidence_id = item.evidence_id
        source_path = item.source_path
        quote = item.quote

        if evidence_id in evidence_ids:
            raise ValueError(
                f"duplicate evidence_id: {evidence_id}"
            )

        if source_path != expected_card.source_path:
            raise ValueError(
                f"{evidence_id} uses unsupported source: "
                f"{source_path}"
            )

        if quote not in job_text:
            raise ValueError(
                f"{evidence_id} quote was not found in job.txt"
            )

        evidence_ids.append(evidence_id)

    evidence_refs = collect_evidence_refs(
        expected_card.model_dump(mode="python")
    )
    missing_refs = sorted(
        set(evidence_refs) - set(evidence_ids)
    )

    if missing_refs:
        raise ValueError(
            f"unknown evidence_refs: {', '.join(missing_refs)}"
        )

    print(
        f"VALID fixture={expected['fixture_id']} "
        f"candidate={expected_card.candidate_id} "
        f"job={expected_card.job_snapshot.company.value}/"
        f"{expected_card.job_snapshot.role.value} "
        f"evidence={len(evidence_ids)} "
        f"refs={len(evidence_refs)} "
        f"constraints={len(expected_card.constraints)} "
        f"dimensions={len(expected_card.dimensions)} "
        f"verdict={expected_card.verdict.status}"
    )


if __name__ == "__main__":
    try:
        validate_fixture(FIXTURE_DIR)
    except (KeyError, TypeError, ValueError) as error:
        print(f"INVALID: {error}")
        raise SystemExit(1)