---
title: 消息队列 MQ — Kafka 核心概念
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [分布式, 架构, 实战]
difficulty: 进阶
---

# 消息队列 MQ

> **一句话**:MQ 解耦系统间直接调用，削峰填谷保护 DB，异步处理提升响应速度。Kafka 是分布式日志，百万 QPS。

## 为什么用 MQ — 三大场景

| 场景 | 传统 | MQ 后 |
|------|------|-------|
| **异步** | 注册+发短信+发邮件（串行 800ms） | 注册→扔消息（50ms），消费者异步处理 |
| **解耦** | 订单直接调库存/物流/积分 | 订单→MQ，各系统订阅 |
| **削峰** | 秒杀直接打 DB→打挂 | 请求进 MQ 排队，后端匀速消费 |

## Kafka 核心架构

```
Producer → Broker(Topic)
              ├── Partition 0 (Leader + Follower)
              ├── Partition 1
              └── Partition 2
                           ↓
                      Consumer Group
```

| 概念 | 说明 |
|------|------|
| Topic | 消息分类（类似 DB 表） |
| Partition | 分区，顺序追加写，**分区内有序** |
| Offset | 消息在分区中唯一位置 |
| ISR | 与 Leader 保持同步的副本集合 |

## 消息丢失怎么解决

| 环节 | 问题 | 配置 |
|------|------|------|
| Producer | 发送失败 | `acks=all` + `retries=3` |
| Broker | 宕机 | `replication.factor=3` + `min.insync.replicas=2` |
| Consumer | 未处理完就提交 | 关闭自动提交，手动 commit |

## 消息重复消费

- 幂等设计：唯一键、Redis setnx、业务状态机
- 消费端：先处理再手动提交 offset

## 面试追问

**Q: Kafka 为什么这么快？**
A: 顺序写磁盘（比随机写快 6000 倍）+ Page Cache + 零拷贝（sendfile）+ 批量压缩。

**Q: 怎么保证消息顺序？**
A: 同一个 key → 同一个 Partition（分区内有序），Consumer 单线程消费。
