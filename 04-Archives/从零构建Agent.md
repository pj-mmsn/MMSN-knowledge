# 项目实战：从零构建 Agent

<!-- 从零手写 AI Agent 学习项目(ai-agent-starter + ai-agent-java)的构建测试经验 -->

---

## 2026-07-03 双项目联调测试 — Python + Java 双轨验证

**场景**：两个 AI Agent 项目构建完成后，完整运行自检，发现并修复了 5 个实际问题。

**测试结果**：
- Python 项目 (ai-agent-starter)：43/43 通过
- Java 项目 (ai-agent-java)：15/15 通过

---

### 发现与修复1: Python 语法错误 — 中文引号陷阱

**问题**：`app.py` 第 230 行报 `SyntaxError: invalid character`。

**根因**：内层 ASCII 双引号 `"记住我…"` 和外层 Python 双引号字符串 `"..." ` 冲突，Python 解析器把内层引号当成了字符串结束符。

**修复**：外层改用单引号 `'[dim]...对我说"记住我…"来添加。[/dim]'`

**教训**：写中英文混排的字符串时，优先用单引号做外层分隔符，避免和内层的中文/英文双引号冲突。

---

### 发现与修复2: Python 依赖缺失 — loguru 未安装

**问题**：`from src.agent import Agent` 失败，报 `No module named 'loguru'`。

**根因**：`agent/core.py` 使用 `loguru` 做日志，但 `pip install -r requirements.txt` 没有提前执行。

**修复**：`pip install -r requirements.txt` 安装全部依赖。

**教训**：项目 README 中的"快速开始"步骤必须包含 `pip install -r requirements.txt`，并且最好在 `__init__.py` 中做依赖检查给出友好提示。

---

### 发现与修复3: Java 编译配置 — --enable-preview vs Java 版本

**问题**：Maven 编译报错"源发行版 17 与 --enable-preview 一起使用时无效"。

**根因**：pom.xml 设置了 `<java.version>17</java.version>` 但编译参数带了 `--enable-preview`，而 `--enable-preview` 只在 Java 22+ 生效。

**修复**：移除 `--enable-preview` 配置（项目只用 Java 17 基础特性，不需要预览功能）。

**教训**：`--enable-preview` 需匹配 JDK 版本；学习项目应尽量用 LTS 版本（17/21），避免预览特性。

---

### 发现与修复4: Java Nashorn 引擎移除 — JDK 15+ 不能用 ScriptEngine

**问题**：`Calculator.java` 执行 `2+3*4` 报错"JavaScript 引擎不可用"。

**根因**：代码使用 `javax.script.ScriptEngineManager` 调用 Nashorn JS 引擎求值表达式，但 Nashorn 在 JDK 15 中被标记 deprecated，JDK 17+ 彻底移除。

**修复**：替换为手写递归下降解析器（parseAddSub → parseMulDiv → parsePower → parseAtom），支持 + - * / ** () 和 abs/round/sqrt 函数。约 80 行纯 Java，零外部依赖。

**教训**：
1. 不要依赖 JDK 内置的 Nashorn 引擎做表达式求值，JDK 版本兼容性太差
2. 递归下降解析器是实现"安全表达式求值"的推荐方案（也可引入 exp4j 等轻量库）
3. Python 版用受限 `eval()` 足够，Java 版必须自己写解析器

---

### 发现与修复5: Java 幂运算解析 — `**` 被误认为乘法

**问题**：`2**10` 计算失败，报"For input string: '*10'"。

**根因**：递归下降解析器 `parseMulDiv` 方法在遍历字符时先匹配到 `*`，把 `2**10` 误拆为 `2 * (*10)`，导致错误。

**修复**：在 `parseMulDiv` 中增加前后检查——当前 `*` 的前面或后面也是 `*` 时，跳过（留给 `parsePower` 处理）：
```java
if (c == '*' && (expr.charAt(i-1) == '*' || expr.charAt(i+1) == '*')) continue;
```

**教训**：递归下降解析器中，运算符优先级的处理顺序是：AddSub→MulDiv→Power→Atom。高级运算符（**）可能包含低级运算符字符（*），必须做前向/后向检查。

