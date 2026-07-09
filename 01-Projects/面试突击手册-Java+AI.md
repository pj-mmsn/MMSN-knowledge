---
title: 面试突击手册 — Java开发 + AI开发
created: 2026-07-09
updated: 2026-07-09
type: project
tags: [Java, AI, Agent, 职业规划, 面试]
---

# 🎯 面试突击手册 — Java 开发 + AI 开发

> 目标：周一面试。策略：Java 八股保底 + AI/Agent 加分 + 项目经验出彩。
> 按面试频率排序，★ 越多越可能被问。

---

## 一、Java 核心高频（必问，60% 时间）

### 1. HashMap ★★★★★

**一句话**：数组 + 链表 + 红黑树，hash 定位槽位，拉链法解决冲突。

| 概念 | JDK 1.7 | JDK 1.8+ |
|------|---------|----------|
| 结构 | 数组 + 链表 | 数组 + 链表 + 红黑树 |
| 插入 | 头插法（并发扩容可能成环） | **尾插法**（避免死循环） |
| 树化 | 无 | 链表 ≥ 8 且数组 ≥ 64 → 红黑树 |
| 退化 | 无 | 红黑树节点 ≤ 6 → 链表 |

**为什么容量是 2 的幂**：用 `(n-1) & hash` 代替 `hash % n`，位运算快。n-1 二进制全 1，hash 分布均匀。

**默认值**：初始容量 16，负载因子 0.75，超过 `16 × 0.75 = 12` 就扩容 2 倍。

**面试话术**：「HashMap 是我最熟悉的集合类，从 1.7 到 1.8 了解过它的演进。头插法改尾插法解决了并发死循环，加入红黑树让极端冲突下查找从 O(n) 降到 O(log n)。」

---

### 2. ConcurrentHashMap ★★★★★

**核心问题**：HashMap 线程不安全，HashTable 全表锁太慢，ConcurrentHashMap 怎么做到高并发安全？

| 版本 | 锁策略 | 结构 |
|------|--------|------|
| 1.7 | Segment 分段锁（继承 ReentrantLock） | 16 个 Segment，每段独立加锁 |
| 1.8+ | **CAS + synchronized 锁单桶头节点** | 数组 + 链表 + 红黑树 |

**1.8 put 流程**：
1. 桶为空 → **CAS 尝试放 Node**（无锁）
2. 桶不为空 → **synchronized 锁头节点** → 遍历链表/树
3. 读操作（get）**完全无锁**，因为 Node 的 val 和 next 是 volatile

**面试话术**：「1.8 的改进把锁粒度从『段』降到『桶』，并发度从默认 16 提升到数组长度。读操作完全无锁，写的 CAS 也减少了锁竞争。这是典型的空间换时间 + 无锁化设计的思路。」

---

### 3. 线程池 ★★★★★

**核心问题**：为什么用线程池？7 个参数？执行流程？

**为什么用**：复用线程 → 减少创建/销毁开销 + 控制并发数 + 统一管理。

**7 个参数**（按重要性记）：
```
corePoolSize      ← 核心线程（常驻）
maximumPoolSize   ← 最大线程
keepAliveTime     ← 非核心线程空闲多久回收
unit              ← 时间单位
workQueue         ← 任务队列（阻塞队列）
threadFactory     ← 线程工厂
handler           ← 拒绝策略
```

**执行流程（面试必画）**：
```
提交任务 → 核心线程没满？→ 创建核心线程执行
                    ↓ 满了
              队列没满？→ 入队等待
                    ↓ 满了
              线程数 < 最大？→ 创建非核心线程
                    ↓ 也满了
              触发拒绝策略
```

**4 种拒绝策略**：AbortPolicy（抛异常，默认）、CallerRunsPolicy（调用者执行）、DiscardPolicy（丢弃）、DiscardOldestPolicy（丢最旧的）。

**《阿里巴巴手册》强制**：用 `ThreadPoolExecutor` 显式构造，**禁止用 Executors**（无界队列/线程数导致 OOM）。

---

### 4. synchronized vs Lock ★★★★

