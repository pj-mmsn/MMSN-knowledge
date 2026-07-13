# Java 索引

> Java 全栈知识体系 — 基础 → 集合 → 并发 → JVM → Spring → 数据库 → 中间件 → 分布式

---

## 基础

- [Java基础知识](Java基础知识.md) — JDK/JRE/JVM、== vs equals、面向对象
- [Java是值传递](Java是值传递.md) — 为什么 Java 只有值传递
- [反射](反射.md) — Class、Method、Field 反射机制
- [泛型与通配符](泛型与通配符.md) — 类型擦除、extends/super 通配符
- [代理](代理.md) — 静态代理、JDK 动态代理、CGLIB
- [SPI机制](SPI机制.md) — ServiceLoader 原理与实战
- [序列化](序列化.md) — Serializable、Externalizable、Kryo
- [BigDecimal](BigDecimal.md) — 精度运算与舍入模式

## 集合

- [HashMap](HashMap.md) — 数组+链表+红黑树、位运算、扰动函数、扩容免重hash
- [ArrayList](ArrayList.md) — 动态数组、扩容、Fail-Fast
- [LinkedList](LinkedList.md) — 双向链表与队列
- [ConcurrentHashMap](ConcurrentHashMap.md) — CAS+synchronized锁单桶、读无锁、分段计数

## 并发

- [线程池](线程池.md) — 7参数+状态机+Worker+拒绝策略
- [AQS](AQS.md) — state+CLH队列、公平vs非公平
- [synchronized与Lock](synchronized与Lock.md) — Mark Word+锁升级四阶段
- [volatile与JMM](volatile与JMM.md) — 可见性+有序性+内存屏障+DCL
- [CAS与Atomic](CAS与Atomic.md) — 乐观锁+ABA+自旋
- [ThreadLocal](ThreadLocal.md) — 线程隔离+内存泄漏

## JVM

- [内存结构](内存结构.md) — 堆、栈、方法区、元空间
- [垃圾回收GC](垃圾回收GC.md) — 标记-清除/复制/整理、G1、ZGC
- [类加载机制](类加载机制.md) — 双亲委派、自定义类加载器

## Spring

- [IoC与AOP](IoC与AOP.md) — Bean生命周期+三级缓存+动态代理
- [Spring Boot 自动配置](Spring Boot 自动配置.md) — @EnableAutoConfiguration+条件装配
- [Spring事务传播机制](Spring事务传播机制.md) — 7种传播行为+失效三场景
- [Spring MVC 请求流程](Spring MVC 请求流程.md) — DispatcherServlet→Controller完整链路

## 数据库

- [索引](索引.md) — MySQL B+Tree 索引原理与优化
- [MySQL 事务与锁](MySQL 事务与锁.md) — ACID+隔离级别+MVCC+行锁/间隙锁
- [持久化](持久化.md) — Redis RDB、AOF 持久化机制
- [Redis 缓存策略](Redis 缓存策略.md) — 穿透/击穿/雪崩+分布式锁

## 中间件

- [MyBatis 核心原理](MyBatis 核心原理.md) — #{} vs ${}+一二级缓存
- [消息队列 MQ](消息队列 MQ.md) — Kafka+削峰/解耦/异步

## 分布式

- [CAP与BASE](CAP与BASE.md) — CAP 定理与 BASE 理论
- [分布式系统设计](分布式系统设计.md) — 分布式事务+ID方案
- [系统设计答题框架](系统设计答题框架.md) — 万能五步法+秒杀案例

## 基础理论

- [计算机网络基础](计算机网络基础.md) — TCP/HTTP+三次握手+状态码
- [设计模式在Spring中的应用](设计模式在Spring中的应用.md) — 单例/工厂/代理/模板/策略

---

## 关联领域

- 🤖 [AI与Agent 索引](../AI与Agent/_index.md) — Java AI 开发（Spring AI、LLM调用、向量数据库）
- 🐍 [Python 索引](../Python/_index.md) — AI 主力语言速成
- 📖 [JavaGuide](../../03-Resources/JavaGuide/) — 470+ 篇参考（只读）
- 📝 [经验日志](../../05-经验日志/_index.md) — 踩坑记录
- 🎯 [面试突击手册](../../01-Projects/面试突击手册-Java+AI.md) — 导航索引

---

*最后更新: 2026-07-11 | 共 36 篇笔记*
