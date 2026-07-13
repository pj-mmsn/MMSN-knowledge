# 面试突击手册 — Java 全栈 + AI 开发

> 🗂️ **这是导航索引，不是大锅炖。** 每个知识点链接到知识库中对应的笔记。
> 按面试频率排序，★ 越多越重要。

---

## Java 核心（必问 ★★★★★）

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| HashMap | [HashMap](02-Areas/Java/HashMap.md | 数组+链表+红黑树，位与取模，扰动函数，扩容免重 hash |
| ConcurrentHashMap | [ConcurrentHashMap](02-Areas/Java/ConcurrentHashMap.md | CAS+synchronized 锁单桶，读无锁，分段计数 |
| 线程池 | [线程池](02-Areas/Java/线程池.md | 7 参数 + 状态机 + Worker + 拒绝策略 |
| synchronized vs Lock | [synchronized与Lock](02-Areas/Java/synchronized与Lock.md | Mark Word + 锁升级四阶段 |
| volatile + JMM | [volatile与JMM](02-Areas/Java/volatile与JMM.md | 可见性+有序性+内存屏障 + DCL |
| AQS | [AQS](02-Areas/Java/AQS.md | state + CLH 队列，公平 vs 非公平 |
| CAS | [CAS与Atomic](02-Areas/Java/CAS与Atomic.md | 乐观锁 + ABA + 自旋 |
| ThreadLocal | [ThreadLocal](02-Areas/Java/ThreadLocal.md | 线程隔离 + 内存泄漏 |
| Java 进阶 | [String/Stream/Optional/CompletableFuture](02-Areas/Java/Java%20进阶核心-String-Stream-Optional-CompletableFuture.md | String 不可变+函数式+异步编排+Java21 |

## JVM（必问 ★★★★）

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| 内存结构 | [内存结构](02-Areas/Java/内存结构.md | 堆/栈/方法区/元空间 |
| GC | [垃圾回收GC](02-Areas/Java/垃圾回收GC.md | 4 种算法 + Minor vs Full + G1 |
| 类加载 | [类加载机制](02-Areas/Java/类加载机制.md | 双亲委派 + 自定义加载器 |

## Java 集合 + 基础（常问 ★★★★）

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| ArrayList | [ArrayList](02-Areas/Java/ArrayList.md | 动态数组 + 扩容 |
| LinkedList | [LinkedList](02-Areas/Java/LinkedList.md | 双向链表 |
| 反射 | [反射](02-Areas/Java/反射.md | Class + Method + Field |
| 泛型 | [泛型与通配符](02-Areas/Java/泛型与通配符.md | 类型擦除 + extends/super |
| 代理 | [代理](02-Areas/Java/代理.md | JDK 动态代理 + CGLIB |
| 序列化 | [序列化](02-Areas/Java/序列化.md | Serializable + Kryo |
| SPI | [SPI机制](02-Areas/Java/SPI机制.md | ServiceLoader + 框架扩展 |
| BigDecimal | [BigDecimal](02-Areas/Java/BigDecimal.md | 精度运算 |

## Spring ★★★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| IoC + AOP | [IoC与AOP](02-Areas/Java/IoC与AOP.md | Bean 生命周期 + 三级缓存 + 动态代理 |
| Spring Boot 自动配置 | [Spring Boot 自动配置](02-Areas/Java/Spring%20Boot%20自动配置.md | @EnableAutoConfiguration + 条件装配 |
| **事务传播机制** | [Spring事务传播机制](02-Areas/Java/Spring事务传播机制.md | 7 种传播行为 + 失效三场景 |
| MVC 请求流程 | [Spring MVC 请求流程](02-Areas/Java/Spring%20MVC%20请求流程.md | DispatcherServlet → Controller 完整链路 |

## MySQL + Redis ★★★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| MySQL 索引 | [索引](02-Areas/Java/索引.md | B+Tree + 最左前缀 + Explain |
| MySQL 事务与锁 | [MySQL 事务与锁](02-Areas/Java/MySQL%20事务与锁.md | ACID + 隔离级别 + MVCC + 行锁/间隙锁 |
| Redis 持久化 | [持久化](02-Areas/Java/持久化.md | RDB + AOF |
| Redis 缓存策略 | [Redis 缓存策略](02-Areas/Java/Redis%20缓存策略.md | 穿透/击穿/雪崩 + 分布式锁 |

## 中间件 + 分布式 ★★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| 消息队列 | [消息队列 MQ](02-Areas/Java/消息队列%20MQ.md | Kafka + 削峰/解耦/异步 |
| MyBatis | [MyBatis 核心原理](02-Areas/Java/MyBatis%20核心原理.md | #{} vs ${} + 缓存 |
| CAP + BASE | [CAP与BASE](02-Areas/Java/CAP与BASE.md | 分布式理论基础 |
| 分布式系统设计 | [分布式系统设计](02-Areas/Java/分布式系统设计.md | 事务 + ID 方案 |
| 系统设计框架 | [系统设计答题框架](02-Areas/Java/系统设计答题框架.md | 万能五步法 + 秒杀案例 |

## 基础理论 ★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| 计算机网络 | [计算机网络基础](02-Areas/Java/计算机网络基础.md | TCP 三次握手 + HTTP 状态码 |
| 设计模式 | [设计模式在Spring中的应用](02-Areas/Java/设计模式在Spring中的应用.md | 单例/工厂/代理/模板/策略 |

## 项目实战 + 算法 ★★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| 项目全流程 | [Java项目开发全流程实战](02-Areas/Java/Java项目开发全流程实战.md | 需求→设计→编码→测试→上线→监控 |
| 算法基础 | [Java面试算法基础](02-Areas/Java/Java面试算法基础.md | 快排/归并/二分/链表/二叉树+思想 |
| 红黑树 | [红黑树原理详解](02-Areas/Java/红黑树原理详解.md | 五条铁律+旋转+变色+HashMap/TreeMap应用 |
| 位运算 | [位运算基础与实战](02-Areas/Java/位运算基础与实战.md | HashMap定位/线程池CTL/权限掩码 |
| B+Tree | [B+Tree 索引原理详解](02-Areas/Java/B+Tree%20索引原理详解.md | 矮胖设计+聚簇vs二级+vs红黑树/Hash |
| 线上排查 | [线上问题排查实战手册](02-Areas/Java/线上问题排查实战手册.md | CPU飙高/OOM/慢接口/死锁/慢SQL/Redis/MQ积压 |
| 微服务 | [微服务与Spring Cloud基础](02-Areas/Java/微服务与Spring%20Cloud基础.md | Nacos/Feign/Sentinel/Seata |
| 测试+日志 | [单元测试与日志框架基础](02-Areas/Java/单元测试与日志框架基础.md | JUnit5+Mockito+SLF4J+Logback |

## DevOps + 安全 ★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| DevOps | [DevOps 部署运维基础](02-Areas/Java/DevOps%20部署运维基础.md | Git/Docker/Linux/CI-CD/Nginx |
| 安全 | [Web 安全基础](02-Areas/Java/Web%20安全基础.md | SQL注入/XSS/CSRF/JWT/OAuth2 |

## 软技能 ★★★★★

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| 行为面试 | [行为面试与软技能话术](02-Areas/Java/行为面试与软技能话术.md | 离职原因/优缺点/STAR/期望薪资/反问5问 |
| AI 加分 | [AI项目面试加分指南](02-Areas/Java/AI项目面试加分指南.md | 三个项目STAR包装+模型速查+追问精准回答 |
| 面试日清单 | [面试当天准备清单](02-Areas/Java/面试当天准备清单.md | 时间线+回答结构+陷阱应对 |

---

## 🔥 全栈开发路线（Vue3 + TypeScript）

> 面试全栈岗位时的前端知识储备。

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| 全栈前端基础 | [全栈开发面试基础-Vue3+TS](02-Areas/Java/全栈开发面试基础-Vue3+TS.md | Vue3 响应式+组件通信+TS+HTTP/REST |

## 🔥 Python/Agent 开发路线

> 面试 Python Agent 开发岗位时的专业知识储备。

| 知识点 | 知识库笔记 | 一句话 |
|--------|-----------|--------|
| Agent 框架选型 | [Python Agent 开发实战-框架对比与选型](02-Areas/Python/Python%20Agent%20开发实战-框架对比与选型.md | LangChain vs LangGraph vs CrewAI 代码对比 |
| FastAPI 实战 | [FastAPI 后端开发实战](02-Areas/Python/FastAPI%20后端开发实战.md | async/SSE/Pydantic/部署 |
| 向量数据库 | [向量数据库实战-Chroma与pgvector](02-Areas/AI与Agent/向量数据库实战-Chroma与pgvector.md | Chroma/pgvector+混合检索+Rerank |
| Prompt 工程 | [Prompt 工程进阶](02-Areas/AI与Agent/Prompt%20工程进阶.md | 五层结构+Json容错+版本管理 |

## AI / Agent ★★★（加分项）

| 知识点        | 知识库笔记                                                          | 一句话                                  |
| ---------- | -------------------------------------------------------------- | ------------------------------------ |
| Agent 核心概念 | [Agent核心概念](02-Areas/AI与Agent/01-核心概念/Agent核心概念.md            | LLM + Memory + Tools + Planning      |
| Agent 架构模式 | [Agent架构模式全景](02-Areas/AI与Agent/01-核心概念/Agent架构模式全景.md        | ReAct / Plan-Execute / Reflection    |
| 规划与推理      | [规划与推理](02-Areas/AI与Agent/01-核心概念/规划与推理.md                    | CoT + Task Decomposition             |
| 记忆系统       | [记忆系统](02-Areas/AI与Agent/01-核心概念/记忆系统.md                      | 短期/长期/向量数据库                          |
| 工具调用       | [工具调用](02-Areas/AI与Agent/01-核心概念/工具调用.md                      | Function Calling 原理                  |
| RAG        | [RAG检索增强生成](02-Areas/AI与Agent/02-RAG与Prompt/RAG检索增强生成.md      | 检索增强生成全流程                            |
| Prompt 工程  | [Prompt工程](02-Areas/AI与Agent/02-RAG与Prompt/Prompt工程.md        | System Prompt + CoT                  |
| Spring AI  | [Spring AI实战](02-Areas/AI与Agent/04-Java-AI开发/Spring%20AI实战.md | ChatClient + Embedding + VectorStore |

---

## 面试话术

### 自我介绍（60 秒）

> 「面试官好，我是 XXX，X 年 Java 后端。技术栈 Spring Boot + MySQL + Redis + Kafka，熟悉并发编程和 JVM 调优。最近用 Spring AI 做过内部系统集成、自建过 RAG 知识库。我认为 AI 不是取代 Java，而是给 Java 加一层智能能力。」

### 反问三问

1. 「团队目前技术栈和中间件是什么样的？」
2. 「这个岗位最希望我解决什么技术难题？」
3. 「团队对 AI 有什么规划吗？」

---

*最后更新: 2026-07-11 | 覆盖 15 大模块，36 篇关联笔记*
