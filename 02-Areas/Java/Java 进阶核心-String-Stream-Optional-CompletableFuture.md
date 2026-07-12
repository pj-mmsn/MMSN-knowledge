---
title: Java 进阶核心 — String/Stream/Optional/CompletableFuture
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [Java, 并发, 基础]
difficulty: 进阶
---

# Java 进阶核心 — String/Stream/Optional/CompletableFuture

> **一句话**:这些是 Java 面试的「基础进阶」——String 不可变、Stream 惰性求值、Optional 防 NPE、CompletableFuture 异步编排。

---

## String — 不可变性

```java
String s1 = "hello";
s1 = s1 + " world";  // s1 指向了新对象，原来的 "hello" 还在常量池

// ❓ 为什么设计成不可变？
// ① 安全：String 做 HashMap 的 key、存密码，不可变就不可被篡改
// ② 线程安全：天然线程安全，不需要同步
// ③ 字符串常量池：同一字符串可以复用，省内存
```

### String vs StringBuilder vs StringBuffer

| | String | StringBuilder | StringBuffer |
|------|--------|--------------|-------------|
| 可变 | ❌ 不可变 | ✅ | ✅ |
| 线程安全 | ✅ | ❌ | ✅ (synchronized) |
| 性能 | 拼接时差 | **最快** | 慢（加锁） |
| 使用 | 少量拼接 | **单线程拼接** | 多线程拼接 |

```java
// ❌ 循环拼接 String → 每次循环创建新对象，O(n²) 性能
String s = "";
for (int i = 0; i < 10000; i++) s += i;

// ✅ 用 StringBuilder → 只一个对象，O(n)
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10000; i++) sb.append(i);
```

## equals vs hashCode — 铁律

```java
// 两条铁律：
// ① equals 相等的两个对象，hashCode 必须相等
// ② hashCode 相等的两个对象，equals 不一定相等（哈希冲突）

// ❌ 只重写 equals → HashMap 里 put 进去 get 不出来！
// ✅ 必须两个一起重写

@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User)) return false;
    User user = (User) o;
    return id == user.id && Objects.equals(name, user.name);
}

@Override
public int hashCode() {
    return Objects.hash(id, name);  // 用 JDK 工具方法，保证一致性
}
```

## 异常处理

```java
// ❓ 受检异常 vs 非受检异常
// 受检(Exception)：必须 try-catch 或 throws → IOException, SQLException
// 非受检(RuntimeException)：不强制处理 → NPE, IAE

// ❓ finally 一定会执行吗？
// 99% 会。除非：① System.exit(0) ② JVM 崩溃 ③ 守护线程退出

// ❓ try-with-resources（JDK 7+）
try (FileInputStream fis = new FileInputStream("a.txt");
     BufferedReader br = new BufferedReader(new InputStreamReader(fis))) {
    return br.readLine();
}  // 自动 close()，即使抛异常也会关 — 比 finally 优雅
```

---

## Stream — 函数式编程

```java
List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5, 6);

// 过滤 + 映射 + 收集
List<Integer> evenSquares = nums.stream()
    .filter(n -> n % 2 == 0)     // 中间操作：惰性求值
    .map(n -> n * n)              // 中间操作
    .collect(Collectors.toList());// 终止操作：触发计算
// → [4, 16, 36]

// 常用操作速查：
nums.stream().distinct()                     // 去重
nums.stream().sorted()                       // 排序
nums.stream().limit(3)                       // 取前3
nums.stream().skip(2)                        // 跳过前2
nums.stream().anyMatch(n -> n > 5)           // 是否有满足的
nums.stream().reduce(0, Integer::sum)         // 聚合（求和）
nums.stream().collect(Collectors.groupingBy(  // 分组
    n -> n % 2 == 0 ? "偶数" : "奇数"))
```

### Stream 惰性求值

