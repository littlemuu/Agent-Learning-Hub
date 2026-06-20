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

### 2026-06-16 - Evaluator-Optimizer Pre-assessment

Demonstrated:

- Understood that evaluator-optimizer uses explicit evaluation criteria rather
  than a vague request to "improve it".
- Recognized that the evaluator should identify concrete improvement areas.
- Proposed practical stopping conditions: little improvement after two
  optimization rounds, or repeated feedback across rounds.

Gap:

- Needs to make evaluator feedback more operational by tying each issue to an
  expected output change, evidence, severity, or pass/fail criterion.

Next task:

- Design a small evaluator-optimizer workflow with explicit criteria, actionable
  feedback, and stopping rules.

### 2026-06-16 - Evaluator-Optimizer Exercise

Demonstrated:

- Identified useful generator inputs for a cover-letter workflow: job
  information, candidate information, and formatting requirements.
- Proposed relevant evaluator criteria: job fit, candidate skill evidence, and
  format correctness.
- Added a hard iteration limit: stop after more than five rounds.

Gap:

- Evaluator output fields were still too high-level. Fields such as "match",
  "information correctness", and "format correctness" should be expanded into
  pass/fail or score, evidence, concrete issues, and revision instructions so the
  optimizer can act on them.

Next task:

- Refine evaluator output into an actionable schema and distinguish scores from
  revision instructions.

### 2026-06-16 - Evaluator-Optimizer Verification

Demonstrated:

- Rewrote vague evaluator feedback into actionable feedback with evidence,
  issue, and revision instruction.
- Correctly grounded the evidence in a mismatch between the job requirement
  (`C++`) and the cover letter's vague wording ("proficient in programming").
- Correctly identified the problem as a missing connection between the candidate's
  tech stack and the target role.

Correction:

- The revision instruction should ask for a concrete C++ learning or development
  experience, not merely a general claim. The candidate source material is needed
  before adding factual experience to avoid hallucinated claims.

Status:

- Evaluator-optimizer: understood at the introductory level.

Next task:

- Learn the final Anthropic distinction between workflow patterns and fully
  autonomous agents, then finish the Stage 0 written artifact.

### 2026-06-16 - Evaluator-Optimizer Evidence Check

Demonstrated:

- Correctly explained that evaluator feedback needs evidence to reduce invented
  or unsupported issues.
- Understood that evidence anchors feedback to the source material and current
  output, making the next optimization step safer.

Status:

- Evaluator-optimizer: verified at the introductory level.

Next task:

- Learn the final distinction between workflow patterns and autonomous agents,
  then write the Stage 0 artifact: why the learner's target scenario needs an
  Agent rather than a normal workflow.

### 2026-06-16 - Workflow Patterns Versus Agents

Demonstrated:

- Correctly stated that using prompt chaining, routing, parallelization, or
  evaluator-optimizer does not automatically make a system an Agent.
- Understood that these patterns can be implemented as workflows and may not
  involve autonomous model decisions.

Clarification:

- A workflow can contain LLM calls but still follow a fixed control flow. An Agent
  is characterized by dynamic decision-making about what to do next based on
  observations, context, tool results, and stopping conditions.

Next task:

- Write the Stage 0 artifact explaining a target scenario and why it needs an
  Agent rather than a normal workflow.

### 2026-06-16 - Stage 0 Artifact Draft

Demonstrated:

- Correctly identified a core reason to use an Agent: the task path cannot be
  fully fixed in advance.
- Correctly stated that the Agent must dynamically decide how to complete the
  task and which tools to use.
- Proposed useful boundaries: a limited Python tool file, maximum five steps,
  human confirmation for modification permissions, and stopping on timeout or
  iteration limit.

Gap:

- The artifact is still generic and does not name a concrete target scenario.
  Stage 0 output requires explaining why a specific scenario needs an Agent rather
  than a normal workflow.

Next task:

- Revise the Stage 0 artifact by adding a concrete scenario and tying the dynamic
  decisions and boundaries to that scenario.

### 2026-06-16 - Stage 0 Artifact Verification

Demonstrated:

- Chose a concrete target scenario: diagnosing a web project that fails to run.
- Explained why a fixed workflow is insufficient: the cause may be in runtime
  setup, dependency configuration, logs, or specific code paths, so the next step
  depends on intermediate observations.
- Identified dynamic Agent decisions: try running the project, inspect errors,
  choose the most likely code or configuration area to review, and decide whether
  further tool use is needed.
- Kept practical boundaries from the draft: limited tools, maximum five steps,
  human confirmation for modification permission, and stopping on timeout or
  iteration limit.

Status:

