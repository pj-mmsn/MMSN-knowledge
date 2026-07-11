---
title: 面试突击手册 — Java开发 + AI开发（深度版）
created: 2026-07-09
updated: 2026-07-09
type: project
tags: [Java, AI, Agent, 职业规划, 面试]
---

# 🎯 面试突击手册 — Java + AI 深度版

> 不是知识点罗列。每道题从「一句话」→「原理」→「图解」→「源码细节」→「面试话术」完整展开。

---

## 一、HashMap — 面试第一题，问到源码才算及格

### 一句话

HashMap = **数组 + 链表 + 红黑树**，hash 定位桶下标，拉链法解决冲突。JDK 1.7 头插、1.8 尾插 + 树化。

### 数据结构全景

```
                table[] 桶数组 (容量必须是 2 的幂)
        ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
        │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 │11 │12 │13 │14 │15 │
        └───┴───┴─┬─┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
                  │
          ┌───────┘
          ▼
      ┌───────┐   ┌───────┐   ┌───────┐
      │k1│v1│next──→│k2│v2│next──→│k3│v3│next──→ null    ← 链表(拉链)
      └───────┘   └───────┘   └───────┘
       冲突了，挂到同一个桶下面。

      当链表 ≥ 8 且数组 ≥ 64：
      ┌───────┐
      │k1│v1│  ─── 红黑树节点 ───    ← 查找从 O(n) → O(log n)
      └───────┘   ╱         ╲
               Node        Node
              ╱    ╲      ╱    ╲
           ...    ...   ...    ...
```

### 位运算：为什么容量必须是 2 的幂

HashMap 用 `(n - 1) & hash` 定位桶下标，代替 `hash % n`。

**位与 `&`**：两个二进制位都是 1 结果才为 1，否则为 0。

```
例：hash=0b1101_0110(214)，n=16

  十进制取模:  214 % 16 = 6     ← 除法指令，几十个 CPU 周期
  位与:        214 & 15 = 6     ← 一条 AND 指令，1 个 CPU 周期

  为什么 214 & 15 = 6？

     1101 0110   (214)
  &  0000 1111   (15 = n-1, 二进制全是 1)
  ─────────────
     0000 0110   (6)   ← 相当于保留 hash 的低 4 位

  n 是 2 的幂 → n-1 的二进制全是 1 → hash 的低位被完整保留 → 分布均匀
  如果 n=10，n-1=9=0b1001，某些位永远是 0 → 大量桶永远用不到！
```

**扰动函数**：hash 值不是直接用 key.hashCode()，而是：

```java
// HashMap.hash() 源码
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
// 高 16 位和低 16 位做异或(XOR)，让高位也参与桶下标计算
// 否则 (n-1) & hash 只用到低几位，高位完全浪费
```

```
  h          = 1101 0110 0011 1001 1010 0101 1110 0011
  h >>> 16   = 0000 0000 0000 0000 1101 0110 0011 1001
  XOR(^)     ─────────────────────────────────────────
  hash       = 1101 0110 0011 1001 0111 0011 1101 1010
               └────高位融入低位────┘ └──低位扰动后──┘
```

### 红黑树：为什么链表 8 个节点就转树

**红黑树的五条铁律**：

1. 节点要么红，要么黑
2. 根节点永远是黑色
3. 红色节点的两个子节点必须是黑色（红不连红）
4. 从任意节点到其所有叶子节点的路径上，黑色节点数量相等（黑平衡）
5. 每个叶子节点（NIL）是黑色

```
       ● (黑)              ← 根永远黑
      ╱   ╲
     ○(红) ○(红)           ← 红节点的孩子必须是黑
    ╱ ╲    ╱ ╲
   ●   ●  ●   ●           ← 任意路径黑节点数相同
  ╱ ╲ ╱ ╲ ╱ ╲ ╱ ╲
 (NIL)……                 ← 叶子 NIL 算黑色
```

**为什么链表 ≥ 8 才转红黑树**：

```
  链表长度    平均查找次数       红黑树查找次数
  ────────   ──────────       ────────────
     1           0.5               O(log n)
     4           2
     8           4         ≈      3
    16           8         ≈      4
    64          32         ≈      6

  结论：长度 < 8 时，链表遍历和红黑树差距不大，转树反而有额外开销
        长度 ≥ 8 时，红黑树优势明显（O(n) vs O(log n)）
```

**红黑树 vs AVL 树**：AVL 更严格平衡（左右子树高度差 ≤ 1），查找稍快，但插入/删除旋转次数多。HashMap 增删频繁 → 红黑树更合适（最多 3 次旋转 vs AVL 可能 O(log n) 次）。

### put 流程（JDK 1.8 源码级）

