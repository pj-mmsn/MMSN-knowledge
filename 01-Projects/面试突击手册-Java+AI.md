---
title: 面试突击手册 — Java开发 + AI开发（图解版）
created: 2026-07-09
updated: 2026-07-09
type: project
tags: [Java, AI, Agent, 职业规划, 面试]
---

# 🎯 面试突击手册 — Java + AI 图解版

> 每道题「一句话 → 图解 → 原理 → 源码细节 → 面试话术」完整链路。所有图表用 Mermaid 渲染。

---

## 一、HashMap — 面试第一题，问到源码才算及格

### 数据结构全景

```mermaid
graph TB
    subgraph HashMap["HashMap (JDK 1.8+)"]
        TABLE["⚡ table 桶数组<br/>容量=16（2的幂）"] --> I1["桶[0]"]
        TABLE --> I2["桶[1]"]
        TABLE --> I3["桶[2]"]
        TABLE --> I4["..."]
        TABLE --> I15["桶[15]"]

        I1 --> N1["Node(k1,v1)"]
        N1 -->|"next"| N2["Node(k2,v2)"]
        N2 -->|"next"| N3["Node(k3,v3) ← 链表"]

        I15 --> T1["TreeNode"]
        T1 --> T2["TreeNode"]
        T2 --> T3["TreeNode"]
        T1 -.->|"left"| T2
        T1 -.->|"right"| T3
    end

    style TABLE fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style T1 fill:#2d1b00,stroke:#ff9800,color:#fff
    style N1 fill:#0d3300,stroke:#4caf50,color:#fff
```

### 位运算：为什么容量必须是 2 的幂

HashMap 用 `(n - 1) & hash` 定位桶，代替 `hash % n`。

**位与 `&`**：两 bit 都是 1 结果才为 1。n 是 2 的幂 → n-1 二进制全是 1 → 保留 hash 全部低位 → 分布均匀。

```mermaid
flowchart LR
    subgraph "取模 vs 位与"
        MOD["hash % 16"] -->|"除法指令<br/>~30 CPU周期"| R1["结果 = 6"]
        AND["hash & 15"] -->|"1条 AND 指令<br/>~1 CPU周期"| R2["结果 = 6"]
    end

    subgraph "位与原理 (hash=214, n=16)"
        BIN["1101 0110 (214)"]
        MASK["0000 1111 (15 = n-1)"]
        RES["0000 0110 (= 6)"]
        BIN -->|"&"| RES
        MASK -->|"&"| RES
    end
```

**扰动函数**：高 16 位和低 16 位做异或（XOR），让高位也参与定位：

```java
// HashMap.hash() 源码
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

```mermaid
flowchart LR
    H["原始 hashCode<br/>1101 0110 0011 1001<br/>1010 0101 1110 0011"]
    H -->|"高16位"| HIGH["1101 0110 0011 1001"]
    H -->|"低16位"| LOW["1010 0101 1110 0011"]
    HIGH --> XOR["🔄 XOR (^)"]
    LOW --> XOR
    XOR --> FINAL["最终 hash<br/>0111 0011 1101 1010<br/>← 高位融入低位"]
```

### 红黑树五条铁律

```mermaid
graph TB
    ROOT["● 根节点 (永远黑色)"] --> R1["○ 红色节点"]
    ROOT --> R2["○ 红色节点"]
    R1 --> B1["● 黑色"]
    R1 --> B2["● 黑色"]
    R2 --> B3["● 黑色"]
    R2 --> B4["● 黑色"]

    RULE["📋 五条铁律<br/>1. 节点要么红要么黑<br/>2. 根永远黑<br/>3. 红节点孩子必须是黑<br/>4. 任意路径黑节点数相同<br/>5. NIL 叶子算黑色"]

    style ROOT fill:#1a1a1a,stroke:#fff,color:#fff
    style R1 fill:#cc0000,stroke:#ff4444,color:#fff
    style R2 fill:#cc0000,stroke:#ff4444,color:#fff
    style B1 fill:#1a1a1a,stroke:#888,color:#fff
    style B2 fill:#1a1a1a,stroke:#888,color:#fff
    style B3 fill:#1a1a1a,stroke:#888,color:#fff
    style B4 fill:#1a1a1a,stroke:#888,color:#fff