- Stage 0 written artifact: demonstrated at the introductory level.
- Stage 0 remains in progress because the OpenAI practical guide reading has not
  yet been confirmed and summarized.

Next task:

- Confirm and discuss the OpenAI practical guide reading, then move to Stage 1:
  structured JSON output and a minimal Python Agent loop.

### 2026-06-16 - OpenAI Practical Guide Verification

Demonstrated:

- Correctly distinguished ordinary LLM workflows from Agents: a normal LLM app may
  include LLM workflow steps, while an Agent uses the model to manage execution,
  make dynamic decisions, and choose tools.
- Correctly identified suitable Agent scenarios: complex decisions, hard-to-
  maintain rules, and tasks depending on unstructured data.
- Correctly named the core Agent design components: model, tools, and
  instructions.
- Applied guardrail thinking to the web debugging Agent: reading environment
  configuration and modifying code should require explicit confirmation.

README updates:

- Completed: OpenAI practical guide reading.

Status:

- Stage 0 complete at the introductory level.

Next task:

- Start Stage 1 with structured JSON output, then build a minimal Python Agent
  loop.

### 2026-06-16 - Stage 1 Diagnostic Assessment

Demonstrated:

- Has modified existing LLM API code and used Tavily-related project code, but is
  not yet fully clear on the distinction between an SDK and a direct API call.
- Can recognize JSON visually, but cannot yet confidently describe JSON data
  types or parse nested fields in Python.
- Understands that a tool function is intended to be called by an Agent, not only
  directly by application code.

Gaps:

- Needs introductory practice with JSON objects, arrays, strings, numbers, and
  nested dictionaries.
- Needs to learn how model action JSON maps to Python dictionaries and tool
  function arguments.
- Needs a concrete distinction between SDK calls and raw HTTP/API calls.

Next task:

- Learn structured JSON output and parse a simple model action object in Python.

### 2026-06-16 - JSON Field Access Exercise

Demonstrated:

- Correctly accessed top-level JSON/dict fields with `data["action"]` and
  `data["confidence"]`.
- Correctly accessed a nested tool argument with
  `data["arguments"]["expression"]`.

Status:

- Basic nested JSON/dict field access: understood.

Next task:

- Parse a JSON string with `json.loads`, validate required fields, and connect the
  parsed action to a Python tool function.

### 2026-06-16 - JSON String Parsing Exercise

Demonstrated:

- Correctly used `json.loads(text)` to parse a model-returned JSON string into a
  Python dictionary.
- Correctly extracted the top-level action with `data["action"]`.
- Correctly extracted a nested tool argument with `data["arguments"]["path"]`.

Status:

- JSON string parsing and nested field access: understood at the introductory
  level.

Next task:

- Add minimal validation for parsed model action JSON before executing a tool.

### 2026-06-16 - Tool Action Validation Pre-check

Demonstrated:

- Recognized that an Agent must check whether a requested tool exists and is
  allowed before execution.

Gap:

- The proposed checks overlapped. Needs to separate tool allowlist validation from
  argument presence, argument type validation, and permission/risk checks.

Next task:

- Practice validating a parsed action object before dispatching it to a Python
  tool function.

### 2026-06-16 - Tool Argument Validation Exercise

Demonstrated:

- Correctly rejected a `calculator` action whose argument name was `expr` instead
  of the required `expression`.
- Understood that an allowed tool name is not enough; the parsed action must also
  match the tool's argument schema before execution.

Status:

- Minimal tool argument validation: understood.

Next task:

- Connect validated action JSON to a Python tool dispatch table.

### 2026-06-16 - Tool Dispatch Exercise

Demonstrated:

- Correctly built a tool table with `tools = {"repeat": repeat}`.
- Correctly retrieved a tool function from the table and executed it with parsed
  arguments.

Clarification:

- Direct positional passing works for a known tool, but a generic Agent dispatcher
  usually uses `tool_func(**arguments)` after validating the argument schema.

Status:

- Basic Python tool dispatch: understood.

Next task:

- Learn why `eval` is unsafe for a calculator tool and implement a safer scoped
  exercise tool before building the full loop.

### 2026-06-16 - Session Paused

- The learner chose to pause during Stage 1 after understanding basic Python tool
  dispatch.
- Resume point: implement a safe `add(a: int, b: int) -> int` tool, register it
  in a `tools` dictionary, dispatch it from parsed action JSON, and print the
  result.
- Do not continue to full tool calling until the learner has written and
  understood the safe dispatch exercise.

### 2026-06-20 - Safe Add Tool Dispatch Attempt

Demonstrated:

