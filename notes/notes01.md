# 学习笔记

## Stage 1：最小 Agent Loop 练习补充

### 增加 `multiply` 工具

在最小 Agent loop 里，新增一个工具通常要同时修改三处：

- 工具函数：例如 `def multiply(a: int, b: int) -> int: return a * b`。
- 工具注册表：例如 `tools = {"add": add, "multiply": multiply}`。
- 模型结构化输出：`fake_model` 返回的 `action` 必须是 `"multiply"`，参数必须和函数签名一致，例如 `{"a": 6, "b": 7}`。

`tools` 是字典，不是列表。注册工具时使用键值映射，而不是 `append`：

```python
tools["multiply"] = multiply
```

或者直接写在字典字面量里：

```python
tools = {
    "add": add,
    "multiply": multiply,
}
```

### 工具名为什么必须一致

工具名不是普通的局部变量名，而是 Agent 控制流里的协议字段。模型输出 `action: "multiply"` 后，`agent_loop` 会拿这个字符串去 `tools` 字典中查找对应函数，并进入对应的参数检查分支。如果模型输出、工具注册表、参数检查分支中的名字不一致，就会出现未知工具、跳过正确校验或错误调用。

### 本次代码审查结论

`stage1.py` 的乘法路径已经跑通：`what is 6 times 7` 会经过 `fake_model -> tool_call -> multiply -> tool observation -> final_answer`，最终输出 `Final answer: 42`。

需要注意的小修正：`multiply` 的参数检查分支里，错误消息仍然写着 `add requires...` 和 `add arguments...`。这不会影响正常输入，但会影响排错。更好的写法是让错误消息说 `multiply requires arguments a and b`。

## Stage 0：理解什么是 Agent

### Chatbot、Workflow、Agent 与 Multi-Agent

- Chatbot 描述的是聊天交互形式，不代表内部一定使用 Agent。它可以只调用一次
  LLM，也可以由 workflow 或 Agent 驱动。
- Workflow 的执行步骤由程序预先规定，适合流程稳定、结果需要可预测的任务。
- Agent 会根据当前输入、上下文和工具结果，动态决定下一步行动，但仍然受到工具、
  权限、最大步数和停止条件等边界限制。
- Multi-Agent 将规划、执行、审查等职责分给多个 Agent。它是一种协调方案，不一定
  比单 Agent 更强；简单任务使用多个 Agent 反而会增加成本和复杂度。

### 什么时候不应该使用 Agent

如果任务可预测、流程稳定、普通代码或固定 workflow 能解决，通常不应使用 Agent。
Agent 会引入模型调用费用、延迟、不确定性、错误传播和更高的管理成本。

### Agent 基本循环

```text
observe -> think/decide -> act -> observe
```

- `observe`：接收用户请求、工具结果、报错或环境状态。
- `think/decide`：根据当前信息选择下一步。
- `act`：调用工具、执行代码、读取文件或输出回答。
- 工具执行后返回的新结果，会成为下一轮 `observe`。

示例：调用搜索工具是 `act`，搜索工具返回的结果是 `observe`。

## Anthropic：Building Effective Agents

### 总体原则

- 优先使用简单、可组合的模式，只在确实提升结果时增加复杂度。
- 能用直接代码清楚表达控制流时，不应为了使用框架而增加抽象层。
- 增加 Agent 或 LLM 调用通常会提高费用、延迟、限流风险和调试难度。

### Prompt Chaining（提示链）

将复杂任务拆成固定的连续步骤，每一步处理上一步的输出。

```text
职位信息 -> 提取结构化要求 -> 校验字段 -> 生成求职信 -> 格式检查 -> 内容核查
```

关键规则：

- 每一步都应有明确的输入和输出。
- 字数、字段是否存在等确定性规则优先用代码校验。
- 语义质量可以由 LLM 评估，但事实核查必须提供原始证据。
- 缺少必填字段时，应根据明确的失败或兜底策略处理，不能随意继续。

### Routing（路由）

先判断输入属于哪个类别，再进入对应的专用流程。例如退款、技术支持和售前咨询分别
进入不同 workflow。

低置信度时可以：

- 向用户追问；
- 使用安全的通用流程；
- 补充上下文后重新分类；
- 对敏感操作转人工处理。

路由错误可能导致答非所问、遗漏身份或权限检查、应用错误政策，甚至执行不应执行的
操作。

### Parallelization（并行化）

