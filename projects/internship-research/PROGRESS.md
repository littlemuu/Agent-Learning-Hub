# Internship Research Agent — Progress

Last updated: 2026-08-25

## Status

- Internship Research Agent is the selected project.
- The first slice is fixed as one candidate profile plus one job URL or pasted JD to one evidence-backed DecisionCard.
- The legacy internship-agent branch has been audited and classified as a reference asset, not an implementation base.
- Stable scope, evidence rules, safety boundaries and the initial eval gate are documented in [PROJECT.md](PROJECT.md).
- No project code, dependency declaration, fixture or test has been added yet.

## Fixed Decisions

- Start with one JD, not open-web job discovery.
- Use a concise decision card, not a long free-form report.
- Keep confirmed facts, unknowns and judgments separate.
- Require field-level evidence for confirmed facts.
- Use transparent dimensions and hard constraints, not an uncalibrated total score.
- Keep the first implementation CLI-only, single-agent and read-only.
- Do not rebase or migrate the old branch wholesale.

## Remaining Gap

There is not yet a validated state contract or a deterministic offline path. Model, provider and framework selection are intentionally deferred until the fixture-based contract is executable.

## Single Next Task

Implement and test one offline fixture to a schema-valid, evidence-backed DecisionCard CLI path.

The task must define CandidateProfile, JobSnapshot, Evidence and DecisionCard; include at least one hand-labeled JD fixture; reject unsupported evidence references; and run without a real network or LLM.

Do not add an API, UI, persistence, scheduler, open-web search, multi-agent orchestration or application tracking in this task.
