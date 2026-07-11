---
title: MyBatis 核心原理
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [框架, Java]
difficulty: 进阶
---

# MyBatis 核心原理

> **一句话**:MyBatis 是半自动 ORM，XML/注解写 SQL，#{} 预编译防注入，${} 原样拼接。

## #{} vs ${}

| | `#{}` | `${}` |
|------|-------|-------|
| 方式 | 预编译占位符 `?` | 字符串拼接 |
| SQL 注入 | **安全** ✅ | **危险** ❌ |
| 使用 | 99% 参数 | 动态表名/列名/ORDER BY |

```xml
<!-- #{} → SELECT * FROM user WHERE id = ? -->
<select id="getUser"> SELECT * FROM user WHERE id = #{userId} </select>

<!-- ${} → SELECT * FROM user ORDER BY create_time DESC -->
<select id="getByOrder"> SELECT * FROM user ORDER BY ${column} ${dir} </select>
```

## 核心流程

```
mybatis-config.xml + Mapper.xml → SqlSessionFactory → SqlSession
  → Executor → StatementHandler（参数+SQL执行）→ ResultSetHandler（结果映射）
```

## 一二级缓存

| | 一级缓存 | 二级缓存 |
|------|------|------|
| 范围 | SqlSession 内 | Mapper namespace |
| 默认 | **默认开启** | 需手动 `<cache/>` |
| 清除 | insert/update/delete | 同上，可跨 SqlSession |

## 面试追问

**Q: MyBatis vs MyBatis-Plus？**
A: Plus 是增强工具，内置通用 CRUD（`baseMapper.selectById()`）、分页插件。底层还是 MyBatis。

**Q: 怎么解决 N+1 查询？**
A: 用 JOIN 一次查出，或嵌套查询 + fetchType=lazy 延迟加载。
