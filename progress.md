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

### 2026-06-22 - Stage 2 coding exercise: hybrid retrieval (partial verification)

- Evidence: `retrieve_hybrid("faulty item one week later")` returned
  `quality_exception` first and `refund_deadline` second; each result preserved
  source, lexical score, and semantic score.
- Strength: the two stable sorts correctly produce semantic-score descending order
  with lexical-score descending tie-breaking.
- Remaining task: change `main()` to call the required natural-language query and
  run `python -B codes/stage2_retrieval.py` to verify the normal entry point.

### 2026-06-22 - Stage 2 coding exercise: hybrid retrieval (complete)

- Verification: normal entry point `python -B codes/stage2_retrieval.py` used
  `faulty item one week later` and returned `quality_exception` first, followed
  by `refund_deadline`, with source, lexical score, and semantic score preserved.
- Status: completed the deterministic hybrid-retrieval exercise. Semantic scores
  are deliberately simulated; real embeddings have not yet been integrated.
- Minor cleanup noted: stale TODO comments and an unnecessary
  `NotImplementedError` handler remain from the earlier scaffold, but do not
  affect the verified behavior.
- Next task: decide what a real embedding API must return and how it replaces the
  simulated semantic-score mapping without changing retrieval boundaries,
  citations, or failure handling.

### 2026-06-22 - Stage 2 verification: scores are not evidence

- Evidence: explained that retrieved original text and sources are required for
  verifiability and accuracy, rather than relying only on a semantic score.
- Status: understands that ranking selects candidates, while retrieved evidence
  and citations constrain the final answer.
- Next task: select an embedding implementation environment, then define the
  provider-neutral API boundary before integrating it.

### 2026-06-23 - Stage 2 coding exercise: offline TF-IDF retrieval

- Artifact: `codes/stage2_tfidf_retrieval.py`.
- Evidence: independently implemented query transformation, cosine-similarity
  scoring, index-aligned `zip(CHUNKS, scores)` metadata retrieval, score filtering,
  and descending sorting.
- Verification: the exact query returned `quality_exception` first with score
  0.513; the paraphrase query returned the controlled empty-result message.
- Understanding demonstrated: explained how chunk text creates the vector matrix
  while the original chunk records preserve IDs and sources; reviewed the roles of
  `.flatten()` and `zip()`.
- Status: completed the offline TF-IDF baseline. It remains lexical retrieval,
  not semantic embedding retrieval.
- Next task: choose a true local semantic embedding model or a remote embedding
  API, then replace the simulated semantic scores with real vector similarities.

### 2026-06-23 - Stage 2 local semantic-embedding environment

- Updated code comments to explain why a query reuses `transform()` rather than
  refitting the vectorizer, why cosine results use `.flatten()`, and how `zip()`
  keeps scores aligned with chunk metadata.
- Updated `AGENTS.md`: missing learning dependencies must be identified with their
  purpose and target interpreter, then installed only after user approval.
- Installed `sentence-transformers 5.6.0` into the `D:\ana\python.exe` user
  environment.
- Blocker: importing `sentence-transformers` fails because installed `torch
  2.12.1` cannot initialize `c10.dll` (`WinError 1114`). No model weights were
  downloaded.
- Next task: obtain approval to replace the broken PyTorch runtime with a CPU
  build, verify `import torch`, then download and test a local embedding model.

### 2026-06-23 - Project virtual environment

- Created `.venv` from `D:\ana\python.exe`; verified
  `.venv\Scripts\python.exe` uses Python 3.11.7.
- The environment is project-local and already ignored by `.gitignore`, so it
  does not replace or modify the broken global PyTorch installation.
- Next task: install a CPU-compatible PyTorch runtime and sentence-transformers
  into `.venv`, verify imports, then download a local embedding model.

### 2026-06-23 - Local embedding runtime installation

- Installed `torch 2.12.1+cpu` into the project `.venv` from the PyTorch CPU
  wheel index. This did not alter the global Python environment.
- Blocker: `import torch` still fails with `WinError 1114` while loading
  `c10.dll`. Adding `D:\ana\Library\bin` to `PATH` did not resolve it, and the
  Windows VC++ runtime DLLs are present.
- `sentence-transformers` was not installed into `.venv`, and no model weights
  were downloaded because the required PyTorch runtime is not usable.
- Next decision: try a different CPU PyTorch build inside `.venv`, or use a
  torch-free local ONNX embedding runtime.

### 2026-06-23 - Conda isolation check

- Ran `conda deactivate` and confirmed `CONDA_PREFIX` was empty before invoking
  `.venv\Scripts\python.exe`.