```
put(key, value)
    │
    ▼
① hash(key) = key.hashCode() ^ (key.hashCode() >>> 16)    ← 扰动函数
    │
    ▼
② i = (n - 1) & hash                                      ← 定位桶下标
    │
    ▼
③ tab[i] == null ?
    ├─ 是 → tab[i] = newNode(hash, key, value, null)      ← 直接放
    │
    └─ 否 → 判断 key 是否相等？
              ├─ equals → 覆盖 value，返回旧值
              │
              ├─ 是 TreeNode → putTreeVal() 红黑树插入
              │
              └─ 普通 Node → 遍历链表（尾插法！）
                     ├─ 找到相同 key → 覆盖
                     ├─ 没找到 → 尾插入
                     └─ 检查 bitCount ≥ TREEIFY_THRESHOLD(8) ?
                         └─ 是 → treeifyBin() 
                              └─ tab.length < MIN_TREEIFY_CAPACITY(64) ?
                                  ├─ 是 → resize()  只扩容不树化
                                  └─ 否 → 转红黑树
    │
    ▼
④ if (++size > threshold) resize()                          ← 扩容
```

**扩容时元素怎么搬（JDK 1.8 的优化）**：

```
旧容量 = 16 (0b10000)
新容量 = 32

判断一个元素去新数组的哪个位置，只需要看 hash 的第 5 位(旧容量的那一位)：

    hash = 0b??? ?_???? ....
                  ↑
             hash & oldCap (0b10000)

    if (hash & oldCap) == 0  →  留在原下标
    if (hash & oldCap) != 0  →  原下标 + 旧容量

例：key 原在桶[5]，旧容量=16
    hash & 16 == 0  → 去新数组[5]
    hash & 16 != 0  → 去新数组[5+16] = [21]
```

**面试话术**：「HashMap 我从三个维度理解——数据结构（数组+链表+红黑树的演进）、hash 算法（扰动函数+位与取模）、扩容策略（2 倍扩容+免重 hash）。1.7 头插法的死循环是一个经典的多线程反例，1.8 尾插法解决了死循环但还是线程不安全——put 过程中的数据覆盖、size 不准确都可能导致丢数据。」

---

## 二、ConcurrentHashMap — 高并发安全的精髓

### 一句话

HashMap 线程不安全，HashTable 全表锁太慢。ConcurrentHashMap 1.8 用 **CAS + synchronized 锁单桶头节点**，读操作完全无锁。

### 锁策略演进

```
JDK 1.7:  Segment 分段锁 (16 个 Segment，每个独立 ReentrantLock)
         ┌─────────┬─────────┬──── ... ────┬─────────┐
         │Segment 0│Segment 1│   ...       │Segment15│  ← 16 把锁
         └────┬────┘─────────┘             └─────────┘
           ┌──┴──┐
           │桶数组│  ← 每个 Segment 有自己的 HashEntry 数组+链表
           └─────┘

JDK 1.8:  CAS + synchronized 锁单桶头节点
         ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
         │0 │1 │2 │3 │4 │5 │6 │7 │8 │9 │10│11│12│13│14│15│
         └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
              ↑                    ↑
         桶[i]空 → CAS 放      桶[i]不空 → synchronized 锁头节点
```

**1.8 改进的本质**：锁粒度从「Segment 的 16 把锁」降到「每个桶独立加锁」。数组长度 64 时理论上可以 64 个线程同时写不同桶。

### put 流程逐行分析

```
put(key, value)
    │
    ▼
① key 和 value 不能为 null（和 HashMap 不同！HashMap 允许一个 null key）
    │
    ▼
② 计算 hash = spread(key.hashCode())   ← 扰动函数和 HashMap 一样
    │
    ▼
③ 死循环 for (Node<K,V>[] tab = table;;) {  ← 自旋保证一定成功
    │
    ├─ tab 未初始化 → initTable()   ← CAS 设置 sizeCtl，只有一个线程初始化
    │
    ├─ tab[i] == null → casTabAt(tab, i, null, newNode)
    │      └─ CAS 成功 → break     ← 无锁！最快的路径
    │      └─ CAS 失败 → 继续循环
    │
    ├─ tab[i].hash == MOVED(-1) → helpTransfer()   ← 正在扩容，帮忙搬数据
    │
    └─ 否则 → synchronized(tab[i]) {   ← 锁住桶头节点
            ├─ 再次检查 tab[i] == 当前锁住的那个
            ├─ tab[i].hash >= 0 → 遍历链表，找相同 key / 尾插
            └─ tab[i] instanceof TreeBin → 红黑树插入
          }
    │
    ▼
④ addCount(1, binCount) → 检查是否需要扩容
    └─ sizeCtl < 0 → 正在扩容，帮忙
    └─ sizeCtl > 0 → CAS 尝试自己扩容
```

### CAS 详解

**CAS(Compare-And-Swap)**：一条 CPU 原子指令（x86: `cmpxchg`），无需加锁：

```
CAS(memoryAddress, expectedValue, newValue):
    比较 memoryAddress 处的值是否 == expectedValue
    相等 → 写入 newValue → 返回 true
    不等 → 不写入 → 返回 false
```

