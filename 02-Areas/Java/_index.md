# Java 索引

> Java 核心知识体系 — 基础 → 集合 → 并发 → JVM → 数据库 → 框架 → 分布式

---

## 基础

- [Java基础知识](Java基础知识.md) — JDK/JRE/JVM、== vs equals、面向对象
- [Java是值传递](Java是值传递.md) — 为什么说 Java 只有值传递
- [反射](反射.md) — Class、Method、Field 反射机制
- [泛型与通配符](泛型与通配符.md) — 类型擦除、extends/super 通配符
- [代理](代理.md) — 静态代理、JDK 动态代理、CGLIB
- [SPI机制](SPI机制.md) — ServiceLoader 原理与实战
- [序列化](序列化.md) — Serializable、Externalizable、Kryo
- [BigDecimal](BigDecimal.md) — 精度运算与舍入模式

## 集合

- [HashMap](HashMap.md) — 哈希表原理、红黑树、扩容机制
- [ArrayList](ArrayList.md) — 动态数组、扩容、Fail-Fast
- [LinkedList](LinkedList.md) — 双向链表与队列
- [ConcurrentHashMap](ConcurrentHashMap.md) — 分段锁 → CAS + synchronized

## 并发

- [线程池](线程池.md) — ThreadPoolExecutor 参数与拒绝策略
- [AQS](AQS.md) — AbstractQueuedSynchronizer 原理
- [synchronized与Lock](synchronized与Lock.md) — 锁升级、ReentrantLock
- [volatile与JMM](volatile与JMM.md) — 可见性、内存屏障、happens-before
- [CAS与Atomic](CAS与Atomic.md) — CAS 原理与原子类
- [ThreadLocal](ThreadLocal.md) — 线程本地变量与内存泄漏

## JVM

- [内存结构](内存结构.md) — 堆、栈、方法区、元空间
- [垃圾回收GC](垃圾回收GC.md) — 标记-清除/复制/整理、G1、ZGC
- [类加载机制](类加载机制.md) — 双亲委派、自定义类加载器

## 数据库

- [索引](索引.md) — MySQL B+Tree 索引原理与优化
- [持久化](持久化.md) — Redis RDB、AOF 持久化机制

## 框架

- [IoC与AOP](IoC与AOP.md) — Spring IoC 容器与 AOP 原理

## 分布式

- [CAP与BASE](CAP与BASE.md) — CAP 定理与 BASE 理论

---

## 关联领域

- 🤖 [AI与Agent 索引](../AI与Agent/_index.md) — Java AI 开发（Spring AI、LLM调用、向量数据库）
- 🐍 [Python 索引](../Python/_index.md) — AI 主力语言，Java 工程师速成路径
- 📖 [JavaGuide](../../03-Resources/JavaGuide/) — 470+ 篇 Java 全栈参考（只读）
- 📝 [经验日志](../../05-经验日志/_index.md) — Spring 启动报错等踩坑记录

---

*最后更新: 2026-07-08 | 共 21 篇笔记*