没有数据依赖、不会互相改变需求的任务可以并行。研究任务可表示为：

```text
分析题目 ->（官方资料、论文、新闻并行搜索）-> 汇总证据 -> 撰写报告
```

并行可以减少总耗时，但会增加 API 费用、限流风险、结果冲突和聚合复杂度。聚合器应
去重、检查证据、排列严重程度，并保留无法解决的分歧。

### Orchestrator-Workers（协调器-工作者）

协调器根据当前任务动态决定子任务的数量、类型和边界，再分配给 worker，并负责汇总
结果。worker 不应随意改变全局任务分配。

它与固定并行的区别：

- 固定并行：分支在代码中提前写死。
- Orchestrator-Workers：根据当前输入动态生成任务和 worker。

开放式搜索不能以“找到所有结果”作为停止条件。应设置可执行规则，例如：

- 候选必须仍在维护、支持 ASGI、最近两年有正式版本，并有公开性能或生产资料；
- 最多搜索五轮；
- 连续两轮没有新的合格候选时提前停止；
- 候选过多时按性能、维护状态、生态、文档、生产成熟度和需求匹配度统一评分。

处理 worker 冲突时，应要求提供证据并使用共同评价标准，而不是简单投票。

### Evaluator-Optimizer（评估器-优化器）

先生成一个候选结果，再由评估器按照明确标准检查质量，输出可执行的修改意见，然后把
原结果、评估意见和原始约束一起交给优化器修改。

它不是简单地让模型“再改好一点”，关键区别是：

- 评估标准要提前定义，例如岗位匹配度、事实准确性、格式正确性、语气是否合适；
- 评估输出要能驱动下一轮修改，不能只写笼统评价；
- 优化器必须看到原始需求、当前版本和评估反馈，避免改偏；
- 循环必须有停止条件，避免无意义迭代。

一个可执行的评估输出通常应包含：

- `criterion`：对应哪条评估标准；
- `passed` 或 `score`：是否通过或得分；
- `evidence`：判断依据，最好引用原文或输入资料；
- `issue`：具体问题；
- `revision_instruction`：下一轮应该如何修改。

`evidence` 很重要，因为它把评价绑定到输入材料或当前输出，能减少 evaluator 凭空挑错，
也能防止 optimizer 为了满足修改意见而编造不存在的经历、数据或事实。

常见停止条件：

- 达到质量阈值，例如所有必过项通过且总分超过目标；
- 连续多轮反馈重复或改进很小；
- 达到最大轮数、最大费用、最大时间等硬限制；
- evaluator 发现缺少必要输入，继续优化无法可靠完成。

### Workflow Pattern 不等于 Agent

Prompt chaining、routing、parallelization、orchestrator-workers 和
evaluator-optimizer 都可以是 workflow pattern。即使其中调用了 LLM，也不一定是 Agent。

关键区别在控制流：

- Workflow：程序预先规定步骤和分支，模型通常只完成某一步的生成、分类或评估；
- Agent：系统会根据观察、上下文、工具结果和停止条件，动态决定下一步要调用哪个工具、
  是否继续、是否换策略或是否结束。

因此，“用了 LLM”“用了多个步骤”“用了多个模型调用”都不是 Agent 的充分条件。是否存在
受边界约束的自主决策，才是更重要的判断依据。

### Stage 0 目标场景示例

目标场景：Web 项目运行出错时，让 Agent 协助排查。

这个场景适合 Agent，而不只是普通 workflow，因为错误原因不一定能预先确定。系统可能
需要先尝试运行项目，观察报错；再根据日志判断是依赖、配置、启动命令、端口、环境变量
还是代码问题；然后选择读取相关文件、审查最可能出错的代码，或停止并请求人工确认。

适合设置的边界：

- 工具范围限制在明确的 Python 工具文件或白名单命令内；
- 最大执行步数，例如 5 步；
- 涉及文件修改、安装依赖、删除文件等操作时需要人工确认；
- 超时、超过最大轮数、连续失败或缺少关键信息时停止。

### OpenAI Practical Guide 要点

普通 LLM 应用可以包含 LLM 调用或 workflow，但不一定让模型管理执行流程。Agent 的特点是
用模型根据上下文和中间结果动态决策、选择工具、推进任务，并在需要时停止或交还给用户。

更适合 Agent 的场景包括：

- 需要复杂决策，路径无法完全预先写死；
- 规则很多、经常变化，固定规则维护成本很高；
- 依赖非结构化数据，例如自然语言文档、日志、网页、邮件或代码。