```
时间线图示：

内存 value = 10
                                ┌── 线程 B: CAS(10, 30)
线程 A: CAS(10, 20)             │    期望值10 = 内存值10 ✓
   期望值10 = 内存值10 ✓         │    → 写入 30，返回 true
   → 写入 20，返回 true          │
                                ▼
                           内存 value = 30
                                │
                                ▼
                           线程 A: CAS(10, 20)  第二次重试
                              期望值10 ≠ 内存值30 ✗
                              → 自旋：重新读 value=30，重试 CAS(30, 20)
```

### ConcurrentHashMap 计数器：怎么不靠锁统计 size

```java
// 不是简单的一个 int size，用了类似 LongAdder 的分段计数：
// CounterCell[] counterCells + baseCount
//
// 写操作时，随机选一个 CounterCell 做 CAS +1
// 读 size() 时，baseCount + 所有 CounterCell 的值求和
//
// 好处：多个线程并发写 size 时几乎无竞争（各自操作不同的 Cell）

// addCount 的大致逻辑：
private final void addCount(long x, int check) {
    CounterCell[] cs; long b, s;
    // 先 CAS baseCount
    if ((cs = counterCells) != null || !U.compareAndSetLong(this, BASECOUNT, b = baseCount, s = b + x)) {
        // CAS 失败了，把 x 加到某个 CounterCell 里
        ...
    }
}
```

**面试话术**：「ConcurrentHashMap 的三个设计精髓——锁粒度降到桶级别、读操作完全无锁（Node.val 和 next 都是 volatile）、size 统计用类似 LongAdder 的分段计数避免竞争。扩容时允许多线程协助搬运，不是单线程扛。」

---

## 三、线程池 — 不只是背 7 个参数

### 一句话

线程池复用线程，避免频繁创建/销毁的开销，同时限流防止系统被压垮。

### 不只是 7 参数 — 线程池的状态机

```java
// ThreadPoolExecutor 用一个 AtomicInteger ctl 同时存储：
//   高 3 位：线程池的运行状态
//   低 29 位：工作线程数

// 5 种状态：
//   RUNNING    (111) → 接受新任务 + 处理队列中的任务
//   SHUTDOWN   (000) → 不接受新任务，但处理队列中剩余任务   ← shutdown()
//   STOP       (001) → 不接受新任务，不处理队列，中断执行中  ← shutdownNow()
//   TIDYING    (010) → 过渡状态，所有任务终止，workerCount=0
//   TERMINATED (011) → terminated() 已执行

状态转换：
  RUNNING ──shutdown()──→ SHUTDOWN ──队列空──→ TIDYING ──→ TERMINATED
     │                                                         ↑
     └────shutdownNow()──→ STOP ──────────────────────────────→┘
```

### 核心流程：不只是简单流程图

```
submit(task) / execute(command)
    │
    ▼
workerCount < corePoolSize ?
    ├─ 是 → addWorker(command, true)  创建核心线程（不管队列有没有空位）
    │         └─ Worker 启动后，while (task != null || (task = getTask()) != null) 循环取任务
    │
    └─ 否 → workQueue.offer(command)  尝试入队
              ├─ 入队成功 → 任务在队列里等着，Worker 线程空闲时会 getTask() 取走
              │
              └─ 入队失败（队列满了）→ workerCount < maximumPoolSize ?
                    ├─ 是 → addWorker(command, false)  创建非核心线程
                    │         └─ 这个线程执行完当前任务后，keepAliveTime 内没新任务就销毁
                    │
                    └─ 否 → reject(command)  触发拒绝策略
```

### getTask() — Worker 怎么取任务

```java
// Worker 线程的 run() 里不断调 getTask()
private Runnable getTask() {
    boolean timedOut = false;
    for (;;) {
        int wc = workerCountOf(ctl);
        // 是否允许超时：核心线程默认不超时（allowCoreThreadTimeOut=false），非核心线程会超时
        boolean timed = allowCoreThreadTimeOut || wc > corePoolSize;

        if (wc > maximumPoolSize || (timed && timedOut)) {
            if (compareAndDecrementWorkerCount(ctl)) return null;  // 线程退出
            continue;
        }

        Runnable r = timed ?
            workQueue.poll(keepAliveTime, TimeUnit.NANOSECONDS) :   // 有超时等待
            workQueue.take();                                        // 阻塞等待
        if (r != null) return r;
        timedOut = true;
    }
}
```

### 拒绝策略图解

```
当线程数 = maximumPoolSize 且队列满：

    任务来了
        │
        ▼
    ┌───────────────┐
    │  拒绝策略      │
    ├───────────────┤
    │ AbortPolicy   │ → throw RejectedExecutionException（默认）
    │ CallerRuns    │ → 由提交任务的线程自己执行（谁 submit 谁跑）
    │ Discard       │ → 直接丢弃，不抛异常（静默丢任务！危险）
    │ DiscardOldest │ → 丢弃队列里最旧的，重新 submit
    └───────────────┘
```

