# Agent Learning Hub

一个面向 **Agent 工程实践与求职作品** 的个人学习工作区。

这里不再维护从 Stage 0 到 Stage 8 的线性课程，也不继续收集大而全的资源目录。新的方法是：选择一个真实问题，做出可运行的 Agent vertical slice，再用测试、trace、eval 和权限边界把它变可靠。

## 当前目标

- 方向：Agent 工程，优先真实工具调用、harness、MCP、Skills、评测与安全边界。
- 结果：完成一个别人能够 clean clone、运行、验证和理解的作品。
- 学习方式：项目驱动；已有证据的基础知识不重复摸底，只在项目暴露缺口时补齐。
- 当前状态与唯一下一步以 [`progress.md`](progress.md) 为准。

## 已有基础

| 能力 | 当前证据 |
| --- | --- |
| Agent loop 与工具边界 | 做过最小循环、工具注册、参数校验、最大步数和失败分支练习。 |
| 检索与证据 | 做过关键词、TF-IDF、embedding 检索，理解 chunk、source、citation、threshold、top-k 与证据不足拒答。 |
| 工程实践 | 在相关项目中实践过 MCP、OAuth、权限门禁、部署、CI、诊断与 Skill 打包。 |
| 当前缺口 | 尚缺一个在本仓库内可复现、带真实模型与工具、trace/eval/CI 的完整 Agent 项目。 |

2026 年 6 月的逐课笔记、toy scripts、静态学习页面和本机虚拟环境已退出活跃分支。它们仍完整保留在 [legacy snapshot `c226e51`](https://github.com/littlemuu/Agent-Learning-Hub/tree/c226e51dc07cf428e49d284a86d1ba898ccfa10e) 中。

## Fast Track

### M1 — Real Agent Vertical Slice

目标：完成一条真实、可观察的端到端路径。

- 使用真实 LLM，而不是硬编码 fake model。
- 接入 2–3 个职责清晰、输入输出严格的工具。
- 使用结构化状态表达成功、证据不足、工具失败和需要人工确认。
- 至少包含一次多步执行，并能解释每一步为什么发生。
- 从干净环境安装依赖后可以运行。

### M2 — Reliability

目标：从“能演示”推进到“可验证”。

- 为关键路径添加 timeout、有限重试、停止条件和权限边界。
- 保存可读 trace，能定位模型、工具、检索或状态层错误。
- 建立不少于 20 个固定 eval case，记录成功率和失败分类。
- 使用 pytest 和 CI 固定回归行为。

### M3 — Ship

目标：形成可以用于作品展示的完整项目。

- 提供 CLI、API 或 Web 入口中的一种。
- README 包含安装、配置、运行、示例、架构、限制与安全说明。
- 提供一段可复现 demo 和至少一个真实失败案例。
- 明确成本、延迟、数据边界和需要人工确认的操作。

## 推荐候选项目

### Internship Research Agent

围绕真实求职需求构建：读取公开岗位信息，结构化提取技能、地点、截止日期和工作方式；去重后按 Agent 工程方向与可持续工作负荷偏好排序，并为每个判断保留证据。

建议的第一版边界：

- 输入：用户偏好与一组公开岗位 URL 或结构化样本。
- 工具：获取公开页面、提取岗位字段、保存/读取已见岗位。
- 输出：强匹配列表、匹配理由、缺失信息和原始来源。
- 安全：不自动投递、不登录招聘账号、不绕过站点规则；任何外部写操作都需人工确认。
- Eval：字段提取、去重、排序、证据对应和“不足以判断”五类测试。

这是推荐候选，不代表已经选择。开始实作前先由学习者确认项目。

## 精选资料

只保留能直接服务当前项目的核心入口：

- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK — Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [Model Context Protocol](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- [Claude Code: Extend Claude Code](https://docs.anthropic.com/en/docs/claude-code/features-overview)

其他框架、论文和项目只在当前实现遇到明确问题时再查，不作为待读清单。

## 仓库约定

```text
README.md        当前方向、里程碑和验收标准
progress.md      当前能力证据、缺口和唯一下一任务
AGENTS.md        AI 协作者在本仓库中的工作规则
projects/        选定项目后创建；每个项目独立管理依赖、测试和说明
```

- 不提交虚拟环境、模型缓存、密钥、编辑器私有配置或生成产物。
- 新项目必须声明依赖，并能从 clean clone 运行。
- 代码、测试和可复现运行结果优先于文字进度；若冲突，应修正文档。
- 不为保持路线完整而制造无使用场景的 demo。

## Learning Principles

- Build first, then read deeper.
- Prefer small reliable agents over impressive demos.
- Use tools with strict schemas.
- Add evals before adding more agents.
- Trace important runs.
- Keep humans in the loop for risky actions.
- Respect platform rules, copyrights, and data access boundaries.

## Attribution

本仓库最初的 Agent 学习路线由 [陈思州](https://github.com/jjyaoao) 整理；当前版本在保留原始署名和 MIT License 的前提下，改造为个人项目驱动的学习工作区。