一个 Agent 的基础组件通常包括：

- `model`：负责理解任务、推理和决策；
- `tools`：让 Agent 能搜索、读写文件、调用 API、执行代码等；
- `instructions`：定义目标、边界、工具使用规则、输出要求和停止条件。

Guardrails 很重要。以 Web 项目排错 Agent 为例，读取敏感环境配置、安装依赖、修改代码、
删除文件或执行有副作用的命令，都应该触发人工确认。

## 下次学习

进入 Stage 1：先学习结构化 JSON 输出，再实现最小 Python Agent loop。

## Stage 1：构建最小 Agent Loop

### JSON 和 Python dict

JSON 是模型和程序之间常用的结构化文本格式。模型返回的 JSON 通常先是字符串，例如：

```python
text = '{"action": "read_file", "arguments": {"path": "README.md"}}'
```

在 Python 中需要先解析：

```python
import json

data = json.loads(text)
```

解析后，JSON object 会变成 Python `dict`，JSON array 会变成 Python `list`。访问字段时：

```python
action = data["action"]
path = data["arguments"]["path"]
```

Agent 中常见的结构化动作格式：

```json
{
  "action": "tool_name",
  "arguments": {
    "name": "value"
  }
}
```

其中 `action` 表示模型想调用哪个工具，`arguments` 表示传给工具函数的参数。

### 工具分发和参数 schema

Agent 可以用一个工具表把模型输出的 `action` 映射到 Python 函数：

```python
def add(a: int, b: int) -> int:
    return a + b

tools = {"add": add}
```

如果模型输出：

```python
data = {
    "action": "add",
    "arguments": {"a": 10, "b": 20}
}
```

就可以分发执行：

```python
action = data["action"]
arguments = data["arguments"]
tool_func = tools[action]
result = tool_func(**arguments)
```

`tool_func(**{"a": 10, "b": 20})` 等价于 `add(a=10, b=20)`。

参数名必须和工具函数的参数 schema 对齐。`add(a, b)` 需要 `a` 和 `b`，不能传
`{"expression": "2 + 3"}`；`calculator(expression)` 才适合接收 `expression`。

### 为什么要求模型只输出 JSON

Agent 的下一步动作需要由程序解析。如果模型输出自然语言，例如“我会调用 add 工具，把
10 和 20 相加”，程序还要从文本里猜工具名和参数，容易出错。

因此，在简单 Agent 里可以先要求模型只输出固定 JSON：

```json
{
  "action": "add",
  "arguments": {
    "a": 10,
    "b": 20
  }
}
```

这样程序可以稳定读取：

```python
action = data["action"]
arguments = data["arguments"]
```

严格结构化输出是 tool dispatch 的前提。

### 工具结果反馈给模型

工具执行结果不会自动进入模型上下文。程序必须把工具结果作为新的 observation 发回模型，
模型才能基于结果决定是继续调用工具，还是返回最终答案。

示例：

```text
用户：10 + 20 等于多少？
模型：{"action": "add", "arguments": {"a": 10, "b": 20}}
程序：执行 add(10, 20)，得到 30
程序发回模型：工具 add 返回结果：30
模型：10 + 20 等于 30。
```

如果工具结果已经足够回答用户，就不需要继续调用工具；如果结果不足、工具失败或需要更多
信息，模型可以继续请求工具调用或停止并说明原因。

### Agent Loop 边界和错误处理

最小 Agent loop 必须有边界：

- `max_steps`：限制最多执行几轮，防止 Agent 无限循环；
- `timeout`：限制总耗时或单步耗时，防止工具或网络请求卡住；
- 错误处理：遇到坏输出、未知工具、参数错误或工具异常时返回可控错误，而不是崩溃。

常见错误处理：

```python
try:
    data = json.loads(model_output)
except json.JSONDecodeError:
    return "Error: model output is not valid JSON."
```

- 模型输出不是合法 JSON：返回 `model output is not valid JSON`；
- `action` 不在工具白名单：返回 `unknown or unauthorized tool`；
- `arguments` 缺少必填参数：返回 `missing required arguments`；
- 参数类型不对：返回 `arguments must be integers` 等具体信息；
- 工具内部报错，例如文件不存在：捕获异常并返回可控错误。

工具调用必须以程序注册的 `tools` 白名单为准，不能因为模型请求了危险工具就执行。