**面试话术**：「线程池的状态机设计是 JDK 的经典——用一个 int 的高 3 位存状态、低 29 位存线程数，CAS 原子操作同时判断和修改。生产上调参的经验：IO 密集型设 `corePoolSize = CPU核数 × 2`，CPU 密集型设 `CPU核数 + 1`。但最终要根据实际压测结果调，不是套公式。」

---

## 四、synchronized — 从字节码到锁升级

### 一句话

synchronized 是 JVM 层面的内置锁。JDK 1.6 后引入**锁升级**（偏向锁 → 轻量级锁 → 重量级锁），性能接近 ReentrantLock。

### Mark Word：对象头里的锁标记

每个 Java 对象在堆内存中都有一个 **Mark Word**，存储了 hash、GC 分代年龄、锁状态：

```
Mark Word (64位 JVM):

无锁状态:
  ┌────────────────────┬──────┬─────┬─────┐
  │  unused:25 │ hash:31 │unused│ age │ 001 │   ← 最后 3 位 = 001 (无锁)
  └────────────────────┴──────┴─────┴─────┘

偏向锁:
  ┌─────────────────────┬──────────┬─────┬─────┐
  │   thread_id:54      │  epoch:2 │ age │ 101 │   ← 101 (偏向锁)
  └─────────────────────┴──────────┴─────┴─────┘

轻量级锁:
  ┌───────────────────────────────────┬─────┐
  │   指向栈中 Lock Record 的指针       │ 00  │   ← 00 (轻量级锁)
  └───────────────────────────────────┴─────┘

重量级锁:
  ┌───────────────────────────────────┬─────┐
  │   指向 ObjectMonitor 的指针         │ 10  │   ← 10 (重量级锁)
  └───────────────────────────────────┴─────┘
```

### 锁升级流程

```
        新建对象
           │
           ▼
        ┌──────┐
        │ 无锁  │  ← Mark Word 最后 3 位 = 001
        └──┬───┘
           │ 线程 A 第一次访问同步块
           ▼
        ┌──────┐
        │偏向锁 │  ← Mark Word 存 thread_id，下次同一线程来直接通过
        └──┬───┘
           │ 线程 B 也来竞争（Mark Word 里的 thread_id 不是 B）
           ▼
        ┌──────┐
        │轻量级│  ← CAS 争夺 Lock Record。线程自旋等待（默认自旋次数，自适应）
        │ 锁   │     自旋成功 → 获得锁；自旋失败次数多 →
        └──┬───┘
           │ 自旋超时 / 竞争激烈
           ▼
        ┌──────┐
        │重量级│  ← 膨胀为 ObjectMonitor，未抢到的线程进入 EntryList 阻塞
        │ 锁   │     靠操作系统的 mutex，线程挂起/唤醒有上下文切换开销
        └──────┘
```

### synchronized vs ReentrantLock 对比

| 维度 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现层 | JVM C++ (monitorenter/exit 字节码) | Java API (AQS + CAS) |
| 释放 | **自动**（JVM 保证，即使抛异常） | **手动** `lock.unlock()` 必须写在 finally |
| 可中断 | 不可（线程死等） | `lockInterruptibly()` |
| 超时获取 | 不支持 | `tryLock(3, SECONDS)` |
| 公平锁 | 只有非公平 | 可选 `new ReentrantLock(true)` |
| 条件变量 | 1 个（wait/notify，绑定 Object） | 多个 `Condition`（一个 Lock 多个 Condition） |
| 性能 | 1.6 优化后接近 | 低竞争时略优 |

**面试话术**：「90% 场景用 `synchronized` 就够了——简单、自动释放、JVM 优化透明。需要可中断、超时、公平锁、多个条件变量时才选 `ReentrantLock`。面试官喜欢问『什么时候选 Lock』，答案就是『synchronized 做不到的那些场景』。」

---

## 五、volatile + JMM — 可见性和有序性

### 一句话

volatile 保证**可见性**（一个线程改了，其他线程立即可见）和**有序性**（禁止指令重排），但**不保证原子性**。

### JMM 模型

```
        线程 1                      主内存                    线程 2
    ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
    │ 工作内存      │   read   │  共享变量     │   read   │ 工作内存      │
    │ (CPU缓存)    │ ◄────── │  x = 10      │ ──────► │ (CPU缓存)    │
    │ x = 10       │ ──────► │  y = 20      │ ◄────── │ x = 10       │
    │              │  write   │              │  write   │              │
    └──────────────┘          └──────────────┘          └──────────────┘
    
    问题：线程 1 改了 x 还没写回主内存，线程 2 读到的还是旧值 → 可见性问题
          编译器/CPU 可能重排指令，执行顺序 ≠ 代码顺序 → 有序性问题
```

### 四种内存屏障

| 屏障类型 | 作用 | 类比 |
|---------|------|------|
| **LoadLoad** | Load1; LoadLoad; Load2 → Load1 一定在 Load2 之前完成 | 排队，前面的读完后面才能读 |
| **StoreStore** | Store1; StoreStore; Store2 → Store1 一定在 Store2 之前刷回 | 排队，前面的写完后面才能写 |
| **LoadStore** | Load1; LoadStore; Store2 → 先读完才能写 | 先看再改 |
| **StoreLoad** | Store1; StoreLoad; Load2 → 写完才能读（最重的屏障） | 全局刷新 |

