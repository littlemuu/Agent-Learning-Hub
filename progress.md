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

- Current stage: Stage 1 - Build A Minimal Agent Loop.
- Stage 0: complete at the introductory level.
- Stage 1 checklist: complete at the introductory level.
- Stage 1 artifact: pending verification.
- Current file: `stage1.py` exists as a reference implementation and runs.
- Next task: review `stage1.py` section by section, then make a small change such
  as adding a `multiply` tool or changing the fake model input case.

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

## Current Gaps

- Needs more independent practice writing valid Python snippets with indentation
  and function syntax.
- Needs to explain `stage1.py` in their own words before marking the Stage 1
  artifact complete.
- Needs to modify the reference implementation, run it, and verify behavior.
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