- Correctly used the generic dispatch shape: retrieve `action`, retrieve
  `arguments`, look up `tool_func = tools[action]`, then call
  `tool_func(**arguments)`.
- Correctly registered the tool name in a `tools` dictionary.

Gap:

- The `arguments` object did not match the `add(a, b)` function schema. It used
  `expression` instead of required parameters `a` and `b`.
- Needs to include the actual `add` function definition in the runnable snippet.

Next task:

- Correct the safe `add` dispatch snippet so that `arguments` contains integer
  fields `a` and `b`, then run through why `tool_func(**arguments)` works.

### 2026-06-20 - Safe Add Tool Dispatch Verification

Demonstrated:

- Correctly matched the `add(a, b)` tool schema with action arguments
  `{"a": 10, "b": 20}`.
- Correctly predicted that dispatching those arguments to `add` returns `30`.

Status:

- Safe single-tool dispatch: understood at the introductory level.

Next task:

- Add minimal validation before dispatch: check that the action is allowed, the
  required arguments are present, and the argument values have the expected types.

### 2026-06-20 - Tool Argument Type Validation

Demonstrated:

- Correctly rejected `{"a": 10, "b": "20"}` for `add(a: int, b: int)` because
  `"20"` is a string rather than an integer.
- Understood that valid tool name and valid parameter names are not sufficient;
  argument values must also match the expected types.

Status:

- Minimal action/argument/type validation: understood conceptually.

Next task:

- Write a small Python validation block for `add`: allowed action, required
  arguments `a` and `b`, and integer types.

### 2026-06-20 - Unknown Tool Validation Exercise

Demonstrated:

- Correctly identified that an action `multiply` should be rejected when only
  registered tools are allowed.
- Understood that the allowlist check happens before argument validation and
  dispatch.

Status:

- Tool allowlist validation: understood.

Next task:

- Practice the other validation branches: missing required arguments and wrong
  argument types.

### 2026-06-20 - Missing Argument Validation Exercise

Demonstrated:

- Correctly identified that `{"action": "add", "arguments": {"a": 2}}` should be
  rejected with a missing required arguments error because `b` is absent.

Status:

- Missing argument validation: understood.

Next task:

- Combine allowlist, missing-argument, and type checks into one runnable dispatch
  snippet.

### 2026-06-20 - Combined Dispatch Snippet Attempt

Demonstrated:

- Correctly included the main pieces of a dispatch snippet: tool definition,
  `tools` registry, action JSON, action/argument extraction, validation branches,
  and tool execution with `tool_func(**arguments)`.
- Correctly used `isinstance(..., int)` for integer type validation.

Gaps:

- Python function syntax was mixed with JavaScript/C-style braces; Python needs a
  colon and an indented `return`.
- The unknown-tool branch printed the wrong error message.
- The missing-argument branch was omitted, which can cause `KeyError` before type
  validation when `a` or `b` is absent.
- Indentation around `elif`/`else` needs to align with the original `if`.

Next task:

- Rewrite the dispatch snippet with valid Python syntax and all three validation
  branches: unknown tool, missing argument, wrong type.

### 2026-06-20 - Validation Order Check

Demonstrated:

- Correctly explained why missing-argument validation must run before type
  validation: otherwise reading a missing key such as `arguments["b"]` can raise
  an error before the validator returns a controlled message.

Status:

- Minimal validated dispatch logic: conceptually understood.

Next task:

- Have the learner rewrite the corrected validated dispatch snippet once, then
  mark the simple tool-function item complete if the code is structurally correct.

### 2026-06-20 - Validated Dispatch Rewrite Attempt

Demonstrated:

- Preserved the intended dispatch structure and all three validation branches:
  unknown tool, missing argument, and wrong type.
- Correctly used the intended `add` action data and `tool_func(**arguments)` in
  the execution branch.

Gaps:

- Function definition syntax is still not valid Python: `def add(...) -> int`
  needs a trailing colon, and `return` must be indented inside the function body.
- `elif` and `else` must align with the original `if`, not be indented under the
  first branch.

Next task:

- Fix Python indentation and colon syntax for the same validated dispatch snippet.

### 2026-06-20 - Python Function Syntax Check

Demonstrated:

- Correctly wrote a valid Python function definition for
  `add(a: int, b: int) -> int`.
- Correctly indented the `return a + b` line inside the function body.

Status:

- Basic Python function syntax for the `add` tool: understood.

Next task:

- Verify `if`/`elif`/`else` alignment, then complete the validated dispatch
  snippet.

### 2026-06-20 - If/Elif Alignment Check

Demonstrated:

- Correctly identified that `elif` should align with the original `if`, not the
  indented statement inside the `if` branch.