- Result: `import torch` still failed at `c10.dll` with `WinError 1114`.
- Conclusion: the current failure is not caused by the active Conda base
  environment; proceed with a torch-free local embedding route or deeper Windows
  DLL diagnostics.

### 2026-06-23 - ONNX local embedding runtime check

- Installed `fastembed 0.8.0` and `onnxruntime 1.27.0` into `.venv` as a
  torch-free local embedding route.
- Blocker: importing `onnxruntime` fails while loading
  `onnxruntime_pybind11_state` with a DLL initialization error.
- Conclusion: both PyTorch and ONNX Runtime native backends fail in the current
  `.venv`; model download and real local embedding integration are deferred.
- Next decision: create an isolated environment from the separate
  `D:\python10\python.exe` interpreter, or defer local semantic embedding and
  continue with the verified TF-IDF/hybrid exercises.

### 2026-06-23 - Python 3.10 ONNX environment

- Created `.venv-py310` from `D:\python10\python.exe` (Python 3.10.9).
- Installed and verified `onnxruntime 1.23.2`; unlike the Anaconda-derived
  `.venv`, it imports successfully.
- Installed and verified `fastembed 0.8.0` in `.venv-py310`.
- Attempted to download and load `BAAI/bge-small-en-v1.5`; the model acquisition
  did not complete within five minutes, so no embedding vector was produced.
- Next task: choose a reachable model-download source or manually provide local
  model files, then rerun the real embedding verification.

### 2026-06-23 - Model mirror download attempt

- Confirmed FastEmbed downloads Hugging Face models through
  `snapshot_download`, which honors `HF_ENDPOINT`.
- Attempted a process-local `HF_ENDPOINT=https://hf-mirror.com` configuration
  with Xet transfer disabled. The environment's automatic risk review stopped
  the download because the network stream disconnected during review.
- No alternative download route was attempted. Next step requires renewed explicit
  user approval for the mirror download, or user-provided local model files.

### 2026-06-23 - Official model download and ONNX load stability

- Used a fresh FastEmbed cache directory to avoid an incomplete prior snapshot;
  Hugging Face official download of `BAAI/bge-small-en-v1.5` completed.
- Initial real encoding succeeded and produced a 384-dimensional `float32`
  embedding vector.
- Subsequent offline model initialization failed twice with ONNX Runtime
  `bad allocation`, including a single-thread CPU attempt.
- Status: model files are downloaded and the embedding path has succeeded once,
  but repeated ONNX initialization is not yet stable. Do not treat the local
  runtime as a reliable project dependency until the allocation failure is
  understood or avoided.

### 2026-06-23 - ONNX allocation stability resolution

- Diagnostics: approximately 6.4 GB of memory was available; the ONNX model file
  was complete at about 63 MB; direct ONNX Runtime model loading succeeded.
- Resolution: configured FastEmbed with `CPUExecutionProvider`, `threads=1`, and
  `enable_cpu_mem_arena=False`.
- Verification: three independent offline Python processes each initialized the
  model and returned a 384-dimensional embedding successfully.
- Status: the local ONNX embedding runtime is stable with the documented session
  settings. Next task: implement a small real-embedding retrieval exercise that
  uses this configuration and preserves chunk sources.

### 2026-06-23 - ONNX stability verification

- Evidence: explained that disabling the arena and limiting threads changes
  initialization/resource scheduling rather than model content, with performance
  as the expected trade-off.
- Status: understands the distinction between inference runtime configuration and
  embedding-model semantics.
- Next task: build the minimal real-embedding retrieval exercise using the stable
  FastEmbed configuration and source-preserving result records.

### 2026-06-23 - Stage 2 coding exercise: real ONNX embedding retrieval

- Artifact: `codes/stage2_onnx_retrieval.py`.
- Evidence: independently encoded document chunks and query with FastEmbed,
  corrected the query shape from `(1, 384)` to `(384,)`, implemented vectorized
  cosine similarity, paired scores with chunk metadata, and sorted results.
- Verification: for `faulty item one week later`, real model scores ranked
  `quality_exception` (0.701), `refund_deadline` (0.660), then `shipping`
  (0.560); all results retained source fields.
- Next task: add a relevance threshold or top-k policy so semantic ranking does
  not automatically send weak candidates to the answer stage.

### 2026-06-23 - Stage 2 verification: relevance threshold

- Evidence: explained that only sufficiently similar text should become final
  answer evidence, while low-similarity candidates should be excluded.
- Status: understands that ranking is relative ordering and a threshold defines a
  minimum evidence-relevance boundary.