volatile 写：前面插 StoreStore，后面插 StoreLoad
volatile 读：前面插 LoadLoad，后面插 LoadStore

### 单例 DCL 为什么两次判空、为什么要 volatile

```java
public class Singleton {
    // volatile 防止指令重排：
    // instance = new Singleton() 分为三步：
    //   1. 分配内存空间
    //   2. 调用构造方法初始化对象
    //   3. instance 引用指向内存地址
    // 没有 volatile → 步骤 2 和 3 可能重排 → 其他线程拿到未初始化的对象！
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {              // 第一重检查：避免不必要的加锁
            synchronized (Singleton.class) {
                if (instance == null) {      // 第二重检查：防止并发创建多个
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### volatile 和 Atomic 的分工

```
volatile int count = 0:
    count++  ← 非原子！读→改→写三步，线程不安全

AtomicInteger count = new AtomicInteger(0):
    count.incrementAndGet()  ← CAS 原子操作，线程安全

选型建议：
    简单标志位(isRunning, initialized) → volatile
    需要递增/递减/复合操作 → AtomicInteger/Long/Reference
    复杂状态管理 → synchronized / ReentrantLock
```

**面试话术**：「volatile 的底层是 CPU 的缓存一致性协议（MESI）和内存屏障。x86 的 lock 前缀指令会锁总线或缓存行，强制刷新到主内存。DCL 里 volatile 防的是 `new Singleton()` 的指令重排——这个如果不理解透，面到一半就会被追问死。」

---

## 六、AQS — JUC 并发工具的地基

### 一句话

AQS 是所有 JUC 锁和同步器的**模板方法框架**。ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock 全基于它。

### AQS 的两大支柱

```
AQS = volatile int state + CLH 双向队列

    state: 同步状态
        ReentrantLock   → state = 0(未锁) / ≥1(重入次数)
        Semaphore       → state = 许可数量
        CountDownLatch  → state = 剩余计数
        ReadWriteLock   → state 高16位=读锁数，低16位=写锁数

    CLH 队列:
        head(哨兵) ← Node(T1, SIGNAL) ← Node(T2, SIGNAL) ← Node(T3, 0) ← tail
        不存线程     等待被唤醒          等待被唤醒          队尾
