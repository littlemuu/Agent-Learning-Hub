# Learning Progress

Last updated: 2026-08-25

## Target

- Career direction: Agent engineering.
- Delivery target: one clean-clone, runnable, testable and explainable Agent project suitable for internship applications.
- Working mode: project-driven fast track; do not resume the old linear Stage 0–8 course.

## Current Position

- The first project is selected: **Internship Research Agent**.
- Its first vertical slice is one candidate profile plus one public job URL or pasted JD to one evidence-backed DecisionCard.
- Stable project decisions are in [projects/internship-research/PROJECT.md](projects/internship-research/PROJECT.md).
- Current project work and its single next task are in [projects/internship-research/PROGRESS.md](projects/internship-research/PROGRESS.md).
- The earlier implementation in [littlemuu/hello-agents:internship-agent](https://github.com/littlemuu/hello-agents/tree/internship-agent) was audited and will remain a historical reference rather than an implementation base.

## Verified Capabilities

- Can explain chatbot, workflow, Agent and multi-agent boundaries.
- Understands the Agent loop, tool registry, structured tool arguments, maximum steps and controlled failure states.
- Understands retrieval, source, citation, threshold, top-k and explicit insufficient-evidence behavior.
- Has related practical experience with MCP, OAuth, permission gates, deployment, CI, diagnostics and Skill packaging.
- Can identify scope inflation, evidence breaks and uncalibrated decision logic in an existing Agent application.

Historical in-repository evidence is preserved at [legacy snapshot c226e51](https://github.com/littlemuu/Agent-Learning-Hub/tree/c226e51dc07cf428e49d284a86d1ba898ccfa10e).

## Material Decisions

- Start with one JD and separate evidence-backed analysis from later job discovery.
- Do not continue or rebase the old DeepResearch-derived branch.
- Do not use a free-form 0–100 total match score.
- Do not build UI, SSE, application tracking, multi-agent, RAG or long-term memory before the core eval gate passes.
- Keep real personal profile data local and ignored.

## Remaining Gaps

- Define executable schemas for profile, snapshot, evidence and decision card.
- Build the first deterministic offline fixture path.
- Add grounded real-model extraction, a read-only acquisition tool, trace and explicit failure behavior.
- Expand to at least 20 eval cases and add CI.
- Produce a concise portfolio explanation with architecture, trade-offs, failures, limits, cost and latency.

## Single Next Task

Implement and test one offline fixture to a schema-valid, evidence-backed DecisionCard CLI path, with no real network or LLM and no API or UI.

## Update Rule

Update this file only when the selected project, global stage, verified capability or global next task changes. Project-level milestones belong in the active project's PROGRESS.md.
