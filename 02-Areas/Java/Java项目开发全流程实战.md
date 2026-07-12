---
title: Java项目开发全流程实战
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [实战, Spring, 架构]
difficulty: 进阶
---

# Java 项目开发全流程实战

> **一句话**:面试官问「你怎么启动一个新项目」不是问你 mvn archetype，是考察你**从需求到上线的全局把控力**。

## 项目启动六阶段

```mermaid
flowchart LR
    REQ["① 需求评审"] --> DESIGN["② 方案设计"]
    DESIGN --> DEV["③ 编码开发"]
    DEV --> TEST["④ 测试验证"]
    TEST --> DEPLOY["⑤ 部署上线"]
    DEPLOY --> OPS["⑥ 运维监控"]
```

## ① 需求评审（1-3 天）

| 要搞清楚的问题 | 为什么重要 |
|---------------|-----------|
| 核心业务流程是什么？ | 决定表结构和技术选型 |
| QPS 预估多少？日活多少？ | 决定单体还是微服务、要不要分库分表 |
| 数据量多大，增长多快？ | 决定分表策略和归档方案 |
| 有哪些外部系统要对接？ | 决定是否要 MQ、API 鉴权方式 |
| 有没有历史数据要迁移？ | 数据迁移方案比功能开发更坑 |

**输出**：需求文档 + 技术评审纪要。

## ② 方案设计（2-5 天）

### 数据库设计

```sql
-- 设计原则：
-- 1. 满足三范式但不教条（适当冗余减少 JOIN）
-- 2. 预留扩展字段（JSON 列或 extend 字段）
-- 3. 索引跟着查询走，不是越多越好

-- 例：订单表设计
CREATE TABLE t_order (
    id BIGINT PRIMARY KEY COMMENT '订单ID（雪花算法生成）',
    order_no VARCHAR(32) NOT NULL COMMENT '订单号（唯一）',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    product_id BIGINT NOT NULL COMMENT '商品ID',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '0待支付 1已支付 2已发货 3已完成 4已取消',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status_create (status, create_time),
    UNIQUE KEY uk_order_no (order_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 为什么要这些索引？
-- idx_user_id：查用户订单列表最频繁
-- idx_status_create：定时任务扫待支付超时订单、客服查待处理订单
-- uk_order_no：订单号唯一保证 + 对外暴露的查询入口
```

### 接口设计 — RESTful 规范

```java
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    // POST   /api/v1/orders          — 创建订单
    @PostMapping
    public Result<Long> create(@Valid @RequestBody CreateOrderRequest req) { ... }

    // GET    /api/v1/orders?userId=1&page=1&size=20  — 分页查询
    @GetMapping
    public Result<Page<OrderVO>> list(OrderQuery query) { ... }

    // GET    /api/v1/orders/{id}     — 查询详情
    @GetMapping("/{id}")
    public Result<OrderVO> detail(@PathVariable Long id) { ... }

    // PUT    /api/v1/orders/{id}/cancel  — 取消订单
    @PutMapping("/{id}/cancel")
    public Result<Void> cancel(@PathVariable Long id) { ... }
}
```

### 技术选型（一张表说清楚）

| 选型 | 选择 | 为什么不用另一个 |
|------|------|----------------|
| 框架 | Spring Boot 3.4 | Spring MVC 需要手动配太多东西 |
| ORM | MyBatis-Plus | JPA 对复杂查询不友好 |
| 缓存 | Redis | 单机 Caffeine 不能分布式共享 |
| MQ | RocketMQ | Kafka 偏日志场景，RocketMQ 事务消息更适业务 |
| 注册中心 | Nacos | Eureka 已停止维护 |
| RPC | Feign + LoadBalancer | Dubbo 稍重，内部服务间调用 Feign 够用 |

### 项目结构