```

| 对比 | 链表 | 红黑树 | AVL 树 |
|------|:--:|:--:|:--:|
| 查找 | O(n) | O(log n) | O(log n) 稍快 |
| 插入 | O(1) | O(log n)，最多旋转 3 次 | O(log n)，可能多次旋转 |
| HashMap 的选择 | 短链表时用 | **链表 ≥8 时转** ✅ | 维护成本太高 |

### put 流程（源码级）

```mermaid
flowchart TD
    START(["put(key, value)"]) --> HASH["① hash(key)<br/>= key.hashCode() ^ (h>>>16)"]
    HASH --> IDX["② i = (n-1) & hash<br/>定位桶下标"]
    IDX --> EMPTY{"③ tab[i] == null?"}
    EMPTY -->|"✅ 是"| NEWNODE["tab[i] = newNode()<br/>直接放入"]
    EMPTY -->|"❌ 否"| EQUALS{"key 相等?<br/>(hash== && equals==)"}
    EQUALS -->|"✅ 覆盖"| OVERWRITE["覆盖旧 value"]
    EQUALS -->|"❌ 否"| ISTREE{"是 TreeNode?"}
    ISTREE -->|"🌲 是"| TREEINS["红黑树插入<br/>putTreeVal()"]
    ISTREE -->|"📋 否"| TRAVERSE["遍历链表<br/>尾插法"]
    TRAVERSE --> FOUND{"找到相同 key?"}
    FOUND -->|"✅"| OVERWRITE
    FOUND -->|"❌ 到尾部"| TAIL["尾插入<br/>binCount++"]
    TAIL --> CHECK8{"binCount ≥ 8?"}
    CHECK8 -->|"✅"| CHECK64{"数组长度 ≥ 64?"}
    CHECK64 -->|"✅"| TREEIFY["🌲 树化为红黑树"]
    CHECK64 -->|"❌"| RESIZE1["📦 只扩容不树化"]
    CHECK8 -->|"❌"| DONE1(["✅"])
    NEWNODE --> SIZECHECK
    OVERWRITE --> SIZECHECK
    TREEINS --> SIZECHECK
    TREEIFY --> SIZECHECK
    RESIZE1 --> SIZECHECK
    TAIL --> SIZECHECK{"④ ++size > threshold?"}
    SIZECHECK -->|"✅ 超阈值"| RESIZE2["📦 扩容 ×2<br/>容量翻倍，rehash"]
    SIZECHECK -->|"❌"| DONE2(["✅ 完成"])
    RESIZE2 --> DONE2

    style HASH fill:#4a148c,stroke:#ce93d8,color:#fff
    style TREEIFY fill:#e65100,stroke:#ff9800,color:#fff
    style RESIZE2 fill:#b71c1c,stroke:#ef5350,color:#fff
```

### 扩容时元素怎么搬（JDK 1.8 优化）

```mermaid
flowchart LR
    subgraph OLD["旧数组 容量=16"]
        O0["桶[0]"]
        O1["桶[1]"]
        O5["桶[5] ← key所在"]
        O15["桶[15]"]
    end

    O5 --> CHECK{"hash & oldCap<br/>= hash & 16"}
    CHECK -->|"== 0"| STAY["→ 新桶[5]<br/>原位不动"]
    CHECK -->|"!= 0"| MOVE["→ 新桶[5+16]=[21]<br/>原下标+旧容量"]

    subgraph NEW["新数组 容量=32"]
        N0["桶[0]"]
        N5["桶[5] ← 部分元素留这"]
        N15["桶[15]"]
        N21["桶[21] ← 部分元素搬这"]
        N31["桶[31]"]
    end

    STAY --> N5
    MOVE --> N21

    style OLD fill:#1a237e,stroke:#5c6bc0,color:#fff
    style NEW fill:#004d40,stroke:#4db6ac,color:#fff
