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

### 2026-06-21 - Stage 2 diagnostic assessment

- Evidence: understands that RAG uses an external knowledge source; identified
  long-context cost and latency concerns; recognizes vector similarity retrieval
  at a high level; explained that citations reduce unsupported claims; rejects
  fabricating answers after a tool failure and would report the state to the user.
- Gaps: needs to distinguish the vector store from the complete RAG pipeline;
  needs to learn the role of chunking and how chunk quality affects retrieval;
  has not yet described an embedding/vector-store workflow independently.
- Next task: learn and explain the minimum RAG flow: ingest -> chunk -> embed ->
  retrieve -> answer with citations.

### 2026-06-21 - Stage 2 lesson: minimum RAG flow

- Evidence: completed the five-stage flow at a high level and correctly explained
  that oversized chunks make retrieval difficult.
- Corrections learned: ingest produces parsed text and metadata; retrieval must
  return the original relevant chunks rather than only similar vectors; the final
  answer requires the user question, retrieved chunks, and source metadata so it
  can cite evidence.
- Next task: compare chunking strategies with a small document and decide what
  chunk boundaries and metadata to keep.

### 2026-06-21 - Stage 2 verification: retrieval metadata

- Evidence: explained that without original text and source metadata, the LLM
  cannot see the retrieved evidence and the user cannot verify citations.
- Status: understands why vector storage must preserve original chunks and source
  metadata in addition to embeddings.

### 2026-06-21 - Stage 2 exercise: chunk boundaries

- Evidence: correctly identified the leave-approval chunk for a leave-related
  query and proposed useful source, page, and sentence-location metadata.
- Correction: initially split two adjacent scholarship sentences into separate
  chunks; learned that chunks should group a complete, single-topic semantic unit
  when size permits.
- Next task: verify the semantic-boundary rule, then learn the trade-off between
  chunk size and chunk overlap.

### 2026-06-21 - Stage 2 verification: semantic boundaries

- Evidence: explained that short, same-topic content should stay together while
  different-topic content should be split into a separate chunk.
- Status: understands that semantic coherence, not a fixed sentence count alone,
  determines chunk boundaries.
- Next task: learn the trade-off between chunk size and chunk overlap.

### 2026-06-21 - Stage 2 lesson: chunk size and overlap

- Evidence: explained that no overlap can retrieve only the main refund rule while
  omitting its exception; chose overlap for semantically continuous boundary
  content; identified that large overlap creates too many chunks.
- Correction learned: overlap is deliberately duplicated boundary text, not an
  accidental overlap already present in the source document.
- Next task: explain the specific storage, retrieval, and context-cost trade-off
  of large overlap, then move to retrieval quality and citations.

### 2026-06-21 - Stage 2 verification: overlap duplication cost

- Evidence: explained that more overlapped text creates more duplicate content and
  therefore more deduplication work in retrieval results.
- Status: understands the accuracy-versus-cost trade-off of chunk overlap.
- Next task: learn how retrieval result count, relevance thresholds, and citations
  constrain a RAG answer to available evidence.

### 2026-06-21 - Stage 2 lesson: retrieval quality and citations

- Evidence: selected both the default refund rule and its quality-issue exception;
  wrote an answer that correctly preserves “manual review” rather than promising
  a refund; stopped when retrieval contained no relevant evidence.
- Status: understands that `top_k` and relevance thresholds filter candidates, and
  that citations must support each material claim and its exceptions.
- Next task: verify why citing only the exception is insufficient, then compare
  short-term context with persistent memory.

### 2026-06-21 - Stage 2 verification: citation boundaries

- Evidence: identified that citing only the exception omits the default-rule
  boundary.
- Status: understands that evidence must cover both the main rule and material
  exceptions needed to interpret it.
- Next task: distinguish short-term context, session memory, and long-term memory.

### 2026-06-21 - Stage 2 exercise: memory scopes

- Evidence: correctly classified a retrieved document as short-term context, a
  prior tool timeout as session memory, and a persistent language preference as
  long-term memory.