Learning preference:

- The learner requested skipping very basic syntax multiple-choice questions for
  now. Future Stage 1 practice should check syntax through small runnable snippets
  rather than isolated beginner-level questions unless needed.

Next task:

- Move from isolated dispatch syntax to a small runnable validated dispatch
  snippet, then connect it to the next Stage 1 topic: structured model output.

### 2026-06-20 - Structured JSON Output Exercise

Demonstrated:

- Correctly produced structured JSON for the request "calculate 10 plus 20":
  action `add` with integer arguments `a = 10` and `b = 20`.
- Matched the model output schema to the Python tool function signature
  `add(a: int, b: int)`.

Status:

- Simple structured JSON action output: understood.

Next task:

- Explain why an Agent prompt should require strict JSON output before parsing and
  dispatching tools.

### 2026-06-20 - Structured JSON Output Verification

Demonstrated:

- Correctly explained that the model should output only JSON because the output
  must be parsed by a program.
- Understood that structured JSON avoids guessing action names and arguments from
  free-form natural language.

README updates:

- Completed: model can output structured JSON.

Status:

- Stage 1 structured JSON output: complete at the introductory level.

Next task:

- Complete the simple tool-function item by writing a small runnable `add` tool
  and dispatch snippet, then move toward parsing model tool calls.

### 2026-06-20 - Tool Function Item Completion

Demonstrated:

- Understood that a tool function is a normal Python function exposed for Agent
  use through a controlled registry.
- Practiced defining a safe `add(a: int, b: int) -> int` tool.
- Practiced registering the tool in a `tools` dictionary and dispatching parsed
  JSON arguments with `tool_func(**arguments)`.
- Understood basic validation around tool names, required arguments, and argument
  types.

README updates:

- Completed: define a tool function such as `search`, `calculator`, or
  `read_file`.

Status:

- Stage 1 tool function definition: complete at the introductory level.

Next task:

- Learn to parse a model tool call/function call represented as structured JSON.

### 2026-06-20 - Model Tool Call Parsing Attempt

Demonstrated:

- Correctly identified the parsed fields needed from a model tool call:
  `action`, `arguments`, and the nested `path` argument.
- Correctly used `arguments["path"]` after extracting the arguments object.

Gap:

- The model output should be parsed from a JSON string with `json.loads`, not
  manually rewritten as a Python dictionary.
- Needs attention to balanced braces when writing inline dictionaries or JSON.

Next task:

- Parse `model_output` with `json.loads`, then extract `action`, `arguments`, and
  nested tool arguments.

### 2026-06-20 - Model Tool Call Parsing Verification

Demonstrated:

- Correctly used `json.loads(model_output)` to parse a model-returned JSON string.
- Correctly extracted `action`, `arguments`, and a nested argument field such as
  `path`.

Clarification:

- Top-level statements in a Python file should not be indented unless they are
  inside a block such as a function, `if`, or loop.

Status:

- Basic parsing of a model tool call represented as JSON: understood at the
  introductory level.

Next task:

- Distinguish JSON-string tool calls from SDK-native function/tool call objects,
  then parse and dispatch one complete model action.

### 2026-06-20 - Tool Call Parsing Item Completion

Demonstrated:

- Parsed a JSON-string model tool call with `json.loads(model_output)`.
- Extracted `action`, `arguments`, and nested argument fields such as `path`.
- Understood that SDK-native tool calls may expose structured fields directly,
  but the core idea is still to retrieve tool name and arguments.

Decision:

- The learner chose to skip the combined parse-and-dispatch drill for now.

README updates:

- Completed: parse model tool call / function call.

Status:

- Stage 1 model tool-call parsing: complete at the introductory level.

Next task:

- Learn to execute a tool and feed the tool result back to the model.

### 2026-06-20 - Tool Result Feedback Concept

Demonstrated:

- Understood that after tool execution, the model needs the tool result to produce
  a final answer in natural language.

Clarification:

- Some programs can directly return tool results without another model call, but
  an Agent loop feeds the result back as a new observation so the model can decide
  whether to continue or provide the final response.

Next task:

- Represent the post-tool observation message that would be sent back to the
  model.

### 2026-06-20 - Tool Observation Message Exercise

Demonstrated:

- Produced a minimal post-tool observation message: "the tool result is 30".

Clarification:

- For reliability, the observation should include the tool name and result in a
  structured or consistently formatted way, especially when multiple tools may be
  used.

Next task:

- Format tool observations with tool name and result, then decide whether the
  model should continue or return a final answer.

### 2026-06-20 - Named Tool Observation Verification

Demonstrated:

- Correctly formatted an observation containing the tool name `read_file` and its
  returned result.

Status:

- Basic tool-result feedback message: understood.

Next task:

- Decide when the model should produce a final answer after receiving a tool
  result, versus when it should request another tool call.

### 2026-06-20 - Final Answer Decision Exercise

Demonstrated:

- Correctly decided that the model should return a final answer when the
  `read_file` result already contains the requested Stage 1 title.
- Understood that another tool call is unnecessary when the latest observation is
  sufficient to answer the user's question.

Status:

- Basic execute-tool-and-feed-result concept: understood at the introductory
  level.

Next task:

- Mark the README item for executing tools and feeding tool results back to the
  model, then start max steps, timeout, and error handling.

### 2026-06-20 - Tool Execution And Feedback Item Completion

Demonstrated:

- Understood that a tool result becomes a new observation for the model.
- Formatted tool-result feedback messages that include the tool name and result.
- Correctly decided that the model should stop and answer when the observation
  already contains the requested information.

README updates:

- Completed: execute a tool and feed the tool result back to the model.

Status:

- Stage 1 tool execution and feedback: complete at the introductory level.

Next task:

- Learn max steps, timeout, and error handling for the minimal Agent loop.

### 2026-06-20 - Max Steps Concept Check

Demonstrated:

- Correctly explained that an Agent loop needs `max_steps` because otherwise it
  may fail to terminate and waste resources.

Status:

- Purpose of maximum-step limits: understood.

Next task:

- Distinguish maximum-step limits from timeout limits, then practice basic error
  handling cases.

### 2026-06-20 - Timeout Concept Check

Demonstrated:

- Correctly distinguished `max_steps` from `timeout`: max steps prevents endless
  looping across turns, while timeout prevents the loop or an operation from
  being stuck too long.

Correction:

- Spelling: `max_steps`, not `max_teps`.

Status:

- Max steps and timeout concepts: understood.

Next task:

- Practice basic error handling for invalid JSON, unknown tools, missing
  arguments, wrong argument types, and tool execution errors.

### 2026-06-20 - Invalid JSON Error Handling

Demonstrated:

- Correctly identified that a natural-language tool request should be rejected as
  invalid JSON rather than allowed to crash the program.
- Proposed a controlled error message: model output is not valid JSON.

Status:

- Invalid JSON handling: understood.

Next task:

- Practice handling unknown tools and tool execution errors, then summarize the
  boundary checks needed for a minimal Agent loop.

### 2026-06-20 - Unknown Tool Error Handling

Demonstrated:

- Correctly identified that an action such as `delete_file` must be rejected when
  it is not in the registered/allowed tools.

Clarification:

- The check is both about whether the tool function exists and whether the Agent
  is authorized to call it. Unknown or unapproved tools must not execute.

Status:

- Unknown tool handling: understood.

Next task:

- Practice tool execution error handling, then complete the Stage 1 loop-boundary
  item.

### 2026-06-20 - Tool Execution Error Handling

Demonstrated:

- Correctly stated that tool execution errors such as a missing file should be
  caught and returned as controlled error information rather than crashing the
  Agent loop.

Status:

- Tool execution error handling: understood.

Next task:

- Mark the README item for max steps, timeout, and error handling, then define the
  Stage 1 final artifact: a 50-150 line minimal Agent.

### 2026-06-20 - Max Steps, Timeout, And Error Handling Completion

Demonstrated:

- Understood that `max_steps` prevents endless Agent loops and resource waste.
- Understood that timeout prevents a step or task from being stuck too long.
- Correctly handled invalid JSON as a controlled error.
- Correctly handled unknown or unauthorized tools as controlled errors.
- Correctly handled tool execution failure, such as missing files, by catching
  errors and returning controlled error information.

README updates:

- Completed: add max steps, timeout, and error handling to an Agent loop.

Status:

- Stage 1 checklist items are complete at the introductory level.
- Stage 1 output artifact is still pending.

Next task:

- Build the Stage 1 artifact: a 50-150 line minimal Python Agent that can choose a
  tool, execute it, and return a final answer.

### 2026-06-20 - Stage 1 Reference Implementation Saved

Artifact:

- Created `stage1.py` as a reference implementation for the Stage 1 minimal Agent
  loop.

Verification:

- Ran `python stage1.py`.
- Output: `Final answer: 30`.

Status:

- Reference code exists and runs.
- Stage 1 output artifact is not yet marked complete because the learner has not
  independently explained or modified the implementation.

Next task:

- Review `stage1.py` section by section, then have the learner make a small change
  such as adding a `multiply` tool or changing the fake model input case.