```java
// Stream 的中间操作是惰性的——终止操作不来，中间操作不执行
List<String> result = nums.stream()
    .filter(n -> {
        System.out.println("filter: " + n);
        return n > 3;
    })
    .map(n -> {
        System.out.println("map: " + n);
        return n * 10;
    })
    .collect(Collectors.toList());

// 输出顺序（不是先全部 filter 再全部 map，而是一条流到底）：
// filter: 1  (false → 短路)
// filter: 2  (false → 短路)
// filter: 3  (false → 短路)
// filter: 4  → map: 4
// filter: 5  → map: 5
// filter: 6  → map: 6
```

---

## Optional — 防 NPE

```java
// ❌ 旧时代
User user = findById(id);
if (user != null) {
    String name = user.getName();
    if (name != null) return name.toUpperCase();
}
return "未知";

// ✅ Optional 链式
return Optional.ofNullable(findById(id))
    .map(User::getName)
    .map(String::toUpperCase)
    .orElse("未知");

// 四个核心方法：
Optional.of(value)       // value 不能为 null → 抛 NPE
Optional.ofNullable(val) // value 可为 null → 返回 empty
orElse(defaultVal)       // null 时返回默认值
orElseGet(() -> ...)     // null 时惰性计算默认值（推荐！）

// ⚠️ orElse vs orElseGet
// orElse("default") → 不管 null 不 null，"default" 都会执行
// orElseGet(() -> expensiveOp()) → 只在 null 时才执行 expensiveOp
// 默认值有副作用或开销大时，一定用 orElseGet
```

---

## CompletableFuture — 异步编排

```java
// 基础用法
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return fetchFromDB();  // 在 ForkJoinPool 线程执行
});

// 链式编排
CompletableFuture<String> result = CompletableFuture
    .supplyAsync(() -> fetchOrder(123))           // ① 查订单
    .thenApply(order -> order.getUserId())         // ② 取用户ID
    .thenCompose(userId -> fetchUser(userId))      // ③ 查用户信息（异步）
    .exceptionally(ex -> "查询失败: " + ex.getMessage()); // ④ 异常兜底

// 并发组合
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> fetchA());
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> fetchB());

// 等两个都完成
CompletableFuture<String> combined = f1.thenCombine(f2, (a, b) -> a + b);

// 任意一个完成就行
CompletableFuture<Object> any = CompletableFuture.anyOf(f1, f2);
```

### Future vs CompletableFuture

| | Future | CompletableFuture |
|------|--------|-------------------|
| 获取结果 | `get()` **阻塞** | `thenApply()` **回调**，不阻塞 |
| 链式调用 | ❌ | ✅ |
| 组合 | ❌ | ✅ `thenCombine`/`anyOf` |
| 异常处理 | ❌ | ✅ `exceptionally` |
| 手动完成 | ❌ | ✅ `complete()` |

---

## Java 8+ 新特性速查

| 版本 | 特性 | 一句话 |
|:--:|------|------|
| **8** | Lambda + Stream + Optional | **面试必问** |
| **8** | 接口 default 方法 | 接口可以有实现 |
| **9** | 模块化 (JPMS) | module-info.java |
| **10** | var 局部变量 | `var list = new ArrayList<String>()` |
| **11** | HttpClient | 标准 HTTP 客户端 |
| **14** | Record | `record Point(int x, int y){}` 替代 POJO |
| **17** | **LTS** | 长期支持版 |
| **17** | 密封类 sealed | `sealed class Shape permits Circle, Rect` |
| **21** | **虚拟线程 Virtual Threads** | 轻量线程，千万级并发 |
| **21** | Switch 模式匹配 | switch 里直接解构对象 |

### 虚拟线程（Java 21，必问！）

```java
// 传统线程：1 个线程 ≈ 1MB 栈，万级就是瓶颈
// 虚拟线程：JVM 管理，百万级也不怕，不用池化

// 创建虚拟线程
Thread.startVirtualThread(() -> {
    System.out.println("I'm a virtual thread!");
});

// 用虚拟线程的 ExecutorService
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> fetchFromAPI());
}
```

## 面试话术

「Java 高阶我重点掌握了 Stream 的函数式编程、Optional 的 NPE 防护、CompletableFuture 的异步编排。最近在关注 Java 21 的虚拟线程——它把线程管理从 OS 层面提到 JVM 层面，让高并发编程简单了一个数量级，不需要线程池调参了。」
