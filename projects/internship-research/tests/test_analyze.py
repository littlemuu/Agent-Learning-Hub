from __future__ import annotations

import subprocess
import sys

import json
from pathlib import Path
from typing import Any

import pytest

from analyze import (
    assess_candidate,
    build_decision_card,
    extract_job,
)
from models import CandidateProfile
from validate_fixture import (
    build_expected_card,
    validate_fixture,
)


PROJECT_DIR = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_DIR / "fixtures" / "jd_001"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_actual_card():
    job_text = (
        FIXTURE_DIR / "job.txt"
    ).read_text(encoding="utf-8")

    candidate = CandidateProfile.model_validate(
        load_json(FIXTURE_DIR / "candidate.json")
    )
    extracted = extract_job(
        job_text,
        source_path="job.txt",
    )
    assessment = assess_candidate(
        candidate,
        extracted,
    )
    card = build_decision_card(
        candidate,
        extracted,
        assessment,
        source_path="job.txt",
    )

    return candidate, card


def test_actual_card_matches_oracle() -> None:
    candidate, actual_card = build_actual_card()

    expected_card = build_expected_card(
        candidate,
        load_json(FIXTURE_DIR / "expected.json"),
    )

    assert (
        actual_card.model_dump(mode="json")
        == expected_card.model_dump(mode="json")
    )


def test_missing_evidence_quote_is_rejected() -> None:
    job_text = (
        FIXTURE_DIR / "job.txt"
    ).read_text(encoding="utf-8")

    broken_job_text = job_text.replace(
        "实习周期：至少 4 个月。",
        "实习周期暂未说明。",
    )

    with pytest.raises(
        ValueError,
        match="ev_duration quote was not found",
    ):
        extract_job(
            broken_job_text,
            source_path="job.txt",
        )


def test_short_duration_is_not_suitable() -> None:
    candidate_data = load_json(
        FIXTURE_DIR / "candidate.json"
    )
    candidate_data["availability"][
        "duration_months"
    ] = 3

    candidate = CandidateProfile.model_validate(
        candidate_data
    )
    job_text = (
        FIXTURE_DIR / "job.txt"
    ).read_text(encoding="utf-8")
    extracted = extract_job(
        job_text,
        source_path="job.txt",
    )
    assessment = assess_candidate(
        candidate,
        extracted,
    )

    constraints = {
        item.name: item.status
        for item in assessment.constraints
    }

    assert constraints["duration"] == "not_met"
    assert assessment.verdict.status == "not_suitable"


def test_candidate_strict_type_is_enforced() -> None:
    candidate_data = load_json(
        FIXTURE_DIR / "candidate.json"
    )
    candidate_data["availability"][
        "days_per_week"
    ] = "4"

    with pytest.raises(
        ValueError,
        match="days_per_week",
    ):
        CandidateProfile.model_validate(
            candidate_data
        )


def test_unknown_evidence_ref_is_rejected(
    tmp_path: Path,
) -> None:
    expected_data = load_json(
        FIXTURE_DIR / "expected.json"
    )
    expected_data["expected_job_snapshot"][
        "company"
    ]["evidence_refs"] = ["ev_missing"]

    (tmp_path / "job.txt").write_text(
        (FIXTURE_DIR / "job.txt").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    (tmp_path / "candidate.json").write_text(
        json.dumps(
            load_json(FIXTURE_DIR / "candidate.json"),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (tmp_path / "expected.json").write_text(
        json.dumps(
            expected_data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="unknown evidence_refs: ev_missing",
    ):
        validate_fixture(tmp_path)

def test_cli_and_comparator_end_to_end(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "decision_card.json"

    analyze_result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_DIR / "analyze.py"),
            "--job",
            str(FIXTURE_DIR / "job.txt"),
            "--candidate",
            str(FIXTURE_DIR / "candidate.json"),
            "--output",
            str(output_path),
        ],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    assert analyze_result.returncode == 0, (
        analyze_result.stdout
        + analyze_result.stderr
    )
    assert output_path.is_file()

    compare_command = [
        sys.executable,
        str(PROJECT_DIR / "compare_output.py"),
        "--candidate",
        str(FIXTURE_DIR / "candidate.json"),
        "--expected",
        str(FIXTURE_DIR / "expected.json"),
        "--actual",
        str(output_path),
    ]

    matching_result = subprocess.run(
        compare_command,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    assert matching_result.returncode == 0, (
        matching_result.stdout
        + matching_result.stderr
    )
    assert "MATCH" in matching_result.stdout

    broken_card = load_json(output_path)
    broken_card["verdict"]["status"] = "worth_applying"
    output_path.write_text(
        json.dumps(
            broken_card,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    mismatching_result = subprocess.run(
        compare_command,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    assert mismatching_result.returncode == 1
    assert "MISMATCH" in mismatching_result.stdout