---

### 发现与修复6: Maven 依赖源 — Spring AI 不在 Maven Central

**问题**：`mvn compile` 时 Spring AI 依赖解析失败。

**根因**：Spring AI 发布在 Spring 自己的仓库（repo.spring.io），不在 Maven Central。

**修复**：
1. pom.xml 添加 `<repositories>` 指向 `https://repo.spring.io/milestone`
2. Spring AI 版本从 `1.0.0` 改为 `1.0.0-M6`（当前最新里程碑）
3. 将 Spring 相关依赖放入 Maven Profile（`-Pspring`），默认只编译核心模块

**教训**：新技术栈的 Maven 坐标要验证可用性；用 Maven Profile 隔离可选依赖，降低编译门槛。

---

## 2026-07-03 Java Agent 与 Python Agent 的关键差异

**场景**：双项目并行开发后的对比总结。

**结论**：

1. **异步模型**：Python 用 async/await（单线程事件循环），Java 用虚拟线程 + CompletableFuture（真正的并行）
2. **工具定义**：Python 用 ABC 抽象基类 + @abstractmethod，Java 用 interface（更轻量）
3. **依赖管理**：Python 的 pip install 一行搞定 90% 场景；Java 的 Maven 需要处理仓库源、版本兼容、Profile 切换
4. **JSON 处理**：Python 原生 dict/list 足够；Java 必须引入 Jackson 或 Gson
5. **跨平台**：Python 代码几乎无平台差异；Java 需要注意 JDK 版本差异（Nashorn 移除是典型案例）
6. **生产就绪**：Java 项目天然适合嵌入 Spring Boot 微服务；Python 项目适合独立部署或 FastAPI 服务

**相关**：
- `../02-Areas/AI与Agent/14-Java AI开发生态概览.md`
- `../02-Areas/AI与Agent/16-Java LLM API调用.md`
- 本经验笔记: 上文"安全设计清单"、"ReAct循环实现"

---

## 2026-07-03 E2E 测试设计 — Mock LLM 端到端验证 ReAct 循环

**场景**：没有真实 LLM API Key 的情况下，如何验证 Agent 的 ReAct 循环、工具调用、错误恢复等核心逻辑。

**方案**：构造 MockLLMClient，根据消息上下文返回预定义的工具调用和文本回答，模拟完整对话流程。

**测试覆盖的场景**：
1. 单工具调用（计算器）：用户问 1+1 → LLM 返回 calculator 工具调用 → 执行 → 观察结果 → 回答
2. 天气查询：用户问天气 → LLM 返回 weather 工具调用 → 执行 → 观察 → 回答
3. 多工具并行：用户问"计算 125×37 同时查上海天气" → LLM 返回两个工具调用 → 并行执行 → 回答
4. 错误恢复：用户问除零 → 工具返回错误 → LLM 看到错误后给出提示（不崩溃）

**Mock 设计关键原则**：
1. 根据**消息列表中最后一条消息的角色和内容**决定返回什么，不要用全局 `call_count` 做分支
2. 工具结果回来后（`last_is_tool`），Mock 应返回最终回答而非继续调工具
3. Reflection 检查时，Mock 应从 prompt 中提取原回答并原样返回

**结论**：Mock LLM 是 Agent 开发中不可或缺的测试工具，能在无 API Key 的情况下验证 90% 的核心逻辑。

**相关**：
- `../02-Areas/AI与Agent/01-Agent核心概念.md`
- `../02-Areas/AI与Agent/13-实战场景与解决方案.md`

---

## 2026-07-03 Reflection 机制的实践发现

**场景**：在项目中实现 Reflection（回答前自我检查），测试中发现一个设计陷阱。

**现象**：Agent 正常回答了"计算已完成"，但 Reflection 步骤调用 LLM 后，返回了一个完全不同的文本，覆盖了原始正确答案。

**根因**：Reflection 的 prompt 说"如果回答没问题，原样返回。如果有问题，返回修正后的回答"。但 LLM（包括 Mock）不总是严格"原样返回"——它倾向于重新措辞。