```

**面试话术**：「HashMap 有三个理解层次——第一层背数据结构，第二层讲清楚位运算和扰动函数，第三层能说出扩容时只需判断 `hash & oldCap` 决定去留、不需要重新 hash。面试官从你回答的深度就能判断你是背的还是真看过源码。」

---

## 二、ConcurrentHashMap — 高并发安全的精髓

### 锁策略演进

```mermaid
graph TB
    subgraph JDK7["JDK 1.7: Segment 分段锁"]
        S0["Segment[0]<br/>🔒 ReentrantLock"]
        S1["Segment[1]<br/>🔒 ReentrantLock"]
        S15["Segment[15]<br/>🔒 ReentrantLock"]
        S0 --> H0["HashEntry 数组"]
        S1 --> H1["HashEntry 数组"]
        S15 --> H15["HashEntry 数组"]
    end

    subgraph JDK8["JDK 1.8: CAS + synchronized 锁单桶"]
        T0["桶[0]"]
        T1["桶[1]"]
        T2["桶[2]<br/>空 → CAS 放"]
        T3["桶[3]"]
        T16["桶[15]<br/>有数据 → 🔒 synchronized"]
    end

    JDK7 -->|"锁粒度: Segment级<br/>并发度: 16"| JDK8
    JDK8 -->|"锁粒度: 桶级<br/>并发度: 数组长度"| BETTER["✅ 性能提升"]

    style JDK7 fill:#4a0000,stroke:#ef5350,color:#fff
    style JDK8 fill:#0d3300,stroke:#66bb6a,color:#fff
    style BETTER fill:#1a237e,stroke:#42a5f5,color:#fff
```

### CAS 原理

```mermaid
sequenceDiagram
    participant T1 as 🧵 线程A
    participant MEM as 📍 内存 value
    participant T2 as 🧵 线程B

    Note over MEM: 初始 value = 10

    T1->>MEM: CAS(10 → 20)
    Note over MEM: 10 == 10 ✅
    MEM-->>T1: 成功！value = 20

    T2->>MEM: CAS(10 → 30)
    Note over MEM: 10 ≠ 20 ❌
    MEM-->>T2: 失败！value 已是 20

    T2->>T2: 🔄 自旋重试：重新读 value = 20
    T2->>MEM: CAS(20 → 30)
    Note over MEM: 20 == 20 ✅
    MEM-->>T2: 成功！value = 30
```

### put 流程（1.8 源码路径）

```mermaid
flowchart TD
    START(["put(key, value)"]) --> SPREAD["spread(key.hashCode())<br/>扰动函数"]
    SPREAD --> LOOP{"🔁 自旋 for(;;)"}
    LOOP --> INIT{"tab 未初始化?"}
    INIT -->|"✅"| INITTAB["initTable()<br/>CAS 设置 sizeCtl<br/>只有一个线程初始化"]
    INIT -->|"❌"| EMPTY{"tab[i] == null?"}
    EMPTY -->|"✅ 空桶"| CAS{"casTabAt()"}
    CAS -->|"✅ 成功"| DONE(["🚀 无锁！最快路径"])
    CAS -->|"❌ 失败"| LOOP
    EMPTY -->|"❌ 有数据"| MOVED{"hash == MOVED(-1)?"}
    MOVED -->|"✅ 正在扩容"| HELP["🤝 helpTransfer()<br/>帮忙搬运数据"]
    MOVED -->|"❌"| LOCK["🔒 synchronized(tab[i])<br/>锁住桶头节点"]
    LOCK --> CHECKAGAIN["再次检查 tab[i]"]
    CHECKAGAIN --> TREECHECK{"是 TreeBin?"}
    TREECHECK -->|"🌲"| TREEINS["红黑树插入"]
    TREECHECK -->|"📋"| LISTTRAV["遍历链表<br/>尾插法"]
    LISTTRAV --> FOUND{"找到相同 key?"}
    FOUND -->|"✅"| OVERWRITE["覆盖旧值"]
    FOUND -->|"❌"| TAILINSERT["尾插入"]
    TREEINS --> ADDCOUNT
    OVERWRITE --> ADDCOUNT
    TAILINSERT --> ADDCOUNT["addCount(1, binCount)<br/>检查是否需要扩容"]

    style CAS fill:#0d3300,stroke:#66bb6a,color:#fff
    style LOCK fill:#e65100,stroke:#ff9800,color:#fff
    style DONE fill:#0d3300,stroke:#66bb6a,color:#fff
    style HELP fill:#1a237e,stroke:#42a5f5,color:#fff
```

### 分段计数 — 怎么不靠锁统计 size

```mermaid
flowchart LR
    BC["baseCount"] -->|"CAS +1"| RESULT["size() 求和"]
    CC1["CounterCell[0]"] -->|"CAS +1"| RESULT
    CC2["CounterCell[1]"] -->|"CAS +1"| RESULT
    CC3["CounterCell[...]"] -->|"CAS +1"| RESULT

    subgraph "写操作"
        WRITE["线程随机选一个 Cell<br/>CAS 递增"]
    end

    WRITE -.->|"无竞争!"| CC1
    WRITE -.->|"无竞争!"| CC2
