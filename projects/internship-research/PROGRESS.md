# Internship Research Agent — Progress

Last updated: 2026-08-27

## Status

- Offline phase one is complete on commit [30529d6](https://github.com/littlemuu/Agent-Learning-Hub/commit/30529d663d033486e689065a909b55918326efc2).
- Strict Pydantic contracts now cover CandidateProfile, Evidence, JobSnapshot, constraint and dimension assessments, Verdict and DecisionCard.
- The anonymized `jd_001` fixture contains the JD source, candidate profile and hand-labeled oracle.
- The analysis CLI reads local UTF-8 JD text and a candidate profile, then writes a schema-valid, evidence-backed DecisionCard without reading the oracle.
- A separate comparator reconstructs the expected card and reports MATCH or MISMATCH.
- Generated outputs are ignored; the committed fixture contains no real personal identity or contact data.

## Verified Evidence

- `python -m pytest projects/internship-research/tests -q` completed with 6 passed.
- The end-to-end test runs the analysis CLI, verifies an oracle MATCH, changes a schema-valid verdict and verifies a MISMATCH with exit code 1.
- Negative tests reject a missing evidence quote, an unknown evidence reference and a string used where a strict integer is required.
- A candidate with only three available months produces `duration=not_met` and `not_suitable`.
- The normal fixture preserves missing salary, education, overtime, mentorship and application-deadline fields as unknown and produces `needs_verification`.

## Fixed Decisions

- Start with one JD, not open-web job discovery.
- Use a concise decision card, not a long free-form report.
- Keep confirmed facts, unknowns and judgments separate.
- Require field-level evidence for confirmed facts.
- Use transparent dimensions and hard constraints, not an uncalibrated total score.
- Keep assessment deterministic after extraction.
- Keep the first implementation CLI-only, single-agent and read-only.
- Do not rebase or migrate the old branch wholesale.

## Remaining Gaps

- The current extractor deliberately recognizes only the exact controlled `jd_001` wording; it is not a general JD parser.
- There is no real-model extraction, structured trace, provider configuration, latency or token accounting.
- There is no public-page acquisition tool, timeout classification or blocked-page behavior.
- The fixed eval set contains 1 of the 10 initial fixtures required by [PROJECT.md](PROJECT.md).
- CI and a concise user-facing project README are not yet present.

## Single Next Task

Add grounded real-model extraction for pasted JD text behind the existing schema and evidence gates.

The next slice must:

1. accept at least one JD whose wording is not encoded as fixture constants;
2. require structured model output to pass the strict schemas;
3. require every confirmed fact quote to be an exact substring of the supplied JD;
4. preserve unsupported fields as unknown;
5. keep constraint, dimension and verdict evaluation deterministic after extraction;
6. record a readable trace with provider/model identity, latency, token usage when available and a stable failure class;
7. keep all six current tests green and add model-boundary tests with a deterministic fake.

Do not add URL acquisition, open-web search, API, UI, persistence, scheduler, multi-agent orchestration or application tracking in this task.
