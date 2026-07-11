---
title: 设计模式在 Spring 中的应用
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [Spring, 框架, 架构]
difficulty: 进阶
---

# 设计模式在 Spring 中的应用

> **一句话**:Spring 本身是设计模式教科书——IoC 用工厂，AOP 用代理，MVC 用适配器+策略。

## 八大模式速查

| 模式 | 定义 | Spring 中的应用 |
|------|------|----------------|
| **单例** | 全局唯一实例 | Bean scope=singleton |
| **工厂** | 工厂创建对象 | `BeanFactory`、`ApplicationContext` |
| **代理** | 代理控制访问 | **AOP**—JDK 动态代理/CGLIB |
| **模板方法** | 父类骨架，子类实现 | `JdbcTemplate`、`RestTemplate` |
| **观察者** | 一对多通知 | `@EventListener`、`ApplicationListener` |
| **策略** | 算法族可互换 | `DispatcherServlet` 选择 Handler |
| **适配器** | 接口转换 | `HandlerAdapter` |
| **装饰器** | 动态添加功能 | `ServerHttpRequestDecorator` |

## 单例 vs 原型

| | Singleton | Prototype |
|------|-----------|-----------|
| 实例数 | 1 个 | 每次获取新建 |
| 生命周期 | 随容器 | 用完即弃 |
| 注意 | 不要持有状态（线程不安全） | 容器不管销毁 |

## 面试话术

「Spring 里最常用的是单例和代理模式。IoC 容器本身就是巨型工厂，AOP 是代理模式的经典应用。我面过一道题：『在 Spring 里你自己实现过什么设计模式』——答单例和代理就够，能说出模板方法（JdbcTemplate）和观察者（@EventListener）就更出彩。」
