# Learning Progress

## Learner Profile

- Python: 能读懂、运行并修改小型练习代码；仍需要继续练习独立编写函数、缩进、返回值和断言。
- TypeScript: 暂无系统经验。
- HTTP API / JSON: 已理解基础 JSON、字典字段访问、`json.loads()` 与嵌套参数读取。
- Agent / RAG: 有项目接触经验，正在补齐底层机制：Agent loop、tool 调用、检索、证据、失败处理和记忆。
- 学习偏好：不重复完整基础摸底；喜欢小型可运行练习，先自己写核心代码，再由助手检查、验证和纠正。

## Current Position

- Current stage: Stage 2 — Learn Tool Use, RAG, And Memory.
- Stage 0: introductory level complete.
- Stage 1: introductory level complete; artifact at `codes/stage1.py`.
- Stage 2 notes: `notes/notes2.md`.
- Current main Stage 2 code:
  - `codes/stage2_retrieval.py`
  - `codes/stage2_tfidf_retrieval.py`
  - `codes/stage2_onnx_retrieval.py`
- Current Python environment for real local embedding: `.venv-py310`.
- Next task: 将 `answer_input` 作为最终回答函数的唯一输入，实现 `generate_answer(answer_input: dict) -> str`，根据 `status` 分支回答或拒答。

## Completed Roadmap Progress

### Stage 0

- 区分了 chatbot、workflow、Agent、multi-agent。
- 理解了 `observe -> think/decide -> act -> observe`。
- 理解了什么时候不适合使用 Agent。
- 阅读并讨论过 Anthropic《Building effective agents》和 OpenAI agents 实践指南。

### Stage 1

- 使用过 LLM API 做普通对话。
- 学习了结构化 JSON 输出。
- 实现了简单工具函数、工具注册表、JSON tool call 解析和工具结果回传。
- 理解 `max_steps`、timeout、未知工具、参数缺失、类型错误和非法 JSON 的基础处理。
- Artifact: `codes/stage1.py` 可运行，包含 `add` 和 `multiply` 路径。

### Stage 2 — completed so far

- 理解最小 RAG 流程：`ingest -> chunk -> embed -> retrieve -> answer with citations`。
- 理解 chunk 边界、chunk size、overlap、metadata、source 与 citation 的作用。
- 区分短期上下文、session memory、long-term memory；知道不应保存不确定或敏感的推断性个人信息。
- 理解工具失败、timeout、空检索和低相关检索的区别；默认不编造、不无限重试。
- 实现并验证了：
  - 关键词检索；
  - 模拟混合检索；
  - TF-IDF 检索；
  - FastEmbed + ONNX 的真实本地 embedding 检索；
  - 余弦相似度；
  - `threshold` 与 `top_k`；
  - 证据回答格式化；
  - 检索输出到最终回答输入的结构转换。

## Current Stage 2 Understanding

- `id` 是 chunk 的稳定标识，用于定位、去重、日志和再次取回内容；不参与 embedding 相似度计算。
- `text` 是可作为事实依据的原文片段。
- `source` 是可核查出处，不等同于证据本身；证据内容主要来自 `text`。
- 检索输出可以包含内部字段，如 `semantic_score`，用于排序、过滤、调试和路由。
- 最终回答输入应更窄：默认只交给 LLM `question`、`status` 和包含 `id/text/source` 的 `evidence`。
- 不默认传 `semantic_score`，因为它是检索阶段的中间产物；放进最终回答输入通常冗余，也可能干扰回答。
- 空检索应建模为结构化状态，例如 `status="insufficient_evidence"` 与 `evidence=[]`，而不是假装正常回答。
- `assert` 可用于检查结构边界，例如最终回答输入不包含 `semantic_score`，空结果 evidence 为空。

## Current Artifacts And Verification

- `codes/stage2_onnx_retrieval.py`
  - 使用 `BAAI/bge-small-en-v1.5` + FastEmbed + ONNX Runtime。
  - 稳定配置：`CPUExecutionProvider`、`threads=1`、`enable_cpu_mem_arena=False`。
  - `.venv-py310` 中已验证可运行。
  - `threshold=0.65`, `top_k=2` 返回：
    - `quality_exception` score ≈ 0.701
    - `refund_deadline` score ≈ 0.660
  - `threshold=0.75` 返回空结果并拒答。
  - `build_answer_input()` 已验证：
    - 非空结果返回 `status="ready"` 和不含 `semantic_score` 的 evidence。
    - 空结果返回 `status="insufficient_evidence"` 和 `evidence=[]`。

