# Learning Progress

Last updated: 2026-08-27

## Target

- Career direction: Agent engineering.
- Delivery target: one clean-clone, runnable, testable and explainable Agent project suitable for internship applications.
- Working mode: project-driven fast track; do not resume the old linear Stage 0–8 course.

## Current Position

- The first project is selected: **Internship Research Agent**.
- Offline phase one is implemented: one candidate profile plus one controlled JD now produces an evidence-backed DecisionCard through a tested CLI path.
- The implementation milestone is preserved at [commit 30529d6](https://github.com/littlemuu/Agent-Learning-Hub/commit/30529d663d033486e689065a909b55918326efc2).
- Stable project decisions are in [projects/internship-research/PROJECT.md](projects/internship-research/PROJECT.md).
- Current project work and its single next task are in [projects/internship-research/PROGRESS.md](projects/internship-research/PROGRESS.md).
- The earlier implementation in [littlemuu/hello-agents:internship-agent](https://github.com/littlemuu/hello-agents/tree/internship-agent) remains a historical reference rather than an implementation base.

## Verified Capabilities

- Can explain chatbot, workflow, Agent and multi-agent boundaries.
- Understands the Agent loop, tool registry, structured tool arguments, maximum steps and controlled failure states.
- Understands retrieval, source, citation, threshold, top-k and explicit insufficient-evidence behavior.
- Has related practical experience with MCP, OAuth, permission gates, deployment, CI, diagnostics and Skill packaging.
- Can identify scope inflation, evidence breaks and uncalibrated decision logic in an existing Agent application.
- Can define strict structured-output contracts and separate structural validation from cross-file evidence validation.
- Can construct a hand-labeled oracle, enforce exact source quotes and preserve unsupported facts as unknown.
- Can implement deterministic hard constraints and three-state verdict behavior behind a CLI.
- Can test both schema-invalid failures and schema-valid but semantically wrong outputs; the current project suite has 6 passing tests.

Historical in-repository evidence is preserved at [legacy snapshot c226e51](https://github.com/littlemuu/Agent-Learning-Hub/tree/c226e51dc07cf428e49d284a86d1ba898ccfa10e).

## Material Decisions

- Start with one JD and separate evidence-backed analysis from later job discovery.
- Do not continue or rebase the old DeepResearch-derived branch.
- Do not use a free-form 0–100 total match score.
- Do not build UI, SSE, application tracking, multi-agent, RAG or long-term memory before the core eval gate passes.
- Keep real personal profile data local and ignored.
- Keep downstream decision logic deterministic even after model extraction is introduced.

## Remaining Gaps

- Replace the fixture-specific extractor with grounded real-model extraction while retaining the current evidence and schema gates.
- Add a read-only acquisition tool, trace and explicit timeout or blocked-page failure behavior.
- Expand from 1 to at least 20 eval cases and add CI.
- Produce a concise portfolio explanation with architecture, trade-offs, failures, limits, cost and latency.

## Single Next Task

Add grounded real-model extraction for pasted JD text behind the existing DecisionCard schema, exact-quote evidence validation and deterministic assessment logic. Use a deterministic fake for tests and do not add network acquisition or UI yet.

## Update Rule

Update this file only when the selected project, global stage, verified capability or global next task changes. Project-level milestones belong in the active project's PROGRESS.md.