```

### 公平锁 vs 非公平锁 — 一行代码的区别

```java
// 公平锁的 tryAcquire：
protected final boolean tryAcquire(int acquires) {
    if (getState() == 0) {
        // 关键：先检查有没有人在排队！
        if (!hasQueuedPredecessors() &&       // ← 这一行就是公平的代价
            compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    }
    ...
}

// 非公平锁的 tryAcquire：
protected final boolean tryAcquire(int acquires) {
    if (getState() == 0) {
        if (compareAndSetState(0, acquires)) {  // ← 直接抢，不看队伍！
            setExclusiveOwnerThread(current);
            return true;
        }
    }
    ...
}
```

### CountDownLatch vs CyclicBarrier

```
CountDownLatch:                         CyclicBarrier:
  一次性，计数到 0 就不能重置              可重复使用（循环屏障）
  一个线程 await()，其他 countDown()       所有线程互相 await()

  Thread1 ──countDown()──┐               Thread1 ──await()──┐
  Thread2 ──countDown()──┤               Thread2 ──await()──┤
  Thread3 ──countDown()──┤               Thread3 ──await()──┤
                          ▼                                  ▼
  Main ────await()────────→ 继续            全部到齐 → 同时继续
```

**面试话术**：「AQS 的精髓在于模板方法模式——`tryAcquire`/`tryRelease` 留给子类实现具体语义，AQS 自己搞定排队、阻塞、唤醒这些通用逻辑。公平锁和非公平锁的差异只有一行 `hasQueuedPredecessors()`，但性能差异很大——非公平锁少一次队列检查，吞吐更高，是默认选项。」

---

## 七、JVM GC — 从算法到收集器

### 一句话

JVM 自动回收堆里无用的对象。核心三问：**怎么判断该回收**（可达性分析）、**怎么回收**（算法）、**谁来回收**（收集器）。

### 可达性分析

```
                    GC Roots (根对象集合)
                   ╱    │     │    ╲
                  ╱     │     │     ╲
                 ▼      ▼     ▼      ▼
              对象A   对象B   对象C   静态变量
                │              │
                ▼              ▼
              对象D          对象E
                │
                ▼
              对象F

    对象 G、H  没有任何引用链连接 GC Roots  →  不可达 → 可回收 ✗
```

### 四种 GC 算法 + 图解

```
① 标记-清除 (Mark-Sweep):
  标记所有可达对象 → 清除未标记的
  ██░░██░░░░██  →  ██  ██    ██   ← 碎片！大对象可能放不下
  缺点：碎片化

② 标记-复制 (Mark-Copy) — 新生代专用:
  ┌──────────┬──────────┐        ┌──────────┬──────────┐
  │ Eden     │ Survivor │   →    │ 空       │ Survivor │  存活对象搬过去
  │ ░░░███░  │ ░░░░     │        │          │ ████     │  Eden+From 清空
  └──────────┴──────────┘        └──────────┴──────────┘
  优点：无碎片，分配快（空闲区连续）
  缺点：浪费一半空间

③ 标记-整理 (Mark-Compact) — 老年代:
  ██░░██░░░░██  →  ████████░░░░  ← 存活对象移到一端，清除边界外
  优点：无碎片
  缺点：移动对象有开销（STW）

④ 分代收集 — 现代 JVM 的统一方案:
  新生代：标记-复制（对象朝生夕死，回收频繁但快）
  老年代：标记-清除/整理（对象活得久，回收慢但频率低）
```

### 新生代和老年代

```
              堆 Heap
  ┌────────────────────────────────┐
  │          新生代 Young            │      老年代 Old
  │  ┌──────┬──────┬──────┐        │  ┌──────────────┐
  │  │ Eden │  S0  │  S1  │        │  │              │
  │  │ 80%  │ 10%  │ 10%  │        │  │   长命对象    │
  │  └──────┴──────┴──────┘        │  │              │
  │  新对象出生地  复制算法          │  └──────────────┘
  └────────────────────────────────┘
                ↑                      ↑
           Minor GC               Major/Full GC
           频繁(几十ms)            偶尔(几百ms~几s)
           复制算法快              标记-整理慢
```

### 垃圾收集器速查

| 收集器 | 代 | 算法 | 特点 | 适用 |
|--------|:--:|------|------|------|
| Serial | 新 | 复制 | 单线程，简单 | 小型应用 |
| Parallel | 新 | 复制 | 多线程，吞吐优先 | 后台计算 |
| CMS | 老 | 标记-清除 | 并发低停顿 | 响应优先（已淘汰） |
| **G1** | 混合 | 分区+复制 | 可控暂停时间，分 Region | **JDK 9+ 默认** |
| ZGC | 全堆 | 染色指针 | 亚毫秒级停顿，超大堆 | JDK 21+ 低延迟 |

### G1 核心概念

```
G1 把堆分成大小相等的 Region（默认 2048 个）：

┌──┬──┬──┬──┬──┬──┬──┬──┐
│E │E │S │O │E │H │O │E │   E=Eden  S=Survivor  O=Old  H=Humongous(大对象)
├──┼──┼──┼──┼──┼──┼──┼──┤
│O │E │S │E │O │O │E │O │
└──┴──┴──┴──┴──┴──┴──┴──┘

每次 GC 选垃圾最多的几个 Region 回收（Garbage First）
不要求一次回收整个老年代，停顿时间可控
```

**面试话术**：「GC 调优的实践经验——大多数情况默认 G1 就够。线上遇到 Full GC 频繁：先看是不是有大对象直接进老年代（Humongous），再看 Survivor 区是不是太小导致过早晋升。基本上-Xmx 设物理内存的 60-70%，-Xms 和 -Xmx 一样大避免动态扩缩。」

---

## 八、Spring IoC & AOP — 不只是背概念

### 一句话

IoC 把对象的创建和依赖交给 Spring 容器管理，AOP 把横切逻辑（事务/日志/权限）从业务代码中抽离。

### IoC 容器的核心数据结构

```java
// Spring IoC 容器本质是：一个巨大的 ConcurrentHashMap + 一系列后置处理器
//
// DefaultListableBeanFactory 的核心：
private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(256);
//   beanName → BeanDefinition（类的元信息：scope、lazy、dependsOn、initMethod...）

private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);
//   beanName → 单例实例（一级缓存）

// 创建 Bean 时经过的处理器链：
//   实例化 → 属性填充 → BeanPostProcessor#postProcessBeforeInitialization
//                     → @PostConstruct / InitializingBean
//                     → BeanPostProcessor#postProcessAfterInitialization
//                        └─ 这里可能返回代理对象！（AOP 的切入点）
```

### AOP 的代理原理

```
目标类实现了接口：
    ┌──────────────┐
    │ UserService  │ (接口)
    └──────┬───────┘
           │
    ┌──────▼───────┐          ┌──────────────┐
    │UserServiceImpl│          │  JdkDynamic   │  生成接口实现类
    │  (目标对象)   │  ──→    │  AopProxy     │  $Proxy123 implements UserService
    └──────────────┘          └──────────────┘

目标类没实现接口：
    ┌──────────────┐          ┌──────────────┐
    │ OrderService │          │  CglibAopProxy│  生成目标类的子类
    │  (目标对象)   │  ──→   │  OrderService$$│  extends OrderService
    └──────────────┘          │  EnhancerBy.. │  final 方法不能代理！
                              └──────────────┘
