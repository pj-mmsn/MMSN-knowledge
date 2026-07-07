---
title: Java AI 开发生态概览
tags: [Java, AI, Spring AI, LangChain4j, 生态, 框架对比]
难度: 基础
---

# Java AI 开发生态概览

> **一句话**:Java 做 AI 开发不是"能不能"的问题，是"怎么选"的问题——Spring AI 是王者，LangChain4j 是备选，直接调 API 是兜底方案。

## 核心概念

### Python vs Java AI 开发生态对比

```mermaid
graph TB
    subgraph Python生态["Python AI 生态"]
        PY1["LangChain / LangGraph"]
        PY2["AutoGen / CrewAI"]
        PY3["Chroma / FAISS / Milvus"]
        PY4["FastAPI 部署"]
        PY5["OpenAI / DeepSeek SDK"]
    end

    subgraph Java生态["Java AI 生态"]
        J1["Spring AI ⭐"]
        J2["LangChain4j"]
        J3["Java HttpClient / OkHttp"]
        J4["Spring Boot 部署"]
        J5["JVector / Java ChromaClient"]
    end

    style Python生态 fill:#E3F2FD,stroke:#1976D2
    style Java生态 fill:#FFF9C4,stroke:#F9A825
    style J1 fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
```

| 维度 | Python | Java | 你的选择 |
|------|--------|------|---------|
| **框架成熟度** | LangChain 100k+ stars | Spring AI 15k+ stars（增长最快） | 双修 |
| **LLM SDK** | openai Python SDK 官方维护 | Spring AI + OkHttp | Spring AI 封装了 |
| **向量数据库** | Chroma Python 原生 | JVector / Java 客户端 | Chroma 有 HTTP API，语言无关 |
| **部署** | FastAPI + Docker | **Spring Boot + Docker（你的强项）** | 🔥 Spring Boot |
| **Function Calling** | 原生支持 | Spring AI 封装 | Spring AI 封装了 |
| **学习成本** | 需要学 Python + 新框架 | **复用 Java + Spring 经验** | ✅ 零成本入门 |

### Java AI 三大技术路线

```mermaid
flowchart LR
    Start["Java 项目需要 AI 能力"] --> Q{"选哪个?"}

    Q -->|"已在用 Spring Boot<br/>需要快速集成 AI"| SA["🛡️ Spring AI<br/>首选 ⭐"]
    Q -->|"需要 LangChain 相同 API<br/>多平台兼容"| LCJ["🔗 LangChain4j"]
    Q -->|"就调一个 API<br/>不想加依赖"| DIR["⚡ 直接调用 HTTP<br/>（兜底方案）"]

    SA --> SA1["Spring AI = Spring 生态的 AI 组件<br/>调用LLM / RAG / Function Calling<br/>类似 Spring Data 之于数据库"]
    LCJ --> LCJ1["LangChain4j = LangChain 的 Java 移植<br/>API 和 Python LangChain 高度相似<br/>适合两边都写的团队"]
    DIR --> DIR1["OpenAI API / DeepSeek API 都是 HTTP<br/>用 RestTemplate / WebClient 就能调<br/>控制力最强"]

    style SA fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style LCJ fill:#FFF3E0,stroke:#F57C00
    style DIR fill:#E3F2FD,stroke:#1976D2
```

### Spring AI 核心概念速查

Spring AI 是 Spring 生态最新成员（2024 年发布），设计哲学和 Spring Data 完全一致：**定义接口 → 配置实现 → 注入使用**。

```java
// Spring AI 的设计模式 = 你熟悉的 Spring 三板斧

// 1️⃣ 定义接口（Spring Data 的 CrudRepository → Spring AI 的 ChatClient）
@Autowired
private ChatClient chatClient;  // 注入 AI 聊天客户端

// 2️⃣ 配置实现（application.yml 里决定用哪个模型）
// spring.ai.openai.api-key=sk-xxx
// spring.ai.deepseek.api-key=sk-xxx

// 3️⃣ 使用（就像用 JdbcTemplate 一样简单）
String answer = chatClient.call("解释一下 HashMap 的原理");
```

## 三大路线对比

| 维度 | Spring AI ⭐ | LangChain4j | 直接调 API |
|------|------------|-------------|-----------|
| **维护方** | VMware/Spring 官方 | 社区 | 你自己 |
| **学习成本** | 低（你本来就会 Spring） | 中（需要理解 LangChain 概念） | 低 |
| **Spring Boot 集成** | **原生** | 需要手动配置 | 手动配置 |
| **Function Calling** | ✅ 原生支持 | ✅ 原生支持 | ❌ 手动实现 JSON 解析 |
| **RAG** | ✅ VectorStore + 文档处理 | ✅ 集成 Chroma/Weaviate | ❌ 自己动手 |
| **支持模型** | OpenAI、DeepSeek、通义、智谱、Ollama 等 | OpenAI、DeepSeek、Ollama 等 | 只要是 HTTP API 都行 |
| **生产级** | ✅ ErrorHandler、Retry、Metrics | ⚠️ 社区驱动 | ⚠️ 全靠你自己 |
| **版本** | 1.0+（2025 年发布正式版） | 1.0+（已正式发布） | N/A |

### Spring AI 支持的大模型

```mermaid
graph TB
    SA[Spring AI] --> O[OpenAI / Azure OpenAI]
    SA --> DS[DeepSeek ⭐ 国内首选]
    SA --> QW[通义千问 Qwen ⭐ 阿里]
    SA --> GL[智谱 GLM]
    SA --> WX[文心一言]
    SA --> OL[Ollama 本地部署]
    SA --> AX[Amazon Bedrock]
    SA --> GO[Google Vertex AI]

    style DS fill:#C8E6C9,stroke:#388E3C
    style QW fill:#C8E6C9,stroke:#388E3C
```

## 项目代码参考

| 代码文件 | 演示的概念 |
|---------|-----------|
| `agent-project-java/pom.xml` | Spring AI / RestTemplate 依赖配置 |
| `agent-project-java/.../controller/AgentController.java` | 纯 Java Agent 实现 |

## 参考来源

- Spring AI 官网: https://spring.io/projects/spring-ai
- Spring AI 文档: https://docs.spring.io/spring-ai/reference/
- LangChain4j 官网: https://docs.langchain4j.dev
- 相关笔记: `Spring AI实战.md`