```

---

## 三、线程池 — 不只是背 7 参数

### 状态机

```mermaid
stateDiagram-v2
    [*] --> RUNNING : new ThreadPoolExecutor()
    RUNNING --> SHUTDOWN : shutdown()
    RUNNING --> STOP : shutdownNow()
    SHUTDOWN --> TIDYING : 队列为空
    STOP --> TIDYING : 所有线程终止
    TIDYING --> TERMINATED : terminated() 执行完
    TERMINATED --> [*]
```

### ctl 位打包

```
一个 AtomicInteger ctl 同时存储状态 + 线程数：
┌──────────────┬─────────────────────────────────┐
│  高 3 位      │  低 29 位                        │
│  运行状态      │  工作线程数 (workerCount)          │
└──────────────┴─────────────────────────────────┘
  RUNNING  = 111 (-1)
  SHUTDOWN = 000 (0)
  STOP     = 001 (1)
  TIDYING  = 010 (2)
  TERMINATED=011 (3)
```

### 核心执行流程

```mermaid
flowchart TD
    TASK(["submit(task)"]) --> WC{"workerCount<br/> < corePoolSize?"}
    WC -->|"✅ 是"| COREWORKER["📗 addWorker(task, true)<br/>创建核心线程<br/>（不管队列有没有空位）"]
    WC -->|"❌ 否"| OFFER{"workQueue.offer(task)"}
    OFFER -->|"✅ 入队成功"| QUEUED["任务在队列等待<br/>Worker 空闲时 getTask() 取走"]
    OFFER -->|"❌ 队列满"| MAX{"workerCount<br/> < maximumPoolSize?"}
    MAX -->|"✅ 是"| NONCORE["📙 addWorker(task, false)<br/>创建非核心线程<br/>keepAliveTime 后回收"]
    MAX -->|"❌ 也满了"| REJECT["🛑 触发拒绝策略"]

    style COREWORKER fill:#0d3300,stroke:#66bb6a,color:#fff
    style NONCORE fill:#e65100,stroke:#ff9800,color:#fff
    style REJECT fill:#b71c1c,stroke:#ef5350,color:#fff
```

### Worker 怎么取任务

```java
// Worker.run() 里不断循环
while (task != null || (task = getTask()) != null) {
    task.run();  // 执行任务
    task = null;
}

// getTask() 核心逻辑：
Runnable r = timed ?
    workQueue.poll(keepAliveTime, NANOSECONDS) :  // 超时等待（非核心线程）
    workQueue.take();                               // 阻塞等待（核心线程）
if (r == null) return null;  // 超时没拿到 → Worker 退出
```

### 四种拒绝策略

```mermaid
flowchart TD
    REJECTED["🛑 任务被拒绝"] --> POLICIES

    POLICIES --> ABORT["AbortPolicy (默认)<br/>throw RejectedExecutionException"]
    POLICIES --> CALLER["CallerRunsPolicy<br/>谁提交谁自己执行<br/>→ 降低任务提交速度"]
    POLICIES --> DISCARD["DiscardPolicy<br/>静默丢弃任务<br/>⚠️ 危险！没有任何通知"]
    POLICIES --> OLDEST["DiscardOldestPolicy<br/>丢弃队列最旧任务<br/>重新 submit 新任务"]

    style ABORT fill:#b71c1c,stroke:#ef5350,color:#fff
    style CALLER fill:#e65100,stroke:#ff9800,color:#fff
    style DISCARD fill:#4a0000,stroke:#ef5350,color:#fff
```

---

## 四、synchronized — 从 Mark Word 到锁升级

### Mark Word 内存布局（64位 JVM）

```mermaid
graph LR
    subgraph "无锁 (001)"
        N1["unused:25 | hash:31 | unused | age | 001"]
    end
    subgraph "偏向锁 (101)"
        B1["thread_id:54 | epoch:2 | age | 101"]
    end
    subgraph "轻量级锁 (00)"
        L1["指向栈中 Lock Record 的指针 | 00"]
    end
    subgraph "重量级锁 (10)"
        H1["指向 ObjectMonitor 的指针 | 10"]
    end

    N1 -->|"线程A第一次访问"| B1
    B1 -->|"线程B也来竞争"| L1
    L1 -->|"自旋超时/竞争激烈"| H1