```

### @Transactional 怎么工作的

```
@Transactional
public void transfer() {
    dao.debit();     ← 这行前后 AOP 做了什么？
    dao.credit();
}

实际执行：
    ├─ AOP 开启事务：conn.setAutoCommit(false)
    ├─ 执行业务方法 transfer()
    ├─ 成功 → conn.commit()
    └─ 异常(RuntimeException/Error) → conn.rollback()

注意：同一个类内部方法调用不走代理！
    @Transactional
    public void methodA() {
        this.methodB();     ← 直接调用 this，绕过了代理，@Transactional 不生效！
    }

    @Transactional
    public void methodB() { ... }
    // 解决方案：注入自己 → 用代理对象调用 或 把 methodB 抽到另一个 Service
```

**面试话术**：「Spring 的核心不是 IoC 和 AOP 的定义，而是它们怎么实现——IoC 底层是 ConcurrentHashMap + 三级缓存解决循环依赖，AOP 底层是 BeanPostProcessor 的后置处理生成代理对象。`@Transactional` 失效最常见的两个场景：同类方法调用不走代理、异常被 try-catch 吞了没抛出来。」

---

## 九、RAG — 企业落地最多的 AI 技术

### 一句话

不靠 LLM 自己的记忆，每次回答前先从你的知识库搜索相关内容，拼进 Prompt 再回答——降低幻觉、数据不出服务器、秒级更新知识。

### 完整流水线

```
  ═══════════ 离线阶段：知识入库 ═══════════
  │
  │  PDF/Word/网页/Markdown  ──→  Loader 加载  ──→  Chunking 切块
  │                                                      │
  │                                              每块 500-1000 字符
  │                                              重叠 10-20% 防止语义断开
  │                                                      │
  │                                                      ▼
  │                                              Embedding 模型
  │                                              文本 → 1536维向量
  │                                                      │
  │                                                      ▼
  │                                              向量数据库存储
  │                                              Chroma / Milvus / pgvector
  │
  ═══════════ 在线阶段：用户提问 ═══════════
  │
  │  用户问题 ──→ Embedding(问题)  ──→  向量相似度搜索  ──→  Top-K 文档
  │       "公积金怎么提取"           "公积金"的向量         最相关的 5 段文档
  │                                                              │
  │                                                              ▼
  │  Prompt = "参考以下文档回答：\n[文档1]\n[文档2]...\n\n问题：公积金怎么提取"
  │                                                              │
  │                                                              ▼
  │                                                         LLM 生成答案
  │                                                         "根据规定，您需要..."
```

### RAG vs 微调 — 90% 企业选 RAG 的原因

| 维度 | RAG | 微调 (Fine-tuning) |
|------|-----|-------------------|
| 更新知识 | **秒级**，重新导入 | 天级，需重新训练 |
| 数据安全 | 文档不出服务器 | 需发送给训练方 |
| 幻觉 | **低**（有文档依据） | 中（模型仍可编造） |
| 成本 | 低（向量数据库 + Embedding） | 高（GPU 训练） |
| 适用 | 知识问答、文档助手 | 改变输出风格/格式 |

**核心难点不在代码，在策略**：

- **Chunking 策略**：切多大？重叠多少？按段落还是按语义？这比模型选择影响更大
- **检索精度**：只用向量相似度？还是加 BM25 关键词检索做混合？需不需要重排序(Rerank)？
- **Embedding 模型选型**：中文场景 `text-embedding-3-large` vs `bge-large-zh-v1.5`，效果差异大

**面试话术**：「我们项目用 RAG 解决企业知识库问答。核心踩坑经验是 Chunking 和检索。单纯按 500 字切块会导致上下文断裂，我们加了 20% 重叠 + 按 Markdown 标题层级切分。检索端用了混合检索——向量相似度 + BM25 关键词，再做 Rerank 重排序。」

---

## 十、Agent 全景 — 不只是聊天机器人

### 四层架构

```
            ┌─────────────────────────────────────┐
            │          AI Agent                    │
            │                                      │
            │  ┌─────────────────────────────┐     │
            │  │ 🧠 规划层 Planning             │     │
            │  │   ReAct推理 / 任务分解 / 反思   │     │
            │  └─────────────────────────────┘     │
            │            ↕                         │
            │  ┌─────────────────────────────┐     │
            │  │ 💾 记忆层 Memory               │     │
            │  │   短期(对话上下文)               │     │
            │  │   长期(向量数据库)               │     │
            │  └─────────────────────────────┘     │
            │            ↕                         │
            │  ┌─────────────────────────────┐     │
            │  │ 🔧 工具层 Tools                │     │
            │  │   Function Calling             │     │
            │  │   搜索 / 代码 / API / 数据库    │     │
            │  └─────────────────────────────┘     │
            │            ↕                         │
            │  ┌─────────────────────────────┐     │
            │  │ 🔄 执行循环 Agent Loop         │     │
            │  │   Observe → Think → Act        │     │
            │  └─────────────────────────────┘     │
            └─────────────────────────────────────┘