| 维度 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现 | JVM 层面（monitorenter） | Java API（AQS） |
| 释放 | **自动**（JVM 保证，异常也释放） | **手动**（必须 finally unlock） |
| 可中断 | 不支持（死等） | `lockInterruptibly()` |
| 超时 | 不支持 | `tryLock(timeout)` |
| 公平锁 | 非公平（默认） | 可选公平 `new ReentrantLock(true)` |
| 条件 | 一个（wait/notify） | 多个 `newCondition()` |

**锁升级（synchronized 优化）**：无锁 → 偏向锁 → 轻量级锁（CAS）→ 重量级锁（monitor）。JDK 1.6 后默认开启。

**面试话术**：「90% 场景用 synchronized 就够了，JDK 1.6 优化后性能接近 ReentrantLock。需要可中断、超时、公平锁这些特性时才用 Lock。」

---

### 5. volatile 与 JMM ★★★★

**volatile 两大作用**：
1. **保证可见性**：一个线程修改 volatile 变量，其他线程立即可见（禁止 CPU 缓存）
2. **禁止指令重排**：通过内存屏障实现

**不保证原子性**：`i++` 是读-改-写三步，volatile 不能保证原子性。需要 `AtomicInteger` 或 `synchronized`。

**JMM（Java 内存模型）**：规范了多线程下内存可见性和指令重排的规则。核心是 **happens-before** 原则。

**DCL（双重检查锁定）单例为什么要 volatile**：
```java
public class Singleton {
    private static volatile Singleton instance;  // ← volatile 防指令重排
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();  // 三步：分配内存→初始化→赋值
                    // 没有 volatile，可能 2 和 3 重排，其他线程拿到未初始化的对象
                }
            }
        }
        return instance;
    }
}
```

---

### 6. AQS（AbstractQueuedSynchronizer）★★★

**AQS 是什么**：JUC 并发工具类的基石。基于 **CLH 队列 + state 状态变量**。

**核心思想**：如果资源空闲（state=0），CAS 抢锁；抢不到，线程封装成 Node 放入 FIFO 队列自旋等待；前驱释放后唤醒后继。

**基于 AQS 的类**：ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock。

**面试话术**：「AQS 就像一个排队系统，state 是计数器，CLH 队列是排队的人。ReentrantLock 把 state 设为 1 表示有线程持锁，设为 0 表示释放。」

---

### 7. JVM 内存结构 & GC ★★★★

**内存结构（5 块）**：
```
堆 Heap            ← 对象实例，GC 主战场
方法区/元空间        ← 类信息、常量、静态变量
虚拟机栈             ← 方法调用的栈帧（局部变量、操作数栈）
本地方法栈           ← native 方法
程序计数器           ← 当前执行的字节码行号
```

**GC 算法对比**：

| 算法 | 原理 | 缺点 | 用途 |
|------|------|------|------|
| 标记-清除 | 标记可达 → 清除未标记 | 碎片化 | CMS 老年代 |
| 标记-复制 | 存活对象复制到另一块 | 浪费一半空间 | **新生代** |
| 标记-整理 | 存活对象移到一端 → 清边界外 | 移动开销 | Parallel Old |

**Minor GC vs Full GC**：
- Minor GC：新生代，频繁，快，STW 短
- Full GC：老年代，慢，STW 长，**应尽量避免**

**如何判断对象可回收**：**可达性分析** — 从 GC Roots 出发搜索引用链，不可达就回收。GC Roots 包括：栈中局部变量、静态变量、常量池引用、JNI 引用。

**面试话术**：「内存结构是面试官最喜欢问的基础题。记住堆和栈的本质区别就行：堆存对象，栈存方法调用。GC 发生在堆上。」

---

### 8. Spring IoC & AOP ★★★★

**IoC（控制反转）**：对象的创建和依赖交给 Spring 容器，不再自己 `new`。

**DI（依赖注入）**：实现 IoC 的方式——构造器注入、setter 注入、字段注入（`@Autowired`）。

**Bean 生命周期**：实例化 → 属性赋值 → 初始化（`@PostConstruct`）→ 使用 → 销毁（`@PreDestroy`）

