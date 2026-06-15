# Learning Progress

## Learner Profile

- Python: can read code and has experience configuring environments and running or
  developing projects, but has limited independent coding practice.
- TypeScript: no prior experience.
- HTTP API and JSON: basic familiarity, not yet deep.
- LLM experience: has called LLM APIs, run Agent projects, and written some
  functions with AI assistance.
- Agent practice: has used tool calling or RAG-related projects, but wants a deeper
  understanding of the underlying mechanisms.

## Current Position

- Current stage: Stage 0 - Understand What An Agent Is.
- Recommended path: quickly complete Stage 0, then build the Stage 1 minimal Agent
  loop in Python.
- Learning emphasis: strengthen independent Python implementation while learning
  the Agent loop, structured JSON, tool calling, limits, timeouts, and error
  handling.

## Session Log

### 2026-06-15 - Baseline Assessment

Demonstrated:

- Correctly described a chatbot as a conversational interaction form.
- Correctly described a workflow as a predefined execution process.
- Correctly described an Agent as dynamically choosing actions from user input and
  context, within defined tools and boundaries.
- Has practical exposure to LLM APIs and Agent projects.

Gaps:

- Needs to distinguish interaction form from implementation: a chatbot interface
  may be backed by a simple model call, a workflow, or an Agent.
- Needs deeper understanding of multi-agent systems and the Agent execution loop.
- Needs more independent Python implementation practice.

### 2026-06-15 - Stage 0 Lesson 1

Topic: distinguishing chatbot, workflow, and Agent, and deciding when not to use an
Agent.

Evidence:

- Classified a fixed OCR -> extraction -> validation -> database pipeline as a
  workflow because its steps are predetermined and require reliability.
- Classified an autonomous research task as an Agent because it dynamically
  chooses searches, decides whether to continue, and produces a report.
- Classified a one-response customer support interface as a chatbot.
- Explained that a predictable, strict process should use a workflow when Agent
  uncertainty would reduce stability or efficiency.

README updates:

- Completed: knowing when not to use an Agent.
- Partial: distinguishing chatbot, workflow, Agent, and multi-agent. The
  multi-agent part has not yet been assessed.

Next task:

- Distinguish a single Agent from a multi-agent system.
- Explain the observe -> think/decide -> act -> observe loop and identify its parts
  in a concrete scenario.

### 2026-06-15 - Stage 0 Lesson 2

Topic: single-Agent versus multi-agent systems and the Agent loop.

Evidence:

- Explained that a single Agent handles the task through one decision-making loop,
  while a multi-agent system divides responsibilities such as planning, coding,
  and reviewing across Agents.
- Correctly stated that multi-agent systems are not inherently better and add
  unnecessary coordination overhead for simple tasks.
- Initially reversed `observe` and `act` in a search example, showing that the
  Agent loop still needs practice.

README updates:

- Completed: distinguishing chatbot, workflow, Agent, and multi-agent.
- In progress: understanding observe -> think/decide -> act -> observe.

Next task:

- Correctly label each step of a concrete Agent execution trace as observation,
  decision/reasoning, or action.

### 2026-06-15 - Stage 0 Lesson 3

Topic: identifying the steps in the Agent execution loop.

Evidence:

- Correctly labeled the user request as an observation.
- Correctly labeled choosing the weather tool and deciding that the result was
  sufficient as thinking/decision steps.
- Correctly labeled calling the tool and returning the final answer as actions.
- Correctly labeled the tool result as a new observation.

README updates:

- Completed: understanding observe -> think/decide -> act -> observe.

Next task:

- Read and discuss Anthropic's `Building effective agents`.
- Focus on the distinction between workflows and Agents, common workflow patterns,
  and when added autonomy is justified.

### 2026-06-15 - Anthropic Reading Pre-assessment

Demonstrated:

- Identified the main costs of adding Agents: model/API expense, latency, process
  complexity, lower stability, and harder coordination or management.
- Preferred direct, simple code over adding a framework when the underlying
  control flow can remain clear.

Gaps:

- Has not yet studied common workflow patterns such as prompt chaining, routing,
  and orchestrator-workers.

Next task:

- Learn prompt chaining first, including its control flow, appropriate use cases,
  and tradeoffs.

### 2026-06-15 - Anthropic Pattern 1: Prompt Chaining

Demonstrated:

- Designed a fixed sequence for job-description analysis, report review, cover
  letter generation, and final validation.
- Correctly chose prompt chaining instead of an Agent because the task has a
  predictable path, defined inputs and outputs, and few steps.

Gaps:

- Needs to define explicit input and output contracts for every step, especially
  review steps.
- Needs to distinguish deterministic program validation from subjective
  model-based content review.

Next task:

- Refine the cover-letter workflow with explicit step contracts and separate
  program checks from LLM quality checks.

### 2026-06-15 - Prompt Chaining Verification

Demonstrated:

- Correctly tied missing-field behavior to schema requirements and an explicit
  fallback policy instead of always continuing or always failing.
- Correctly chose deterministic code to enforce a measurable length limit.
- Understood that semantic checks require model judgment.

Correction:

- An LLM cannot reliably detect invented experience without grounding evidence.
  The review step must receive the candidate's source resume/profile and require
  every factual claim to be supported. Important structured facts can also be
  compared in code.

Status:

- Prompt chaining: understood at the introductory level.

Next task:

- Learn routing: classify an input, select a specialized path, and define behavior
  for uncertain classifications.

### 2026-06-15 - Anthropic Pattern 2: Routing

Demonstrated:

- Understood that routing selects a specialized workflow based on clear task or
  intent boundaries.
- Recognized that uncertain classifications may need human review.
- Recognized that a wrong route can cause task failure.

Gaps:

- "Ask the LLM to think again" is not by itself a robust uncertainty policy.
- Needs concrete low-confidence handling: request clarification, use a safe generic
  path, retry with more context, or escalate to a human.
- Needs to account for consequences beyond a poor answer, including skipped
  validation, incorrect permissions, policy violations, and unsafe actions.

Next task:

- Design a routing decision that includes confidence thresholds and a safe fallback
  path.

### 2026-06-15 - Routing Verification

Demonstrated:

- Correctly applied the confidence threshold: a refund probability of `0.65`
  requires clarification rather than entering the refund workflow.
- Proposed a direct clarification question asking whether the user wants a refund.
- Included explicit user choices rather than silently guessing intent.

Design note:

- Keep intent selection and escalation preference separate where possible. "Yes"
  or "No" resolves refund intent; "contact a human" is a separate escalation
  action.

Status:

- Routing: understood at the introductory level.

Next task:

- Learn parallelization: decide when independent LLM calls can run concurrently
  and how their outputs should be aggregated.

### 2026-06-15 - Anthropic Pattern 3: Parallelization

Demonstrated:

- Identified independence and lack of exclusive-resource conflicts as conditions
  for parallel execution.
- Proposed an aggregation stage that reviews and merges multiple code-review
  outputs.
- Identified lower elapsed time and possible result conflicts as tradeoffs.

Corrections:

- Tasks are not parallelizable when one result can change the other's requirements;
  answering a clarification question may need to happen before writing code.
- For remote LLM APIs, the main costs are additional tokens/API expense, provider
  rate limits, conflicting outputs, and aggregation complexity. Local memory may
  matter for self-hosted models but is not usually the primary concern for hosted
  APIs.
- An LLM aggregator should not blindly summarize. It should deduplicate findings,
  compare evidence, rank severity, and preserve disagreements or uncertainty.

Next task:

- Identify dependencies in a concrete research workflow and choose which steps can
  run concurrently.

### 2026-06-15 - Parallelization Verification

Demonstrated:

- Correctly identified official-source search, paper search, and news search as
  parallel branches after the topic has been analyzed.
- Correctly avoided stopping all other independent searches when one branch fails.

Correction:

- The dependency graph is `A -> (B, C, D) -> E -> F`: B, C, and D wait for topic
  analysis; evidence aggregation waits for the search branches; final writing waits
  for aggregation.