## Remaining Gaps

- 继续练习独立写小函数、显式 `return`、格式化字符串和断言。
- 继续练习把“检索阶段结构”和“最终回答阶段结构”分开设计。
- 已将最终回答生成改为只依赖 `answer_input`；下一步需要校验 evidence 结构，例如缺少 `text/source` 时如何失败。
- Stage 2 还未整体完成；README Stage 2 复选框不要提前勾选。

## Compact Timeline

- 2026-06-21: 完成 Stage 1 入门 artifact；进入 Stage 2。
- 2026-06-21: 学习 RAG 最小流程、chunk、metadata、citation、memory scopes 和 failure handling。
- 2026-06-21: 实现本地关键词检索原型 `codes/stage2_retrieval.py`。
- 2026-06-22: 完成模拟混合检索，保留 lexical / semantic scores 与 source。
- 2026-06-23: 完成 TF-IDF 检索基线 `codes/stage2_tfidf_retrieval.py`。
- 2026-06-23: 建立 `.venv-py310`，解决 ONNX Runtime 稳定性问题，完成真实本地 embedding 检索。
- 2026-06-23: 完成阈值、top-k、证据回答格式化和空结果拒答。
- 2026-06-26: 完成 `build_answer_input()`，明确检索输出结构与最终回答输入结构的边界。
- 2026-06-26: 完成 `generate_answer(answer_input)` 练习；函数只依赖最终回答输入，根据 `status` 分支输出证据答案或证据不足拒答。脚本已运行通过。
- 2026-06-26: 完成未知 `status` 错误处理；`weird_status` 会触发 `ValueError`。下一步：校验 evidence 字段缺失或证据项缺少 `text/source` 的情况。
- 2026-06-26: 验证理解：能说明未知 `status` 可能来自程序运行或上游结构错误，不应误判为证据不足；抛错有助于定位真正问题来源。
- 2026-06-26: 验证理解：能说明 `status="ready"` 与 `evidence=[]` 是结构矛盾，因为 ready 表示已有证据支持回答；这种情况应报错而不是返回空字符串或拒答。
- 2026-06-26: 完成 `ready` 状态下的空 evidence 校验；正常路径仍运行通过，`status="ready"` 且 `evidence=[]` 会触发 `ValueError`。
- 2026-06-26: 验证理解：能说明 ready 状态下的证据项缺少 `text` 应报错，因为没有原文证据就无法组织可靠回答。
- 2026-06-26: 完成 evidence 字段校验；缺少 `text` 或 `source` 的证据项都会触发 `ValueError`，正常回答路径仍运行通过。
- 2026-06-26: 完成接口收口；已删除旧 `format_evidence_answer()`，`main()` 只保留 `retrieve -> build_answer_input -> generate_answer` 路径，脚本运行通过。
- 2026-06-26: 完成 `run_answer_tests()` 自测函数；覆盖正常回答、证据不足、未知 status、ready 空 evidence、缺少 `text/source` 五类情况。脚本运行通过并输出 `answer tests passed`。
- 2026-06-27: 进入索引复用练习；能说明 `query_vector` 随用户输入变化不能复用，选择 `prepare_documents()` 作为文档侧索引构建函数名。需修正理解：连续查询时最昂贵的重复步骤是重新 embedding 全部文档，而不只是解析 document。
- 2026-06-27: 重新下载 `BAAI/bge-small-en-v1.5` 到 TEMP FastEmbed 缓存，验证可生成 384 维向量；`prepare_documents()` + `retrieve_from_index()` 路径运行通过，两次查询复用同一个文档索引并输出 `answer tests passed`。
- 2026-06-27: 完成索引复用路径收口；统一索引字段名为 `document_vectors`，删除旧 `retrieve()`，文件中只保留 `prepare_documents()` + `retrieve_from_index()` 检索路径。脚本运行通过。
- 2026-06-27: 检索层自测诊断：能说明 `document_vectors` 行数必须与 `CHUNKS` 对齐，排序异常可能来自分数计算、索引错位或 embedding/阈值变化；检索测试应早于回答测试，因为检索证据错误时不应继续组织答案。
