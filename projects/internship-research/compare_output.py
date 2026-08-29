from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
from typing import Any

from models import CandidateProfile, DecisionCard
from validate_fixture import build_expected_card


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(card: DecisionCard) -> str:
    return json.dumps(
        card.model_dump(mode="json"),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare an actual decision card "
            "with a fixture oracle."
        )
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--expected",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--actual",
        type=Path,
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    candidate = CandidateProfile.model_validate(
        load_json(args.candidate)
    )
    expected_data = load_json(args.expected)
    expected_card = build_expected_card(
        candidate,
        expected_data,
    )

    actual_card = DecisionCard.model_validate(
        load_json(args.actual)
    )

    expected_text = canonical_json(expected_card)
    actual_text = canonical_json(actual_card)

    if actual_text != expected_text:
        print("MISMATCH")

        diff = difflib.unified_diff(
            expected_text.splitlines(),
            actual_text.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )

        for line in diff:
            print(line)

        raise SystemExit(1)

    print(
        f"MATCH fixture={expected_data['fixture_id']} "
        f"candidate={actual_card.candidate_id} "
        f"verdict={actual_card.verdict.status}"
    )


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError) as error:
        print(f"COMPARISON_FAILED: {error}")
        raise SystemExit(1)