**解决方案**：
1. 【简单】让 Reflection 提取原回答并尽量保持原文
2. 【严格】用单独的 Reviewer 模型做"通过/不通过"二进制判断，而不是修改回答
3. 【折中】Reflection 只检查事实错误，不重写风格

**教训**：自我检查机制虽然能提升质量，但必须谨慎设计——不能让 Reflection 变成"瞎改"。

**相关**：
- `../02-Areas/AI与Agent/02-规划与推理.md` (Reflection 一节)
- `../02-Areas/AI与Agent/13-实战场景与解决方案.md`


**场景**：为学习 AI Agent 开发设计一个从零手写的实战项目，需要兼顾"渐进式学习"和"工程化组织"。

**结论**：

1. **渐进式学习路径**：按 Agent 的五大核心组件分层组织代码，每个模块既是独立可用的组件，又是学习的一个"课程"：
   - `src/llm/` → Lesson 1: LLM 基础调用
   - `src/memory/` → Lesson 2: 记忆系统（短期+长期）
   - `src/tools/` → Lesson 3: 工具系统（Function Calling）
   - `src/agent/` → Lesson 4: ReAct 核心循环（灵魂）
   - `src/cli/` → Lesson 5: CLI 交互界面

2. **examples/ 与 src/ 的关系**：examples 是"教科书"，src 是"源码集"。examples 按难度编号（01~06），从 30 行的 Hello LLM 到完整的 Agent 逐步叠加。每个 example 顶部有明确的学习目标说明。