- A failed official-source branch should normally trigger retry or a fallback and
  be reported to the aggregation step. If official evidence is a required success
  criterion, the system must not present the final report as complete without it.

Status:

- Parallelization: understood at the introductory level.

Next task:

- Learn orchestrator-workers: let a coordinator dynamically create and assign
  subtasks when their number or shape cannot be fixed in advance.

### 2026-06-15 - Anthropic Pattern 4: Orchestrator-Workers

Demonstrated:

- Correctly described the orchestrator as interpreting work and assigning it to
  suitable workers.
- Correctly kept cross-worker task allocation under orchestrator control rather
  than allowing workers to change the global plan freely.
- Recognized that this pattern adds a dynamic coordination and assignment stage.

Clarification:

- Fixed parallelization defines branches in code ahead of time. In an
  orchestrator-workers system, the orchestrator determines the number, type, and
  boundaries of subtasks from the current input, then combines worker results.

Next task:

- Design dynamic worker assignments for a research task whose required subtasks
  vary with the user's topic.

### 2026-06-15 - Orchestrator-Workers Exercise

Demonstrated:

- Defined worker inputs and outputs instead of leaving responsibilities implicit.
- Kept final synthesis under a coordinating component.
- Proposed explicitly investigating conflicting worker conclusions.
- Correctly noted that clear, fixed processes do not justify dynamic orchestration.

Correction:

- The proposed sequence of framework analysis -> requirement analysis -> fit
  analysis -> recommendation is mostly a fixed workflow because the worker types
  and order are known in advance.
- A stronger orchestrator-workers design first identifies the candidate frameworks
  and comparison dimensions, dynamically creates one or more research tasks, then
  assigns synthesis or verification work based on the returned evidence.
- Conflict resolution should request evidence and apply shared evaluation criteria,
  not merely ask another worker to choose a side.

Status:

- Orchestrator-workers: concept understood, dynamic task generation still needs
  verification.

Next task:

- Rewrite the Python framework comparison as a dynamic task list created by the
  orchestrator.

### 2026-06-15 - Dynamic Orchestration Verification

Demonstrated:

- Correctly made worker count depend on the number of candidates discovered by the
  orchestrator.
- Identified framework research, evidence verification, and report synthesis as
  useful responsibilities.

Correction:

- "After comparing all frameworks" is not an executable stopping condition for an
  open-ended web search because completeness cannot usually be proven.
- The orchestrator must operationalize "all" using a bounded candidate scope and
  stopping rules, such as approved source lists, relevance thresholds, time or
  iteration limits, and no-new-candidate convergence.

Next task:

- Define measurable candidate-selection and stopping rules for the high-concurrency
  Python framework search.

### 2026-06-15 - Orchestrator-Workers Verification

Demonstrated:

- Defined bounded candidate criteria: active maintenance, ASGI support, a release
  within two years, and public performance or production evidence.
- Set a maximum of five search rounds.
- Defined convergence as two consecutive rounds without a new qualifying candidate.
- Proposed ranking candidates when the result set is too large.

Clarification:

- Selection should use a shared scorecard rather than performance alone. Relevant
  dimensions include performance, maintenance health, ecosystem, documentation,
  operational maturity, and fit for the user's requirements.

Status:

- Orchestrator-workers: understood at the introductory level.

Next task:

- Learn evaluator-optimizer: iteratively generate, evaluate against explicit
  criteria, and revise until a quality threshold or stopping condition is reached.

### 2026-06-15 - Session Paused

- The learner chose to pause after completing the introductory
  orchestrator-workers pattern.
- Resume point: Anthropic workflow pattern `evaluator-optimizer`.
- Resume with the three pending diagnostic questions about iterative evaluation,
  actionable feedback, and stopping conditions.
- Stage 0 remains in progress. The OpenAI official reading task and the Stage 0
  written artifact are not yet complete. The Anthropic reading item is already
  marked complete in the remote README; discussion resumes at evaluator-optimizer.