- Next task: compare threshold and top-k policies, then add one explicit filter
  to the real embedding retrieval exercise.

### 2026-06-23 - Stage 2 exercise: threshold and top-k

- Evidence: correctly retained only the 0.701 candidate at a 0.70 threshold and
  identified that top-k alone can select low-relevance text.
- Correction: when no candidate passes a threshold, the default behavior is to
  report insufficient evidence; lowering the threshold requires an explicit,
  controlled fallback policy rather than an automatic attempt to force an answer.
- Next task: add `threshold` and `top_k` parameters to the real embedding
  retrieval function, then verify both a filtered result and an empty result.

### 2026-06-23 - Stage 2 coding exercise: real embedding filtering

- Evidence: added threshold filtering before appending candidates, sorted retained
  results, and capped output with `results[:top_k]`.
- Verification: `threshold=0.65`, `top_k=2` returned `quality_exception` and
  `refund_deadline` but excluded `shipping`; `threshold=0.75` returned an empty
  result and printed the controlled no-evidence message.
- Status: completed real embedding retrieval with source preservation, threshold
  filtering, and top-k capping.
- Minor improvements noted: add default parameter values to `retrieve()`, and
  cache document vectors instead of re-encoding them for each query.
- Next task: build an evidence-based answer formatter that includes retrieved
  source references and refuses to answer when retrieval is empty.

### 2026-06-23 - Stage 2 verification: filter-order reasoning

- Evidence: distinguished threshold as an absolute relevance boundary from top-k
  as a relative quantity cap, and noticed that the operation order can produce
  the same set in a simple single-score sorted list.
- Correction learned: write threshold filtering before top-k to make the policy
  explicit; order can matter once retrieval includes multiple scores, fusion, or
  reranking stages.
- Next task: build an evidence-based answer formatter that cites sources and
  refuses unsupported answers when retrieval is empty.

### 2026-06-23 - Stage 2 code review: evidence formatter (partial)

- Evidence: added a `format_evidence_answer()` function and preserved source
  fields in its intended result structure.
- Gaps: the function is annotated to return `str` but returns `None` or a list;
  it places `id` in the `text` field instead of the original chunk text; it is
  not called from `main()`; and empty retrieval must return a refusal string
  rather than only printing.
- Next task: return one evidence-only string containing original text and source
  citations, then call and print it for both non-empty and empty result sets.

### 2026-06-23 - Stage 2 code review: evidence formatter (string assembly)

- Evidence: corrected the empty-result branch to return a refusal string and
  invoked the formatter from `main()` for the retrieved result set.
- Gap: `{f"..."}` creates a one-item `set`, not a string, causing
  `"\n".join(lines)` to fail because every list item must be a string.
- Next task: append the formatted citation string directly, then rerun both the
  evidence and empty-result paths.

### 2026-06-23 - Stage 2 verification: evidence-based answer formatter

- Evidence: `codes/stage2_onnx_retrieval.py` ran successfully in `.venv-py310`.
  With `threshold=0.65`, it returned two original text excerpts with their
  `source` values; with `threshold=0.75`, it returned the explicit
  no-evidence refusal.
- Correction learned: `{f"..."}` creates a one-item `set`; append the f-string
  itself so that every `lines` element is a string and `"\n".join(lines)` works.
- Next task: explain why preserving `id` along with text and source can still be
  useful even though the current evidence answer displays only text and source.

### 2026-06-23 - Stage 2 check-in: retrieval-result identifiers

- Evidence: recognized that an `id` is useful in the retrieval workflow.
- Correction: `id` normally does not take part in embedding or cosine-similarity
  scoring. It is a stable identifier for locating a chunk, deduplicating results,
  recording logs, and fetching the same source fragment again.
- Next task: continue Stage 2 by separating retrieval output from the final
  answer step, and identify which fields each step needs.
## 2026-06-23 — Stage 2：检索输出结构与最终回答输入结构（诊断）

- 已确认：检索结果需要保留稳定 `id`、原文 `text` 与可核查出处 `source`；最终回答只应接收排序、阈值过滤后的证据，避免低分和调试数据干扰回答。
- 已确认：`score` 不必默认交给 LLM；保留它可支持后续路由或策略判断。无合格证据时必须进入明确的“证据不足”拒答路径。
- 待补强：区分 `text`（可作为事实依据的内容）与 `source`（该内容的出处）；将空检索结果建模为结构化状态，而不是仅一条自然语言提示。
- 下一任务：实现一个最小转换函数，将检索结果转换为最终回答输入，并验证正常与空结果两条路径。