3. **学习文档放在 docs/**：不把原理写到代码注释里（代码注释只写"为什么这么写"），原理放 docs/ 下的 Markdown 文件。

4. **配置集中管理**：用 `config.py` + `.env` 两层配置。config.py 用 dataclass 管理类型安全的静态配置，.env 管理敏感信息（API Key）。

**关键结构**：
```
ai-agent-starter/
├── config.py           # 全局配置（dataclass）
├── .env.example        # 环境变量模板
├── src/                # 核心源码（每个子模块是一个 Lesson）
│   ├── llm/client.py   # API 封装
│   ├── memory/         # 短期+长期+持久化
│   ├── tools/          # 基类+注册+5个工具
│   ├── agent/core.py   # ⭐ ReAct 循环
│   └── cli/app.py      # 交互界面
├── examples/           # 6 个渐进式练习（01-06）
├── tests/              # 单元测试
└── docs/               # 学习文档
```

**相关**：
- `../02-Areas/AI与Agent/02-规划与推理.md` (ReAct 模式)
- `../02-Areas/AI与Agent/01-Agent核心概念.md`
- `../02-Areas/AI与Agent/12-学习路径与转型指南.md`

---

## 2026-07-03 ReAct 循环实现 — 核心就 30 行代码

**场景**：从零实现 Agent 的 ReAct 主循环 `_react_loop`，理解了所有 Agent 框架的底层逻辑。

**结论**：

1. **ReAct 的本质**：在一个 `while` 循环中反复执行"思考→行动→观察"，直到 LLM 认为可以回答。去掉注释后核心逻辑不到 30 行。

2. **为什么需要循环**：一个工具调用通常不够。例如"比较北京和上海的房价"需要分头查两个城市，再综合分析。

3. **MAX_STEPS 是生命线**：不设上限会陷入无限循环（LLM 可能反复调用同一工具），经验值 5-10 步足够覆盖绝大多数场景。

4. **工具结果要作为"观察"加入消息**：LLM 没有记忆，必须把所有中间结果都放在消息列表里，它才能在下一轮"看到"。

5. **并行执行优于串行**：多个独立工具用 `asyncio.gather` 同时发出，比逐个等待快 2-3 倍。

6. **错误即信息**：工具执行失败 → 错误信息作为观察返回 → LLM 看到错误后可能调整策略重试或换工具。这是 ReAct 的自纠错能力。

**关键代码**：
```python
async def _react_loop(messages, tools_schema):
    step = 0
    while step < MAX_STEPS:
        step += 1
        response = await llm.chat(messages, tools=tools_schema)

        if not response.has_tool_calls:
            return response.content  # 最终回答

        messages.append(assistant_msg_with_tool_calls)
        results = await registry.execute_all(response.tool_calls)  # 并行
        for r in results:
            messages.append(tool_result_as_message(r))
```

**相关**：
- `../02-Areas/AI与Agent/02-规划与推理.md` (ReAct 详解)
- `../02-Areas/AI与Agent/04-工具调用.md` (Function Calling)

---

## 2026-07-03 工具系统设计 — ABC 基类 + Registry 模式

**场景**：设计一个可扩展的工具系统，让 Agent 能使用计算器、搜索、天气、代码执行、文件操作 5 种工具。

**结论**：

1. **基类设计（ABC）**：每个工具必须实现三个接口：
   - `name` + `description`：给 LLM 看的"自我介绍"
   - `get_parameters_schema()`：JSON Schema 格式的参数说明（LLM 据此构造参数）
   - `execute(**kwargs)`：实际执行逻辑

2. **Registry 模式的价值**：工具注册中心做三件事：
   - `get_all_schemas()`：导出给 LLM 的 tools 参数
   - `execute(name, args)`：按名字执行工具
   - `execute_all(tool_calls)`：并行执行多个工具

3. **描述是工具的灵魂**：LLM 完全靠 `description` 和参数的 `description` 来决定是否调用。描述要写清"何时使用"+"何时不使用"，给出正反例。

4. **安全三原则**：
   - 代码执行：子进程隔离 + 超时限制（5秒）+ 禁用危险模块
   - 计算器：限制 eval 可用函数 + 危险关键词检测
   - 文件操作：限定工作目录 + 防路径穿越

**相关**：
- `../02-Areas/AI与Agent/04-工具调用.md`
- 本经验笔记: `常见问题记录.md#工具调错` (工具描述不佳导致调错)

---

## 2026-07-03 记忆系统设计 — 短期滑动窗口 + 长期用户画像

**场景**：实现 Agent 的记忆系统，既要记住当前对话上下文，又要跨会话记住用户信息。

**结论**：

1. **短期记忆（滑动窗口）**：
   - 保留最近 N 轮对话（经验值 10-20 轮）
   - 按"轮次"裁剪，而非按消息数——避免在工具调用链中间断开
   - System Prompt 始终保留在窗口最前面

2. **长期记忆（用户画像）**：
   - 存关键事实（名字、城市、偏好等键值对）
   - 每次对话时将画像注入 System Prompt，让 LLM "记得"用户
   - 用简单的 JSON 文件即可（学习阶段），生产可换 SQLite/向量库

3. **为什么 JSON 而不是数据库**：学习阶段追求简单可读，JSON 让人能直接打开看数据结构。生产环境再换（这是有意的设计取舍，不是疏忽）。

4. **对话摘要作为长期记忆的桥梁**：旧对话超出滑动窗口被丢弃前，用 LLM 生成摘要存入长期记忆，关键信息不丢失。

**相关**：
- `../02-Areas/AI与Agent/03-记忆系统.md`
- 本经验笔记: `常见问题记录.md#多轮对话忘记上下文`

---

## 2026-07-03 多模型兼容 — OpenAI 兼容接口统一接入

**场景**：项目需要支持 OpenAI、DeepSeek、智谱GLM、Moonshot 等多种 LLM，但不想写多套调用代码。

**结论**：

1. **几乎所有国产模型都兼容 OpenAI 接口格式**：只需改 `base_url` 和 `model` 两个参数。
2. **配置方式**：`.env` 文件存 API Key 和 Base URL，支持一键切换。
3. **常见配置速查**：

| 服务商 | LLM_BASE_URL | LLM_MODEL |
|--------|-------------|-----------|
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| 智谱GLM | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-flash` |
| Moonshot | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-turbo` |

**相关**：
- `../02-Areas/AI与Agent/16-Java LLM API调用.md`

---

## 2026-07-03 安全设计清单

**场景**：代码执行、文件操作、eval 计算都有安全风险，需要在学习项目中明确体现安全意识。

**结论**——三个必须做的安全措施：

1. **代码执行**：用 `asyncio.create_subprocess_exec` 在子进程中执行，设置 5 秒超时。绝不直接 `exec()` 用户代码在 Agent 进程中。

2. **计算器 eval**：用受限的 `__builtins__` 字典覆盖 eval 的全局命名空间，只暴露安全的数学函数。先检查危险关键词（`__`, `import`, `os`, `subprocess` 等）。

3. **文件操作**：设定工作目录（如 `data/`），用 `Path.resolve()` 后检查路径是否在工作目录内，防止 `../../etc/passwd` 路径穿越。

**相关**：
- `../02-Areas/AI与Agent/11-部署与运维.md`
- `../02-Areas/AI与Agent/13-实战场景与解决方案.md`

---

## 2026-07-03 语音交互 — Python vs Java 方案对比

**场景**：为两个 Agent 项目增加语音交互能力（语音输入 → Agent 处理 → 语音输出）。

**方案选择**：

| 环节 | Python | Java |
|------|--------|------|
| 语音识别 (STT) | `speech_recognition` 库（Google/CMU Sphinx） | 云端 ASR API（百度/阿里/腾讯） |
| 语音合成 (TTS) | `pyttsx3`（离线）+ `edge-tts`（在线微软免费） | 系统 TTS（PowerShell SAPI/macOS say/Linux espeak） |
| 推荐度 | ⭐⭐⭐⭐⭐ 开箱即用 | ⭐⭐ 生态不成熟，建议前后端分离 |

**结论**：
1. Python 语音生态碾压 Java——`speech_recognition` + `pyttsx3` 两行代码就能跑
2. Java 语音方案需要接入云端 ASR API，不适合纯本地场景
3. 生产推荐架构："浏览器录音 + 后端 Agent + 浏览器播放"（语言无关）
4. edge-tts 是免费且音质最好的 TTS 方案（微软 Azure 语音，免 API Key）

**相关**：
- `../02-Areas/AI与Agent/11-部署与运维.md`

---

## 2026-07-03 容器化部署 — Docker + docker-compose 最佳实践

**场景**：将两个 Agent 项目打包为 Docker 容器，支持一键部署。

**关键设计**：

1. **Python Dockerfile 要点**：
   - 基于 `python:3.12-slim`（轻量，约150MB）
   - 利用 Docker 缓存层：先 COPY requirements.txt 安装依赖，再 COPY 代码
   - 语音模式需 `--device /dev/snd` 挂载声卡

2. **Java Dockerfile 要点**：
   - **多阶段构建**：Maven 编译 → JRE 运行（最终镜像约200MB vs 单阶段700MB+）
   - 第一阶段用 `maven:3.9-eclipse-temurin-22`，第二阶段用 `eclipse-temurin:22-jre-alpine`
   - 先用 `mvn dependency:go-offline` 缓存依赖，再 COPY 源代码编译

3. **docker-compose 统一编排**：
   - Python Agent 暴露 8000 端口，Java Agent 暴露 8080 端口
   - 数据卷挂载 `data/` 和 `knowledge/` 目录持久化
   - `.env` 文件统一管理 API Key

4. **镜像体积**：Python ~310MB / Java 多阶段 ~260MB

**相关**：
- `../02-Areas/AI与Agent/11-部署与运维.md`
- `../02-Areas/AI与Agent/18-Java AI项目实战模式.md`

---

## 2026-07-03 学习项目设计的核心原则

**场景**：总结设计"教学型项目"（tutorial-first project）的核心原则。

**结论**：

1. **代码即教程**：注释写"为什么"（设计决策），不写"是什么"（语法解释）。文档写"是什么"和"怎么用"。

2. **渐进式叠加**：每个 Lesson 在前一个基础上增加一个新组件，而不是一次全堆出来。这样学习者每步都能独立运行和验证。

3. **可运行的示例优先于完备的测试**：学习项目中，`examples/` 比 `tests/` 更优先。每个 example 顶部写清学习目标。

4. **抽象要克制**：教学项目不要过度抽象。宁可代码重复一点，也不要引入学习者看不懂的间接层。

5. **可配置但不杂乱**：所有配置集中在一个 config.py，所有密钥在一个 .env，一个 .env.example 模板说明每个变量的含义。
