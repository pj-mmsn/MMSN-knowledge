# Wiki Schema — MMSN 知识库

> 本知识库的约定、标签体系和页面规则。所有 LLM 辅助操作以此为准。

---

## 领域

**Java 后端开发 + AI Agent 技术**，双线并进。Python 作为 AI 主力语言辅助线。

## 目录结构（PARA）

```
E:\知识库\
├── 01-Projects/       🟢 活跃项目（有目标、进行中）
├── 02-Areas/          🔵 持续积累的技术领域（能力圈）
│   ├── AI与Agent/      Agent理论 → 框架 → 运维
│   ├── Java/           基础/并发/JVM/数据库/框架
│   └── Python/         Java工程师视角速成
├── 03-Resources/      🟡 外部参考资料（只读）
├── 04-Archives/       ⚫ 已完成的项目（经验可复用）
├── 05-经验日志/        📝 踩坑记录
├── SCHEMA.md           📋 本文件：约定与规范
├── index.md            📇 总索引
└── log.md              📜 操作日志
```

---

## Frontmatter 规范

每篇笔记以 YAML frontmatter 开头。**必填字段**用 🔴 标记。

```yaml
---
title: 页面标题           # 🔴 必填
created: YYYY-MM-DD      # 🔴 必填 — 首次创建日期
updated: YYYY-MM-DD      # 🔴 必填 — 最后修改日期
tags: [AI, Agent, 概念入门]  # 🔴 必填 — 从下方标签体系中选择
type: area | project | resource | archive | log  # 🔴 必填 — PARA 类型
difficulty: 基础 | 进阶 | 深入  # 可选 — 02-Areas 使用
sources: []              # 可选 — 引用来源列表
confidence: high | medium | low  # 可选 — 观点置信度
contested: true          # 可选 — 标记有争议的内容
contradictions: [slug]   # 可选 — 与此篇矛盾的页面
---
```

### 字段说明

- **sources**: 引用来源数组，格式 `[filename.md]` 或 `[URL]`。跨 3+ 来源的页面建议在段落末尾加 `^[source.md]` 标记。
- **confidence**: 仅对观点/推断类内容使用。有交叉验证的设为 `high`，单一来源设为 `medium`，猜测设为 `low`。
- **contested / contradictions**: 当收录了互相矛盾的信息时，两篇都设为 `contested: true`，并在 `contradictions` 中互相引用。不要无声覆盖。
- **difficulty**: 仅 02-Areas 笔记使用，三选一：`基础`、`进阶`、`深入`。

---

## 标签体系

> 只能使用此列表中已有的标签。如需新增标签，先在这里添加，再使用。
> 共 **31 个标准标签**，覆盖 66 篇笔记。

### 技术域（7 个）
- `AI` — 人工智能通用
- `Agent` — 智能体：概念、架构、多Agent、工具调用、记忆系统
- `LLM` — 大语言模型：API调用、DeepSeek/OpenAI
- `RAG` — 检索增强生成：向量检索、Embedding、重排序
- `Prompt` — 提示工程：CoT、Few-shot、结构化输出
- `Java` — Java 语言与 JVM
- `Python` — Python 语言

### 框架与工具（9 个）
- `LangChain` — LangChain / LangChain4j
- `LangGraph` — LangGraph 状态机框架
- `CrewAI` — CrewAI 多Agent框架
- `AutoGen` — AutoGen 多Agent框架
- `Dify` — Dify 低代码Agent平台
- `Spring` — Spring / Spring AI / Spring Boot
- `向量数据库` — Chroma、FAISS、Milvus、JVector
- `API` — API 设计、调用、端点
- `工具` — IDE、环境搭建、效率工具

### 技术子域（7 个）
- `并发` — 多线程、锁、JMM、线程池
- `集合` — 数据结构与集合框架
- `JVM` — 内存、GC、类加载
- `数据库` — MySQL/Redis 相关
- `框架` — IoC/AOP/SPI 等框架机制
- `分布式` — CAP、BASE、一致性
- `部署` — Docker、FastAPI、监控

### 工程实践（5 个）
- `架构` — 系统设计、架构模式、企业级设计
- `概念入门` — 入门级概念、基础知识
- `实战` — 动手实践、踩坑经验、落地经验
- `排错` — debug、troubleshooting、优化
- `调研` — 技术选型、框架对比、生态概览

### 元信息（3 个）
- `学习方法` — 学习路径、转型指南
- `职业规划` — 职业发展方向
- `项目复盘` — 已完成项目的经验总结

---

## 页面创建与维护规则

### 何时创建新页面
- 一个实体/概念出现在 **2+ 条记录**中，或是一条记录的**核心主题**
- 新技术栈达到「能讲清楚原理 + 有代码示例」的程度
- 一条踩坑记录有独立成篇的价值（超过 30 行）

### 何时更新现有页面
- 信息是对已有主题的补充、修正或深化
- 同一技术栈的新版本更新
- 新的实践经验可归入已有分类

### 不创建页面的情况
- 一句话就能说清的概念（加到已有页面即可）
- 纯粹的文章转载（放入 `03-Resources/` 或直接记链接）
- 临时备忘录（用 05-经验日志 的一条记录即可）

### 页面长度控制
- 目标：一篇笔记 **30 秒可扫读完**（~200 行以内）
- 超过 200 行时，考虑拆分为主页面 + 子页面
- 拆分时主页面保留概述和索引，细节下沉到子页面

---

## 索引维护规则

- 每个目录必须有 `_index.md`
- 新页面创建后，必须同步更新所在目录的 `_index.md`
- 根目录 `index.md` 每周至少更新一次总览
- 索引中所有 `[[wikilink]]` 必须指向存在的文件

---

## 更新策略（冲突处理）

当新信息与已有内容矛盾时：
1. 检查时间戳 — 新信息通常取代旧信息
2. 如果确实矛盾且无法确定，**两边都保留**，标注日期和来源
3. 在两篇页面的 frontmatter 中都设 `contested: true`，用 `contradictions` 互相引用
4. 在下次 lint 时提醒人工裁决

---

## 日志规范

所有操作记录在 `log.md` 中，格式：

```markdown
## [YYYY-MM-DD] action | subject
- 创建页面：path/to/file.md
- 更新页面：path/to/file.md（修改内容摘要）
- 索引更新：path/to/_index.md
```

action 类型：`create | update | archive | delete | lint | ingest | query`

---

*最后更新: 2026-07-08*