**AOP（面向切面）核心术语**：
- **切面 Aspect**：横切逻辑的类（如日志切面）
- **切点 Pointcut**：在哪些方法生效（`execution(* com.xxx.*.*(..))`）
- **通知 Advice**：`@Before`/`@After`/`@Around`
- **代理方式**：有接口用 JDK 动态代理，无接口用 CGLIB（生成子类）

**面试话术**：「IoC 解耦对象的创建，AOP 解耦横切逻辑。Spring Boot 里 `@Transactional` 就是 AOP 的典型应用——在方法前后加事务管理，业务代码一行不用改。」

---

### 9. 类加载机制 ★★★

**双亲委派模型**：
```
Bootstrap ClassLoader      ← 加载 rt.jar（JVM 核心类）
    ↑
Extension ClassLoader      ← 加载 ext/ 目录
    ↑
Application ClassLoader    ← 加载 classpath
    ↑
自定义 ClassLoader          ← 你写的
```

**工作流程**：收到加载请求 → 不自己加载 → 委托父加载器 → 父找不到 → 自己加载。

**为什么**：1. 防止重复加载  2. 防止核心类被篡改（你写的 `java.lang.String` 不会被加载）。

---

### 10. MySQL 索引 & Redis ★★★

**B+Tree 索引**：为什么 MySQL 用 B+Tree 不用 Hash 或二叉树？
- B+Tree 树高很低（3-4 层就能存千万级数据），减少磁盘 IO
- 叶子节点形成有序链表，支持范围查询（Hash 不支持）
- 非叶子节点只存 key，一页能存更多，树更矮

**联合索引最左前缀原则**：`(a,b,c)` 索引，查询 `a=?` 或 `a=? AND b=?` 走索引，`b=?` 或 `c=?` 不走。

**Redis 持久化**：RDB（快照，快但有丢失风险）vs AOF（追加日志，数据安全但文件大）。生产环境通常两者都用。

---

## 二、AI/Agent 加分项（展示差异化，30% 时间）

### 1. Agent 是什么 ★★★★★

> Agent = LLM（大脑）+ Memory（记忆）+ Tools（工具）+ Planning（规划）

| 层级 | 对比 |
|------|------|
| Chatbot | 被动聊天，不会"做事" |
| Copilot | LLM 建议，人类执行 |
| **Agent** | LLM 自主规划 + 执行 + 反思，完成端到端任务 |

**类比**：LLM 是大脑，Memory 是笔记本，Tools 是手，Planning 是做事方法。

---

### 2. RAG — 企业落地最多的 AI 技术 ★★★★★

**一句话**：先把你的文档存进向量数据库，用户提问时先检索相关文档，拼进 Prompt 给 LLM 回答。从此不再胡说八道。

**流程**：文档 → 切块(Chunking) → Embedding 向量化 → 存入向量数据库 → 用户提问 → 检索 → 拼入 Prompt → LLM 生成答案

**RAG vs 微调**（面试官最爱问）：

| 维度 | RAG | 微调 |
|------|-----|------|
| 更新速度 | 秒级 | 天级（需重新训练） |
| 幻觉 | **低**（有文档依据） | 中（模型仍可编造） |
| 成本 | 低（向量数据库） | 高（GPU 训练） |
| 推荐 | **90% 企业首选** | RAG 不够时补充 |

**面试话术**：「我们之前的项目用 RAG 解决了企业知识库问答。核心难点在 Chunking 策略和检索精度——文档切多大、要不要重叠、用什么 Embedding 模型，这些比代码本身更关键。」

---

### 3. Spring AI — Java 集成 AI 的标准方式 ★★★★

**核心抽象**（和 Spring Data 一样的套路）：
```
ChatClient        → 调用 LLM（读配置改模型，不改代码）
EmbeddingModel    → 文本转向量
VectorStore       → 向量数据库操作
```

**一段代码说清楚**：
```java
// 和写 Spring Data 一样熟悉
@RestController
public class AIController {
    private final ChatClient chatClient;

    public AIController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/chat")
    public String chat(@RequestParam String question) {
        return chatClient.prompt()
            .user(question)
            .call()
            .content();
    }
}
```

