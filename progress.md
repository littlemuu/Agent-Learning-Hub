# Learning Progress

## Learner Profile

- Python: can read code and run/modify existing projects, but still needs practice
  writing small programs independently.
- TypeScript: no prior experience.
- HTTP API and JSON: basic familiarity; JSON parsing and nested field access have
  been introduced.
- LLM/Agent practice: has used LLM APIs and Agent/RAG-related projects with
  assistance; wants to understand the underlying Agent loop and tool mechanism.
- Learning preference: skip very basic syntax multiple-choice checks when
  possible; prefer small runnable snippets and concrete project changes.

## Current Position

- Current stage: Stage 2 - Learn Tool Use, RAG, And Memory.
- Stage 0: complete at the introductory level.
- Stage 1 checklist: complete at the introductory level.
- Stage 1 artifact: complete at the introductory level.
- Current file: `codes/stage1.py` contains `add` and `multiply` tool paths and
  runs.
- Current notes: `notes/notes01.md` contains Stage 0-1 notes; `notes/notes2.md`
  is reserved for Stage 2 notes.
- Next task: start Stage 2 with a short diagnostic assessment on search/RAG,
  chunking, embeddings, citations, and tool failure handling.

## Completed README Items

### Stage 0

- Distinguished chatbot, workflow, Agent, and multi-agent.
- Understood `observe -> think/decide -> act -> observe`.
- Understood when not to use an Agent.
- Read and discussed Anthropic's `Building effective agents`.
- Read and summarized OpenAI's practical guide to building agents.
- Wrote the Stage 0 scenario: a Web project debugging Agent is useful because the
  failure path is not fixed and depends on runtime observations, logs, config, and
  code inspection.

### Stage 1

- Used an LLM API for ordinary conversation through existing code.
- Learned structured JSON output.
- Defined a simple tool function and tool registry.
- Parsed model tool calls represented as JSON.
- Understood executing tools and feeding tool results back as observations.
- Understood `max_steps`, timeout, and basic error handling.

## Key Evidence

- Correctly parsed JSON/dict fields such as `data["action"]`,
  `data["arguments"]["path"]`, and `json.loads(model_output)`.
- Correctly matched tool schemas, for example `add(a, b)` with
  `{"a": 10, "b": 20}`.
- Understood `tool_func(**arguments)` as dispatching parsed keyword arguments to a
  registered tool.
- Correctly rejected unknown tools, missing arguments, wrong argument types, and
  invalid JSON.
- Correctly explained that tool results must be sent back to the model as a new
  observation when the Agent needs a final answer or another decision.
- Created `stage1.py`; running `python stage1.py` produced `Final answer: 30`.
- Modified `stage1.py` to add a `multiply` tool path; running `python stage1.py`
  produced both `Final answer: 30` and `Final answer: 42`.
- Reorganized learning artifacts: moved `notes.md` to `notes/notes01.md`, created
  `notes/notes2.md` for Stage 2, and moved `stage1.py` to `codes/stage1.py`.

## Current Gaps

- Needs more independent practice writing valid Python snippets with indentation
  and function syntax.
- Needs continued practice keeping function names, tool registry keys, model
  action names, and validation branches consistent.
- Needs continued practice writing precise error messages for each tool branch.
- SDK vs direct HTTP API distinction has been introduced but is not yet deeply
  practiced.

## Next Session Plan

1. Read `stage1.py` in four blocks: tools, `fake_model`, `agent_loop`, run entry.
2. Ask the learner to explain the message flow:
   `user -> fake_model -> tool_call -> tool result -> final_answer`.
3. Add one small feature, preferably `multiply(a, b)`.
4. Run `python stage1.py` and inspect output.
5. Mark the Stage 1 artifact complete only if the learner can explain the loop and
   the modified code runs.

## Session Log

### 2026-06-21 - Stage 1 continuation assessment

- Evidence: correctly explained that a tool result becomes the model's next
  observation; correctly described the user -> model -> tool -> result -> answer
  flow; correctly identified the purpose of the tool registry; wrote the core
  multiplication function body.
- Gaps: needs to distinguish Python dictionaries from lists (`tools["multiply"] =
  multiply`, not `tools.append(...)`) and keep identifiers consistently spelled.
- Next task: register `multiply` in the existing Stage 1 tool registry, then run
  a multiply request through the loop.

### 2026-06-21 - Stage 1 artifact verification

- Evidence: independently modified `stage1.py` to define `multiply(a, b)`,
  register it in `tools`, make `fake_model` return `action: "multiply"` for a
  `6 times 7` request, validate the arguments, and run the program successfully.
- Run result: `python stage1.py` produced `Final answer: 30` and
  `Final answer: 42`.
- Understanding demonstrated: explained that the tool name must stay consistent
  because it is passed through the model output and `agent_loop` dispatch path,
  not merely used as a local variable; if inconsistent, the tool cannot be
  recognized or validated correctly.
- Remaining correction: the `multiply` validation branch still says `add` in its
  error messages; normal behavior works, but diagnostics should name the actual
  tool.
- Status: Stage 1 artifact complete at the introductory level.
- Next task: begin Stage 2 assessment before studying search/RAG and memory.

### 2026-06-21 - Workspace reorganization

- Moved Stage 0-1 notes from `notes.md` to `notes/notes01.md`.
- Created `notes/notes2.md` as the Stage 2 note file.
- Moved Stage 1 code from `stage1.py` to `codes/stage1.py`.
- Updated `AGENTS.md` so future sessions use `notes/` for learning notes and
  `codes/` for practice code.
