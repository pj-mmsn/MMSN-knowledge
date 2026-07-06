# Agent 框架选型 — 2026 年技术全景

<!-- 2026 年 AI Agent 框架/协议最新格局，结合项目实战的选型建议 -->

---

## 2026-07-06 2026 Agent 框架全景与项目选型

**场景**：在 AI 小说家项目中评估是否需要引入多 Agent 框架，调研了 2026 年最新技术格局。

### 核心结论：协议时代来了，但不是所有项目都需要

2026 年被认为是从"单体智能"迈向"多智能体协作"的分水岭。两大核心协议互补：

| 协议 | 发起方 | 连接对象 | 比喻 |
|------|--------|---------|------|
| **MCP** (Model Context Protocol) | Anthropic | 模型 ↔ 工具/数据 | AI 世界的"USB-C 接口" |
| **A2A** (Agent-to-Agent) | Google | Agent ↔ Agent | "智能体间的对讲机" |

### 四足鼎立的协议格局

| 协议 | 连接对象 | 层级 | 最佳场景 |
|------|---------|------|---------|
| MCP | Agent → 工具 | 工具层 | 工具标准化接入 |
| A2A | Agent → Agent | 智能体间层 | 跨厂商 Agent 协作 |
| ACP | Agent → Agent | 编排层 | 多模态、REST 团队 |
| ANP | Agent → Agent | 发现层 | 去中心化开放网络 |

### 2026 年最新多智能体架构模式

**三层解耦架构（生产级铁律）**：
```
感知层(Perception) → 决策层(Decision) → 执行层(Execution)
```

**五类编排模式**：
- Chain：顺序执行
- Route：条件路由
- Parallel：并行执行
- Orchestrator-Workers：主从分发
- Evaluator-Optimizer：评估优化循环

### 对小型项目的建议

**不需要多 Agent 框架的场景**（AI 小说家就属于这类）：
- 串行流水线任务（构思→大纲→写作）
- 不需要外部工具调用
- 上下文可以完全塞进 context window
- 单个开发者维护

**需要多 Agent 框架的场景**：
- Agent 之间需要并行协作
- 需要调用外部 API/工具
- 上下文超过 context window 需要向量检索
- 多个开发者独立维护不同 Agent

### 升级路径建议

```
当前：单体 Agent + Prompt 工程
  ↓ 需要调外部 API 时
  加 MCP：把视频生成/图片生成 API 封装为 MCP Tool
  ↓ 需要多 Agent 协作时
  加 A2A：导演 Agent、分镜 Agent、摄像师 Agent 通过 A2A 通信
  ↓ 上下文超出窗口时
  加 Vector DB：角色/伏笔/世界观做 RAG 检索
```

### 关键教训

1. **不要为了用框架而用框架**：现在的单体 Agent 已经工作得很好，引入框架只会增加复杂度
2. **协议比框架更持久**：MCP 和 A2A 是标准协议，10 年后可能还在；LangGraph/CrewAI 是具体实现，5 年后可能换掉
3. **先跑通再说**：先有一个能用的单体 Agent，再考虑拆分成多 Agent