```

### 锁升级流程

```mermaid
flowchart TD
    NEW(["新建对象"]) --> NOLOCK["🔓 无锁<br/>Mark Word: 001"]
    NOLOCK -->|"线程A首次访问同步块"| BIASED["🔹 偏向锁<br/>Mark Word 存 thread_id<br/>同线程再进直接通行"]
    BIASED -->|"线程B 也来竞争<br/>thread_id 不是 B"| LIGHT["🔸 轻量级锁<br/>CAS 争夺 Lock Record<br/>线程自适应自旋等待"]
    LIGHT -->|"自旋超时<br/>竞争激烈"| HEAVY["🔒 重量级锁<br/>膨胀为 ObjectMonitor<br/>未抢到的进 EntryList 阻塞<br/>靠 OS mutex，有上下文切换开销"]

    style NOLOCK fill:#0d3300,stroke:#66bb6a,color:#fff
    style BIASED fill:#1a237e,stroke:#42a5f5,color:#fff
    style LIGHT fill:#e65100,stroke:#ff9800,color:#fff
    style HEAVY fill:#b71c1c,stroke:#ef5350,color:#fff
```

### synchronized vs ReentrantLock

```mermaid
graph TB
    subgraph SYN["synchronized"]
        S1["JVM C++ 实现<br/>monitorenter/exit"]
        S2["自动释放 ✅<br/>异常也释放 ✅"]
        S3["不可中断 ❌"]
        S4["不支持超时 ❌"]
        S5["只有非公平锁"]
        S6["1个条件变量<br/>(wait/notify)"]
    end

    subgraph LOCK["ReentrantLock"]
        L1["Java API + AQS"]
        L2["手动释放 ⚠️<br/>必须 finally unlock"]
        L3["lockInterruptibly() ✅"]
        L4["tryLock(timeout) ✅"]
        L5["可选公平/非公平"]
        L6["多个 Condition<br/>精细线程调度"]
    end

    CHOICE["💡 90% 用 synchronized<br/>需要可中断/超时/多条件 → Lock"]
    SYN --> CHOICE
    LOCK --> CHOICE

    style SYN fill:#1a237e,stroke:#42a5f5,color:#fff
    style LOCK fill:#4a148c,stroke:#ce93d8,color:#fff