- Correction: a time-limited instruction such as “today pause and continue
  tomorrow” is temporary session state, not a cross-session project convention or
  long-term memory.
- Next task: verify why time-limited instructions must expire, then learn a small
  policy for writing, retrieving, and deleting long-term memory.

### 2026-06-21 - Stage 2 verification: expiring state

- Evidence: explained that a relative-time instruction such as “tomorrow” changes
  meaning by the next session.
- Status: understands that stale time-bound state can cause an agent to act on an
  outdated plan.
- Next task: define a minimal policy for writing, retrieving, updating, and
  deleting long-term memory.

### 2026-06-21 - Stage 2 exercise: long-term memory policy

- Evidence: correctly chose to store an explicit durable language preference and
  rejected a time-bound learning plan as long-term memory.
- Corrections: verified project configuration is a mutable project fact rather
  than a user preference; an unverified inference about a user's employer must
  not be stored, especially because it may be sensitive personal information.
- Next task: verify the rejection rule for inferred personal data, then learn how
  an agent handles tool failures and empty retrieval results.

### 2026-06-21 - Stage 2 verification: inferred personal data

- Evidence: rejected an old inference as evidence and chose to ask the user only
  for information necessary to the current task.
- Status: understands that uncertain or sensitive inferred data should not become
  persistent memory.
- Next task: learn how to handle tool timeouts, errors, and empty retrieval
  results without fabricating an answer or retrying indefinitely.

### 2026-06-21 - Stage 2 exercise: tool failures and low-relevance retrieval

- Evidence: correctly rejected using low-relevance chunks as policy evidence.
- Corrections: a missing `query` is a deterministic parameter error that should
  first be repaired from available task context, not immediately reported as a
  lack of user information; repeated timeouts show that search did not complete,
  not that no results exist.
- Next task: verify the distinction between parameter repair and user follow-up,
  and between a timeout report and an empty-result report.

### 2026-06-21 - Stage 2 verification: bounded failure handling

- Evidence: chose to construct a missing query from the user request before
  retrying, with user follow-up only if the query cannot be determined; correctly
  reported repeated timeouts as an incomplete search that cannot be verified.
- Status: understands bounded retries, deterministic-error repair, empty-result
  handling, and evidence-preserving failure reports.
- Next task: build a small local retrieval exercise with fixed chunks, relevance
  scores, threshold filtering, and cited answers before using real embeddings.

### 2026-06-21 - Stage 2 coding exercise: local keyword retrieval

- Artifact: `codes/stage2_retrieval.py`.
- Evidence: independently implemented token-overlap scoring, score-based filtering,
  result records with `id/text/source/score`, and descending score sorting.
- Verification: `python -B codes/stage2_retrieval.py` returned
  `quality_exception` first with score 4; a query for `zzzz` returned
  `No reliable material found.`
- Status: completed a deterministic local retrieval prototype. This is preparation
  for RAG, not yet a real embedding-based retrieval implementation.
- Next task: inspect why keyword overlap can retrieve misleading chunks, then
  decide when embeddings or hybrid search are needed.

### 2026-06-21 - Stage 2 lesson: keyword, embedding, and hybrid retrieval

- Evidence: identified that keyword retrieval cannot infer synonym relationships;
  chose keyword retrieval for an exact source-path query and hybrid retrieval for
  a natural-language refund question.
- Status: understands the complementary roles of lexical precision and semantic
  recall, and why hybrid retrieval still needs filtering and citations.
- Next task: extend the local exercise with controlled lexical and semantic
  candidate scores, then apply thresholding and source-preserving fusion.

### 2026-06-21 - Stage 2 exercise: hybrid candidate selection

- Evidence: retained a high-semantic-score exception without keyword overlap,
  retained the semantically relevant default rule, and correctly retained an
  exact-path candidate through its keyword match.
- Correction learned: the default rule and exception should both be retained when
  together they define the answer boundary, not merely because both pass a score
  threshold.
- Next task: implement controlled lexical and semantic candidate scores in the
  local exercise, then filter and print source-preserving fused results.