```
src/main/java/com/xxx/order/
├── controller/     # 接口层：接收请求、参数校验、响应包装
├── service/        # 业务层：核心逻辑
│   └── impl/
├── manager/        # 通用业务处理层：组合多个 service 或第三方调用
├── dao/            # 数据访问层：MyBatis Mapper
│   └── mapper/
├── model/
│   ├── entity/     # 数据库实体
│   ├── dto/        # 数据传输对象
│   ├── vo/         # 视图对象（返回前端的）
│   └── query/      # 查询条件对象
├── config/         # 配置类
├── common/         # 公共：异常枚举、工具类、常量
└── aop/            # 切面：日志、权限
```

## ③ 编码开发（核心阶段）

### 开发顺序（别上来就写 Controller）

```
① 建表 + 索引  →  ② entity/mapper  →  ③ service（写单测！）
→  ④ controller  →  ⑤ 联调  →  ⑥ 补充文档
```

### 要写单元测试吗？

```java
// 面试这么说：
// "我会给核心 Service 写单测，不是追求覆盖率，是让核心逻辑可回归。
//  比如订单金额计算、状态流转——这些错了就是生产事故。"

@SpringBootTest
class OrderServiceTest {
    @Autowired private OrderService orderService;

    @Test
    void shouldFailWhenStockNotEnough() {
        // 库存不足时应该抛异常
        assertThrows(InsufficientStockException.class,
            () -> orderService.createOrder(1L, 999L, 999));
    }
}
```

### 开发规范

```
① 统一返回格式：Result<T> { code, message, data }
② 统一异常处理：@ControllerAdvice + 业务异常枚举
③ 参数校验：@Valid + @NotBlank/@NotNull/@Min
④ 日志规范：关键节点 info（创建订单），异常 error（带堆栈），敏感数据脱敏
⑤ SQL 上线前 Explain 检查
⑥ 所有接口加 Swagger/Knife4j 文档
```

## ④ 测试验证

| 测试类型 | 做了什么 | 工具 |
|---------|---------|------|
| 单元测试 | Service 核心逻辑 | JUnit5 + Mockito |
| 集成测试 | 接口全链路 | Postman / Apifox 集合 |
| 压力测试 | 核心接口 QPS | JMeter |
| 数据校验 | 迁移数据完整性 | SQL 脚本 |

## ⑤ 部署上线

```
上线 Checklist：
□ SQL 脚本（含回滚脚本）评审通过
□ 配置文件按环境分离（dev/test/prod）
□ 依赖的外部服务都健康（MQ/Redis/Nacos）
□ 灰度发布：先 1 台 → 观察 10 分钟 → 全量
□ 监控告警配置（接口耗时 P99、错误率、DB 慢查询）
□ 回滚方案就绪（代码回滚 + SQL 回滚）
```

## ⑥ 运维监控

| 监控什么 | 工具 | 告警阈值示例 |
|---------|------|------------|
| 接口 QPS + RT | Prometheus + Grafana | P99 > 1s 告警 |
| 错误率 | Sentry / 日志告警 | 错误率 > 1% 告警 |
| JVM | Arthas / VisualVM | Full GC > 1次/小时 |
| DB 慢查询 | Druid 监控 / 慢查询日志 | > 500ms |
| 业务指标 | 自定义埋点 | 支付成功率 < 99% |

---

## 面试话术

「启动一个项目，我的流程是：需求评审阶段搞清楚 QPS 和数据量，方案设计阶段出的第一份交付物是数据库设计——表结构加索引，因为 DB 设计定了后面很难改。然后定义接口文档前后端对齐，编码阶段先写 Service 单测保证核心逻辑正确。上线时一定灰度发布，每个阶段都有明确的 Checklist。」

### 追问：遇到过什么坑？

「数据迁移的坑最深。有一次迁移历史订单，自增 ID 冲突导致线上订单查不到。从那之后迁移前一定先在测试环境跑一遍全量 SQL，而且必须有回滚脚本。」