**面试话术**：「Spring AI 最大的价值是让 Java 团队零学习成本接入 AI。同样的依赖注入、同样的配置方式、同样的 MVC 分层，只是把数据库换成了大模型。我们已经在一个内部项目里落地了。」

---

### 4. Function Calling / Tool Use ★★★

Agent 不只是聊天，还能**调用外部工具**：查数据库、调 API、写文件、发邮件。

流程：用户说"帮我查一下张三的订单"→ LLM 输出 function call `{name: "query_order", args: {user: "张三"}}` → 你的代码执行查询 → 结果返回 LLM → LLM 用自然语言回答。

**面试话术**：「Function Calling 是 Agent 从『能说』到『能做』的关键。我们在项目里封了一层统一适配器，让 OpenAI、DeepSeek、Anthropic 三种协议的不同 function call 格式对业务代码透明。」

---

### 5. 你做的 AI 项目（要有故事）★★★★★

**项目一：AI 小说家**
- 技术栈：PyQt5（桌面端）+ DeepSeek API
- 亮点：5 种写作模式，Prompt 模板化设计，从零踩坑完整交付
- 面试可以讲：Prompt 工程的实战经验、调用 API 的坑（双协议兼容）

**项目二：从零构建 Agent**
- 技术栈：Python + Java 双轨
- 亮点：完整踩坑记录，覆盖 Agent 核心概念到部署
- 面试可以讲：Agent 四层架构的实际落地、技术选型过程

**项目三：Multi-Agent 视频工作室**
- 技术栈：多 Agent 协作
- 亮点：多个 Agent 分工协作完成复杂任务
- 面试可以讲：Agent 间通信、任务拆分与编排

---

## 三、现场话术模板（10% 时间，出场即用）

### 自我介绍（60 秒版）

> 「面试官好，我是 XXX，XX 年后端开发经验，主要技术栈是 Java + Spring Boot。最近一年在主动学习和实践 AI/Agent 开发，用 Python + DeepSeek 从零做过几个项目——AI 写作工具、Agent 框架对比、从零构建 Agent。我认为 AI 不会取代 Java 开发，但会用 AI 的 Java 开发会取代不会用的。所以我来面试这个『Java 开发 + 带点 AI』的岗位，正好是我正在深入的方向。」

### 回答"为什么学 AI"

> 「这不是跟风。我发现在实际工作中，很多场景其实可以用 AI 解决——比如日志分析、代码审查、知识库问答。学了 Agent 之后发现，它不是另一个技术栈，而是对现有系统的增强层。Spring AI 就是最好的证明——同样的 Spring，同样的依赖注入，只是多了一个 ChatClient。」

### 被问"你不会 AI 算法底层？"

> 「我目前聚焦在应用层——怎么把大模型接入现有 Java 系统、怎么做 RAG、怎么设计 Agent 架构。底层训练和算法不是我的强项，但工程落地是我的优势。我对 Spring 生态很熟，Spring AI 的集成我能很快上手。」

### 反问面试官的好问题

- 「团队目前用 AI 在哪些场景？是主要在探索还是已经有落地？」
- 「Java 系统接入 AI，团队倾向用 Spring AI 还是自研？」
- 「这个岗位未来一年最希望我在 AI 方向做到什么程度？」

---

## 四、最后 24 小时速查清单

**必须脱口而出的知识点**：
- [ ] HashMap 1.7→1.8 变化、为什么 2 的幂
- [ ] ConcurrentHashMap 1.7 分段锁 vs 1.8 CAS+synchronized
- [ ] 线程池 7 参数 + 执行流程
- [ ] synchronized vs Lock 对比表
- [ ] volatile 两大作用 + DCL 为什么用它
- [ ] JVM 内存结构 5 块
- [ ] GC 算法 4 种 + Minor GC vs Full GC
- [ ] AOP 核心术语（切面/切点/通知/代理）
- [ ] Agent 定义：LLM + Memory + Tools + Planning
- [ ] RAG 流程 + RAG vs 微调对比
- [ ] Spring AI 三大抽象（ChatClient/Embedding/VectorStore）