```

### Function Calling — Agent 从「说」到「做」的关键

```
 用户: "帮我查张三的订单"
   │
   ▼
 LLM 推理: "我需要调用数据库查询工具"
   返回: {
     "tool_calls": [{
       "function": "query_order",
       "arguments": {"user": "张三"}
     }]
   }
   │
   ▼
 你的代码执行:
   SELECT * FROM orders WHERE user = '张三'
   → 返回 [{id: 123, amount: 99, status: '已发货'}]
   │
   ▼
 把结果发回 LLM, LLM 用自然语言回答:
 "张三有一笔订单（编号123），金额99元，状态已发货"
```

### Agent 三种架构模式对比

| 模式 | 流程 | 适用场景 |
|------|------|---------|
| **ReAct** | Thought → Action → Observation → Thought → ... | 需要多步推理+工具调用的任务 |
| **Plan-Execute** | 先制定完整计划 → 逐步执行 | 复杂但可预测的任务 |
| **Reflection** | 执行 → 自我评价 → 修正 → 再执行 | 需要迭代优化的任务（如写代码） |

### Spring AI — Java 集成 AI 的标准方式

```java
// 和 Spring Data 一样的套路，只是把数据库换成了大模型

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

// application.yml 改一行换模型：
// spring.ai.openai.api-key: sk-xxx  →  deepseek
// spring.ai.openai.base-url: https://api.deepseek.com/v1
```

**面试话术**：「Agent 不是新技术栈，而是对现有系统的增强层。我用 Spring AI 的经验是：ChatClient 做对话、EmbeddingModel 做向量化、VectorStore 做检索——这三个接口覆盖了 80% 的 AI 集成需求。团队里 Java 开发不需要学 Python 就能上手。」

---

## 十一、面试现场话术

### 自我介绍（60 秒版）

> 「面试官好，我是 XXX，X 年 Java 后端开发。主要技术栈 Spring Boot + MySQL + Redis，熟悉并发编程和 JVM 调优。最近一年在系统学习 AI/Agent，做过几个实战项目——用 Spring AI 给内部系统集成了智能问答、从零搭建过 RAG 知识库、还用 DeepSeek API 做过桌面 AI 写作工具。我认为 AI 不是取代 Java，而是让 Java 系统多一层智能能力。这个岗位正好对 AI 有兴趣，是我在深入的方向。」

### 回答"为什么 HashMap 用红黑树不用 AVL"

> 「红黑树是弱平衡，AVL 是严格平衡。HashMap 增删频繁，红黑树插入最多旋转 3 次，AVL 可能 O(log n) 次。JDK 选择红黑树是用『插入性能』换『极限平衡』，对 HashMap 这种读多写多场景更合适。」

### 回答"你们的 AI 项目有什么实际价值"

> 「内部知识库 RAG 项目上线后，新人问『xx 接口怎么调』这种问题减少了 60%——以前要翻 Wiki 或者找人问，现在直接对话就能得到准确答案。技术不复杂，但工程细节多——切块策略调了四版，检索从纯向量改成混合检索后准确率提了 15 个点。」

### 反问面试官的好问题

- 「团队目前 AI 在哪些场景落地了？主要在探索阶段还是已经有线上服务？」
- 「Java 系统接 AI，团队倾向 Spring AI 还是自研对接？」
- 「这个岗位未来一年，最希望我在 AI 方向做到什么程度？」

---

## 十二、24 小时速查清单

### Java（必背）

- [ ] HashMap：数据结构演进、位与取模、扰动函数、树化条件、扩容免重 hash
- [ ] ConcurrentHashMap：CAS 放 Node、synchronized 锁头节点、读无锁、分段计数
- [ ] 线程池：7 参数 + 执行流程 + Worker 取任务逻辑 + 拒绝策略
- [ ] synchronized：Mark Word 锁标记、偏向→轻量→重量升级流程
- [ ] volatile：可见性+有序性+不保证原子性、DCL 为什么用、内存屏障
- [ ] AQS：state + CLH 队列、公平锁 vs 非公平锁区别、state 在不同实现中的含义
- [ ] JVM GC：可达性分析、四种算法、Minor GC vs Full GC、G1 原理
- [ ] Spring AOP：JDK 动态代理 vs CGLIB、@Transactional 失效两个场景

### AI（加分）

- [ ] Agent = LLM + Memory + Tools + Planning
- [ ] RAG 完整流水线（离线+在线）+ RAG vs 微调对比
- [ ] Function Calling 数据流（LLM 不执行工具，只输出调用意图）
- [ ] Spring AI 三大抽象（ChatClient/Embedding/VectorStore）

### 项目故事

- [ ] 自我介绍 60 秒
- [ ] 一个 AI 项目的完整经历（需求→方案→踩坑→效果）
- [ ] 3 个反问面试官的问题

---

> 你不是在「背题」，你是在「把做过的项目讲清楚」。Java 底子 + AI 实战 = 大部分候选人没有的组合优势。加油 🔥
