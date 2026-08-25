# Learning Progress

Last updated: 2026-08-25

## Target

- Career direction: Agent engineering.
- Delivery target: one clean-clone, runnable, testable and explainable Agent project suitable for internship applications.
- Working mode: project-driven fast track; do not resume the old linear Stage 0–8 course.

## Current Position

- Foundations are sufficient to start a real vertical slice.
- The old toy Agent/RAG exercises are historical evidence, not the active implementation.
- No active project has been selected yet.
- Recommended candidate: Internship Research Agent.

## Verified Capabilities

- Can explain chatbot, workflow, Agent and multi-agent boundaries.
- Understands the Agent loop, tool registry, structured tool arguments, maximum steps and controlled failure states.
- Understands the basic RAG path and the roles of chunk, embedding, retrieval, source, citation, threshold and top-k.
- Can distinguish retrieval-layer data from answer-layer evidence and model insufficient evidence explicitly.
- Has related practical experience with MCP, OAuth, permission gates, deployment, CI, diagnostics and Skill packaging.

Historical in-repository evidence is preserved at [legacy snapshot `c226e51`](https://github.com/littlemuu/Agent-Learning-Hub/tree/c226e51dc07cf428e49d284a86d1ba898ccfa10e).

## Remaining Gaps

- Build a complete project with a real LLM and real tools instead of a fake model or three hard-coded chunks.
- Make the project reproducible with declared dependencies, a clean setup path and portable configuration.
- Add formal tests, trace capture, an eval set and CI.
- Demonstrate timeout, limited retry, stopping conditions and human approval for risky actions.
- Produce a concise portfolio explanation covering architecture, trade-offs, failures and limits.

## Single Next Task

Confirm the first vertical-slice project. The recommended option is **Internship Research Agent**; implementation must not begin until the learner confirms this project or selects another candidate.

After confirmation, write a one-page project specification containing:

1. user and problem;
2. success criteria;
3. first-version inputs and outputs;
4. 2–3 tools and their schemas;
5. state and failure modes;
6. permission boundaries;
7. initial eval cases.

## Update Rule

Update this file only when a durable capability is verified, an artifact is runnable, a material gap is discovered, or the single next task changes. Do not append lesson transcripts or daily timelines.
