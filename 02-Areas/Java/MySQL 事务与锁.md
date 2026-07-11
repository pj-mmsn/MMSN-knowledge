---
title: MySQL 事务与锁机制
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [数据库, 并发]
difficulty: 深入
---

# MySQL 事务与锁机制

> **一句话**:事务保证一组操作要么全成功要么全回滚（ACID），锁和 MVCC 是并发控制的两大手段。

## ACID

| 特性 | 含义 | 实现 |
|------|------|------|
| **A** 原子性 | 全成功或全回滚 | undo log |
| **C** 一致性 | 约束不被破坏 | DB+业务层面 |
| **I** 隔离性 | 并发互不干扰 | MVCC + 锁 |
| **D** 持久性 | 提交后不丢失 | redo log |

## 四种隔离级别

| 级别 | 脏读 | 不可重复读 | 幻读 |
|------|:--:|:--:|:--:|
| READ UNCOMMITTED | ✅ | ✅ | ✅ |
| READ COMMITTED | ❌ | ✅ | ✅ |
| **REPEATABLE READ** | ❌ | ❌ | ✅(部分) |
| SERIALIZABLE | ❌ | ❌ | ❌ |

> MySQL RR 通过 **MVCC（ReadView）+ Next-Key Lock** 解决大部分幻读。

## MVCC 原理

```
每条记录隐藏两列：
  DB_TRX_ID:  最近修改本行的事务 ID
  DB_ROLL_PTR: 指向 undo log 的回滚指针

ReadView: 事务开始时生成活跃事务列表
  如果 trx_id < min_trx_id → 可见（已提交）
  如果 trx_id > max_trx_id → 不可见
  如果属于活跃列表 → 不可见
  → 顺着 roll_ptr 找 undo 版本
```

## InnoDB 三种锁

| 锁 | 粒度 | 说明 |
|------|:--:|------|
| Record Lock | 单行 | 锁定索引记录 |
| Gap Lock | 区间 | 锁住索引间隙，防插入 |
| **Next-Key Lock** | 行+间隙 | Record+Gap，RR 默认 |

## 面试追问

**Q: `select ... for update` 什么时候锁表？**
A: 没走索引时！行锁依赖索引，没索引 → 升级为表锁。

**Q: 不可重复读 vs 幻读区别？**
A: 不可重复读是同一行被 UPDATE（值变了），幻读是多行或少行（INSERT/DELETE）。RR 用 MVCC 解前者，间隙锁解后者。