**准备好讲的故事**：
- [ ] 自我介绍（60 秒）
- [ ] 一个 AI 项目的完整经历（挖坑→踩坑→填坑）
- [ ] 反问面试官的 3 个问题

---

> 加油 💪 你有扎实的 Java 底子 + 真实的 AI 项目经验，已经跑赢了 90% 的候选人。

---

## 五、🆕 2026 年面试新热点（网上最新趋势补充）

> 以下内容基于 2026 年 7 月各大厂真实面试题趋势汇总，用于补全手册。

---

### 1. Virtual Threads（虚拟线程）— JDK 21 最大变革 ★★★★★

**一句话**：Java 的轻量级线程，一个 OS 线程上跑百万虚拟线程，不用再写异步回调。

| 维度 | 平台线程 (传统) | 虚拟线程 (JDK 21+) |
|------|:---:|---|
| 对应 | OS 线程 1:1 | JVM 管理，M:N 映射 |
| 创建成本 | ~1MB 栈空间 | ~几 KB |
| 阻塞行为 | **占用** OS 线程 | 自动让出 carrier |
| 最大数量 | 几千 | **百万级** |

**代码对比**：
```java
// 传统：1000 个线程可能 OOM
for (int i = 0; i < 1000; i++) {
    new Thread(() -> callAPI()).start();
}

// 虚拟线程：100 万个也没事
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        executor.submit(() -> callAPI());
    }
}
```

**面试话术**：「虚拟线程解决了 Java 在 IO 密集型场景长期以来的痛点——以前必须用 CompletableFuture 或 WebFlux 写异步代码，现在同步写法就能获得异步性能。Spring Boot 3.2+ 已经内置支持，`@Async` + 虚拟线程一行不改就能享受。」

---

### 2. Pattern Matching + Record — JDK 17/21 语法糖 ★★★★

**Record**：不可变数据载体，一行替代 POJO：
```java
// 以前 50 行
public class User {
    private final String name;
    private final int age;
    // constructor, getters, equals, hashCode, toString...
}

// 现在 1 行
public record User(String name, int age) {}
```

**Pattern Matching for switch**（JDK 21）：
```java
String result = switch (obj) {
    case Integer i  -> "整数: " + i;
    case String s   -> "字符串长度: " + s.length();
    case User u     -> "用户: " + u.name();
    case null       -> "空值";
    default         -> "未知类型";
};
```

**面试话术**：「Record 让我终于不用写 Lombok 了。Pattern Matching 让 Java 的类型判断从冗长的 instanceof+cast 变成了优雅的模式匹配，写代码像是在写 Scala。」

---

### 3. Spring AI 2026 新动向 ★★★★

| 特性 | 说明 |
|------|------|
| **多模态** | 图片 + 文字一起输入 LLM |
| **MCP 集成** | 通过 Model Context Protocol 连接外部工具/数据库 |
| **Advisor 链** | 类似 Spring Interceptor，给 Prompt 加前后处理 |
| **评估框架** | 内置 RAG 质量评估 + 幻觉检测 |
| **原生虚拟线程** | Spring AI 全链路用虚拟线程，无需额外配置 |

**典型的 Advisor 链**：
```java
ChatClient chatClient = ChatClient.builder(model)
    .defaultAdvisors(
        new SimpleLoggerAdvisor(),       // 记录请求
        new QuestionAnswerAdvisor(vectorStore),  // RAG
        new ChatMemoryAdvisor(memory)    // 对话记忆
    ).build();
```

---

### 4. MCP（Model Context Protocol）★★★★★

**这是 2026 上半年最火的 AI 话题，面试必问。**

**一句话**：AI 应用的「USB-C 接口」——统一了 LLM 连接外部工具的协议标准。

- **之前**：每个 LLM Provider 有自己的 Tool 格式（OpenAI function calling、Anthropic tool use…）
- **现在**：MCP 定义一个标准协议，任何 MCP Server 可以被任何 MCP Client 调用
- **类比**：就像 HTTP 统一了 Web 通信，MCP 统一了 AI 工具调用