```

---

## 五、volatile + JMM

### JMM 内存模型

```mermaid
flowchart LR
    subgraph T1["🧵 线程1"]
        WM1["工作内存<br/>(CPU缓存)"]
    end
    subgraph MAIN["📍 主内存"]
        X["x = 10"]
        Y["y = 20"]
    end
    subgraph T2["🧵 线程2"]
        WM2["工作内存<br/>(CPU缓存)"]
    end

    WM1 <-->|"read / write"| MAIN
    WM2 <-->|"read / write"| MAIN

    PROBLEM["⚠️ 问题：
    线程1改了x没刷回主内存
    → 线程2读到旧值(可见性问题)
    → CPU/编译器重排指令(有序性问题)"]

    style MAIN fill:#0d3300,stroke:#66bb6a,color:#fff
    style PROBLEM fill:#b71c1c,stroke:#ef5350,color:#fff
```

### 四种内存屏障

```mermaid
flowchart LR
    subgraph "volatile 写"
        SW["StoreStore 屏障"] --> VW["写 volatile"]
        VW --> SL["StoreLoad 屏障<br/>(最重的屏障)"]
    end

    subgraph "volatile 读"
        LL["LoadLoad 屏障"] --> VR["读 volatile"]
        VR --> LS["LoadStore 屏障"]
    end
```

### DCL 为什么两次判空 + volatile

```mermaid
sequenceDiagram
    participant T1 as 🧵 线程1
    participant INST as Singleton.instance
    participant T2 as 🧵 线程2

    T1->>INST: ① if (instance == null) → true
    T1->>T1: ② synchronized 获取锁
    T1->>INST: ③ if (instance == null) → true ← 第二重检查
    T1->>INST: ④ instance = new Singleton()
    Note over T1,INST: ①分配内存 ②初始化 ③赋值引用<br/>volatile 防止②③重排!

    T2->>INST: if (instance == null) → false
    Note over T2: 拿到完整初始化好的对象 ✅

    T1->>T1: ⑤ synchronized 释放锁
```

---

## 六、AQS — JUC 的地基

### CLH 队列结构

```mermaid
flowchart LR
    HEAD["head<br/>🔹 哨兵节点<br/>(不存线程)"] -->|"next"| N1["Node(T1)<br/>waitStatus=SIGNAL<br/>🔔 需要唤醒后继"]
    N1 -->|"next"| N2["Node(T2)<br/>waitStatus=SIGNAL<br/>🔔 需要唤醒后继"]
    N2 -->|"next"| N3["Node(T3)<br/>waitStatus=0<br/>队尾"]
    N3 --> TAIL["tail"]

    N1 -.->|"prev ←"| HEAD
    N2 -.->|"prev ←"| N1
    N3 -.->|"prev ←"| N2

    style HEAD fill:#e65100,stroke:#ff9800,color:#fff
    style N1 fill:#1a237e,stroke:#42a5f5,color:#fff
    style N2 fill:#1a237e,stroke:#42a5f5,color:#fff
    style N3 fill:#1a237e,stroke:#42a5f5,color:#fff
    style TAIL fill:#e65100,stroke:#ff9800,color:#fff
```

### 公平锁 vs 非公平锁

```mermaid
flowchart TD
    TRY["tryAcquire(1)"]
    TRY --> FAIR{"公平锁?"}
    FAIR -->|"✅ 公平"| CHECKQUEUE{"hasQueuedPredecessors()?<br/>队列里有人在等?"}
    CHECKQUEUE -->|"有人等"| FAIL["排队去"]
    CHECKQUEUE -->|"没人等"| CAS_FAIR["CAS state 0→1"]
    FAIR -->|"❌ 非公平"| CAS_UNFAIR["直接 CAS state 0→1"]
    CAS_FAIR --> SUCCESS["🔒 获得锁"]
    CAS_UNFAIR --> SUCCESS

    style FAIL fill:#4a0000,stroke:#ef5350,color:#fff
    style SUCCESS fill:#0d3300,stroke:#66bb6a,color:#fff
```

---

## 七、JVM GC — 从算法到 G1

### 四种 GC 算法

```mermaid
flowchart LR
    subgraph MS["标记-清除"]
        M1["██░░██░░░░██"] --> M2["██  ██    ██"]
        M3["碎片化 ❌"]
    end
    subgraph MC["标记-复制 (新生代)"]
        C1["Eden ░░░███░"] --> C2["空 | Survivor ████"]
        C3["无碎片 ✅ 浪费空间 ⚠️"]
    end
    subgraph MCP["标记-整理 (老年代)"]
        P1["██░░██░░░░██"] --> P2["████████░░░░"]
        P3["无碎片 ✅ 移动开销 ⚠️"]
    end

    style MS fill:#4a0000,stroke:#ef5350,color:#fff
    style MC fill:#0d3300,stroke:#66bb6a,color:#fff
    style MCP fill:#1a237e,stroke:#42a5f5,color:#fff
```

### 新生代 vs 老年代

```mermaid
flowchart TB
    subgraph HEAP["堆 Heap"]
        subgraph YOUNG["新生代 Young"]
            EDEN["Eden (80%)<br/>🆕 新对象出生地"]
            S0["S0 (10%)"]
            S1["S1 (10%)"]
        end
        OLD["老年代 Old<br/>🏛️ 长命对象<br/>GC 15次没死的"]

        EDEN -->|"Minor GC<br/>复制到 Survivor"| S0
        S0 -->|"多次 GC 仍存活<br/>晋升到老年代"| OLD
    end

    style EDEN fill:#0d3300,stroke:#66bb6a,color:#fff
    style OLD fill:#4a148c,stroke:#ce93d8,color:#fff
```

### G1 收集器核心

```mermaid
flowchart TB
    subgraph G1["G1 堆布局"]
        R1["Eden"]
        R2["Eden"]
        R3["Survivor"]
        R4["Old"]
        R5["Eden"]
        R6["Humongous<br/>(大对象)"]
        R7["Old"]
        R8["Eden"]

        GC["🔄 每次 GC：选垃圾最多的 Region 回收<br/>不要求一次回收整个老年代<br/>停顿时间可控 ✅"]
    end

    style R4 fill:#4a0000,stroke:#ef5350,color:#fff
    style R7 fill:#4a0000,stroke:#ef5350,color:#fff
    style R6 fill:#e65100,stroke:#ff9800,color:#fff
```

---

## 八、Spring IoC & AOP

### AOP 代理原理

```mermaid
flowchart TB
    TARGET["目标对象<br/>UserServiceImpl"]

    TARGET -->|"实现了接口"| JDK["JDK 动态代理<br/>$Proxy123 implements UserService"]
    TARGET -->|"没实现接口"| CGLIB["CGLIB 代理<br/>UserService$$Enhancer<br/>extends UserServiceImpl<br/>⚠️ final方法不能代理"]

    JDK --> AOP_CHAIN["AOP 调用链"]
    CGLIB --> AOP_CHAIN

    AOP_CHAIN --> BEFORE["@Before"]
    BEFORE --> TARGET_METHOD["执行业务方法"]
    TARGET_METHOD --> AFTER["@After"]
    AFTER --> AROUND["@Around"]

    style JDK fill:#0d3300,stroke:#66bb6a,color:#fff
    style CGLIB fill:#1a237e,stroke:#42a5f5,color:#fff
```

### @Transactional 失效两大场景

```mermaid
flowchart TD
    SCENE1["❌ 场景1: 同类方法调用<br/>this.methodB() 不经过代理"]
    SCENE2["❌ 场景2: 异常被 try-catch 吞了<br/>Spring 感知不到异常"]

    SCENE1 --> FIX1["✅ 解决: 注入自己<br/>或抽到另一个 Service"]
    SCENE2 --> FIX2["✅ 解决: catch 里手动回滚<br/>TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()"]

    style SCENE1 fill:#b71c1c,stroke:#ef5350,color:#fff
    style SCENE2 fill:#b71c1c,stroke:#ef5350,color:#fff
    style FIX1 fill:#0d3300,stroke:#66bb6a,color:#fff
    style FIX2 fill:#0d3300,stroke:#66bb6a,color:#fff
```

---

## 九、RAG — 企业 AI 落地首选

### 完整流水线

```mermaid
flowchart TB
    subgraph OFFLINE["⚙️ 离线阶段：知识入库"]
        DOC["📄 PDF/Word/网页"]
        DOC --> LOAD["Loader 加载"]
        LOAD --> CHUNK["Chunking 切块<br/>每块 500-1000 字符<br/>重叠 10-20%"]
        CHUNK --> EMBED["Embedding 向量化<br/>文本 → 1536维向量"]
        EMBED --> STORE["向量数据库<br/>Chroma / Milvus / pgvector"]
    end

    subgraph ONLINE["⚡ 在线阶段：用户提问"]
        QUERY["❓ 用户问题<br/>'公积金怎么提取'"]
        QUERY --> QEMBED["问题 → 向量"]
        QEMBED --> SEARCH["🔍 向量相似度搜索<br/>Top-K 最相关文档"]
        SEARCH --> PROMPT["拼入 Prompt<br/>'参考以下文档回答...'"]
        PROMPT --> LLM["🤖 LLM 生成答案<br/>'根据规定，您需要...'"]
    end

    STORE -.->|"检索"| SEARCH

    style OFFLINE fill:#1a237e,stroke:#42a5f5,color:#fff
    style ONLINE fill:#0d3300,stroke:#66bb6a,color:#fff
    style LLM fill:#4a148c,stroke:#ce93d8,color:#fff
```

### RAG vs 微调

```mermaid
flowchart LR
    RAG["RAG<br/>✅ 秒级更新<br/>✅ 数据不出服务器<br/>✅ 幻觉低<br/>✅ 成本低<br/>✅ 90%企业首选"]
    FT["微调 Fine-tuning<br/>⚠️ 天级训练<br/>⚠️ 数据需外传<br/>⚠️ 仍可能编造<br/>⚠️ GPU成本高<br/>⚠️ 仅RAG不够时补充"]

    RAG -->|"首选"| CHOOSE["💡 企业选型"]
    FT -->|"补充"| CHOOSE

    style RAG fill:#0d3300,stroke:#66bb6a,color:#fff
    style FT fill:#e65100,stroke:#ff9800,color:#fff
```

---

## 十、Agent = LLM × 记忆 × 工具 × 规划

### 四层架构

```mermaid
flowchart TB
    USER["👤 用户给目标"] --> AGENT

    subgraph AGENT["🤖 AI Agent"]
        PLANNING["🧠 规划层<br/>ReAct推理 / 任务分解 / 反思"]
        MEMORY["💾 记忆层<br/>短期(对话上下文)<br/>长期(向量数据库)"]
        TOOLS["🔧 工具层<br/>Function Calling<br/>搜索 / 代码 / API"]
        LOOP["🔄 执行循环<br/>Observe → Think → Act"]
    end

    PLANNING <--> MEMORY
    PLANNING <--> TOOLS
    LOOP --> PLANNING

    style PLANNING fill:#4a148c,stroke:#ce93d8,color:#fff
    style MEMORY fill:#1a237e,stroke:#42a5f5,color:#fff
    style TOOLS fill:#0d3300,stroke:#66bb6a,color:#fff
    style LOOP fill:#e65100,stroke:#ff9800,color:#fff
```

### Function Calling 数据流

```mermaid
sequenceDiagram
    participant User as 👤 用户
    participant LLM as 🤖 LLM
    participant Code as ⚙️ 你的代码
    participant Tool as 🔧 真实工具

    User->>LLM: "帮我查张三的订单"
    LLM->>Code: 💭 返回 tool_calls:<br/>{function: "query_order",<br/> args: {user: "张三"}}
    Note over Code: LLM 不直接执行工具！<br/>只输出"想调用什么"
    Code->>Tool: SELECT * FROM orders<br/>WHERE user='张三'
    Tool-->>Code: [{id:123, amount:99, status:'已发货'}]
    Code-->>LLM: 工具结果返回给 LLM
    LLM->>User: "张三有一笔订单（编号123）<br/>金额99元，状态已发货"
```

### 三大架构模式

```mermaid
flowchart LR
    REACT["ReAct<br/>Thought→Action→Observe<br/>适合多步推理+工具调用"]
    PLAN["Plan-Execute<br/>先制定完整计划→逐步执行<br/>适合复杂可预测任务"]
    REFLECT["Reflection<br/>执行→自我评价→修正<br/>适合迭代优化（写代码）"]

    REACT --> CHOOSE["根据任务复杂度<br/>选择合适的模式"]
    PLAN --> CHOOSE
    REFLECT --> CHOOSE

    style REACT fill:#1a237e,stroke:#42a5f5,color:#fff
    style PLAN fill:#0d3300,stroke:#66bb6a,color:#fff
    style REFLECT fill:#4a148c,stroke:#ce93d8,color:#fff
```

---

## 十一、现场话术模板

### 自我介绍（60s）

> 「面试官好，我是 XXX，X 年 Java 后端开发。主要技术栈 Spring Boot + MySQL + Redis，熟悉并发编程和 JVM 调优。最近一年系统学习 AI/Agent，做过几个实战项目——用 Spring AI 集成智能问答、自建 RAG 知识库、DeepSeek API 项目。AI 不是取代 Java，而是给 Java 系统加一层智能能力。这个岗位正好是我在深入的方向。」

### 反问面试官

- 「团队目前 AI 在哪些场景落地了？」
- 「Java 系统接 AI，倾向 Spring AI 还是自研？」
- 「这个岗位未来一年最希望我在 AI 方向做到什么程度？」

---

## 十二、速查清单

### Java（必背 8 题）

- [ ] HashMap：位运算 + 扰动函数 + 红黑树 + 扩容免重 hash
- [ ] ConcurrentHashMap：CAS + synchronized 锁单桶 + 读无锁 + 分段计数
- [ ] 线程池：7 参数 + 执行流程 + Worker 取任务 + 拒绝策略
- [ ] synchronized：Mark Word + 锁升级四阶段
- [ ] volatile：可见性+有序性+内存屏障 + DCL
- [ ] AQS：state + CLH 队列 + 公平 vs 非公平
- [ ] JVM GC：四种算法 + Minor/Full GC + G1
- [ ] Spring AOP：JDK vs CGLIB + @Transactional 失效

### AI（加分 3 题）

- [ ] Agent = LLM + Memory + Tools + Planning
- [ ] RAG 离线+在线流水线 + RAG vs 微调
- [ ] Function Calling 数据流 + Spring AI 三大抽象

---

> 💪 你比 90% 候选人多的是：Java 八股有源码级理解 + AI 有真实项目。把图画到脑子里，面试时直接画给面试官看。