**面试话术**：「我们之前对接不同 LLM 要写三套 tool 适配代码，引入 MCP 后只需要写一个 MCP Server。它的生态发展极快——数据库、文件系统、API 平台都有现成的 MCP Server。」

---

### 5. Agent 全家桶：从单 Agent 到 Multi-Agent ★★★★

**2026 面试官会追问的进阶问题**：

**Q: 单 Agent vs Multi-Agent 什么时候用？**
- 单 Agent：任务单一、流程线性（如客服问答）
- Multi-Agent：任务复杂、需要专业分工（如视频制作：编剧Agent→剪辑Agent→配音Agent）

**Q: Agent 怎么评估效果？**
- 任务完成率（是否做完）
- 工具调用准确率（function call 参数对不对）
- 幻觉率（和 RAG 文档的匹配度）
- 成本（花了多少 token）

**Q: Agent 的 Memory 怎么设计？**
- 短期记忆：对话上下文窗口
- 长期记忆：向量数据库存储历史交互
- 工作记忆：当前任务的临时状态（类似 CPU 寄存器）

**Agent 架构 2026 主流方案**：

| 框架 | 语言 | 优势 |
|------|:---:|------|
| LangGraph | Python | 状态机式 Agent 编排 |
| CrewAI | Python | 角色扮演式 Multi-Agent |
| AutoGen | Python | 微软出品，对话驱动 |
| Spring AI | Java | Spring 生态原生集成 |
| Dify/Coze | 低代码 | 拖拽式 Agent 搭建 |

---

### 6. GraalVM Native Image — 面试新宠 ★★★

**为什么面试官开始问这个**：云原生时代，启动速度 = 钱。

| 指标 | JVM (传统) | Native Image |
|------|:---:|:---:|
| 启动时间 | 1-3 秒 | **<0.1 秒** |
| 内存占用 | 200MB+ | **<50MB** |
| 镜像大小 | 200MB+ | **<50MB** |
| 编译时间 | — | 需要额外编译（几分钟） |

**限制**：反射、动态代理、AOP（CGLIB）需要配置元数据。Spring Boot 3.x 的 AOT 编译能自动生成大部分配置。

**面试话术**：「Serverless 场景下冷启动是关键 KPI，Native Image 让 Java 微服务也能做到毫秒级启动，不再被 Go 碾压。」

---

### 7. 2026 大厂高频系统设计题 ★★★★

| 题目 | 考察点 | 出现频率 |
|------|--------|:---:|
| 设计一个 RAG 知识库问答系统 | Chunking、向量检索、混合搜索 | 🔥🔥🔥🔥🔥 |
| 设计一个秒杀系统 | 缓存、限流、分布式锁、MQ 削峰 | 🔥🔥🔥🔥 |
| 设计一个短链接服务 | 哈希算法、301 vs 302、布隆过滤器 | 🔥🔥🔥 |
| 设计一个 AI Agent 平台 | 工具注册、Memory、多模型路由 | 🔥🔥🔥🔥 |
| 设计一个实时消息推送 | WebSocket、连接管理、离线消息 | 🔥🔥🔥 |
| 设计一个分布式 ID 生成器 | 雪花算法、号段模式、时钟回拨 | 🔥🔥🔥 |

---

### 📋 速查清单补充（2026 新增）

**必须脱口而出**：
- [ ] Virtual Threads vs 平台线程对比
- [ ] Record + Pattern Matching 一句话讲清楚
- [ ] MCP 是什么、解决了什么问题
- [ ] Spring AI 的 Advisor 链机制
- [ ] GraalVM Native Image 三指标（启动/内存/大小）
- [ ] Multi-Agent 协作方案选型
- [ ] Agent Memory 三层设计

**准备好讲的故事**：
- [ ] 为什么从传统线程池迁移到 Virtual Threads（实际收益）
- [ ] 一个 MCP 集成的实战案例
- [ ] 对「AI 编码工具（Claude Code/Cursor/Copilot）对程序员的影响」的看法

---

*补充于: 2026-07-09 | 来源：2026 年大厂面经 + AI 技术社区 + 官方文档*
