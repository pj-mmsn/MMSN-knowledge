---
title: Python 速成 — Java 工程师视角
tags: [Python, Java对比, 快速上手, 语法]
难度: 基础
---

# Python 速成 — Java 工程师视角

> **一句话**:如果你会 Java，Python 就是去掉花括号和分号、不加类型声明、写起来更快的语言。**2 小时能上手，2 天能写 Agent**。

## 核心概念

### Java vs Python — 宏观对比

| 维度 | Java | Python |
|------|------|--------|
| 类型系统 | 静态强类型 | 动态强类型 |
| 编译/解释 | 编译为字节码 | 解释执行 |
| 典型代码量 | 多（样板代码多） | 少（通常只有 Java 1/3） |
| 学习曲线 | 陡 | 平 |
| 运行速度 | 快 | 慢（但 Agent 开发瓶颈在 LLM API 延迟） |
| 包管理 | Maven/Gradle | pip/uv |
| IDE | IntelliJ | VSCode/PyCharm |
| 多线程 | Thread 模型 | asyncio 异步模型 |
| 应用场景 | 后端服务/中间件 | 数据科学/AI/自动化脚本 |

### 快速上手 — 语法对照表

下面是用 Java 工程师能秒懂的方式，列出最常用的 Python 语法：

#### 变量与常量

```python
# ===== Java =====
# String name = "Hello";
# final int MAX = 100;

# ===== Python =====
name = "Hello"           # 类型自动推断，不用声明类型
MAX = 100                # 没有 final 关键字，约定全大写表示常量
name: str = "Hello"      # 可以加类型注解（但不强制）
age: int = 25
pi: float = 3.14
is_ok: bool = True       # True/False 首字母大写！

# Python 的 None = Java 的 null
value = None
```

#### 字符串

```python
# Java: String s = "Hello" + " " + "World";
# Java: String.format("Hello %s", name);

# Python 字符串拼接
s = "Hello" + " " + "World"

# f-string（Python 3.6+，最推荐）
name = "小明"
age = 25
msg = f"我叫{name}，今年{age}岁"   # 输出: 我叫小明，今年25岁

# 格式化
msg2 = "我叫%s，今年%d岁" % (name, age)   # % 操作符
msg3 = "我叫{}，今年{}岁".format(name, age)  # format 方法

# 字符串操作
text = "  Hello World  "
text.strip()          # trim → "Hello World"
text.split(" ")       # split → ["Hello", "World"]
text.upper()          # toUpperCase → "HELLO WORLD"
text.lower()          # toLowerCase → "hello world"
text.replace("H", "h")  # replace → "hello World"
text.startswith("H")    # startsWith → True
text.endswith("d")      # endsWith → True
len(text)               # length → 14
"Hello" in text         # contains → True
```

#### 列表（List）— 相当于 ArrayList

```python
# Java: List<String> list = new ArrayList<>();
# Python 列表 - 可以装不同类型！
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]   # Python 的列表可以混装类型

# 增删改查
nums.append(6)          # add → [1,2,3,4,5,6]
nums.insert(0, 0)       # add(index,element) → [0,1,2,3,4,5,6]
nums.pop()              # remove last → 6, nums=[0,1,2,3,4,5]
nums.remove(3)          # remove by value → [0,1,2,4,5]
nums[0]                 # get(0) → 0
nums[-1]                # 最后一个元素 → 5
nums[1:3]               # subList(1,3) → [1,2]
len(nums)               # size → 5

# 列表推导式（Java 没有的高效写法！）
squares = [x*x for x in range(10)]        # [0,1,4,9,16,25,36,49,64,81]
evens = [x for x in range(20) if x%2==0]  # [0,2,4,...18]
matrix = [[i*j for j in range(3)] for i in range(3)]  # 二维数组

# 遍历
for item in nums:          # for (String item : nums)
    print(item)

for i, item in enumerate(nums):  # 带索引的遍历
    print(f"{i}: {item}")
```

#### 字典（Dict）— 相当于 HashMap

```python
# Java: Map<String, Object> map = new HashMap<>();
# Python 字典
user = {
    "name": "张三",
    "age": 28,
    "skills": ["Java", "Python", "Go"],
    "active": True
}

# 增删改查
user["email"] = "zhang@example.com"   # put
email = user.get("email", "默认值")    # getOrDefault
del user["active"]                     # remove
"name" in user                         # containsKey → True
user.keys()                            # keySet
user.values()                          # values
user.items()                           # entrySet

# 遍历
for key, value in user.items():
    print(f"{key}: {value}")
```

#### 条件判断

```python
# Java: if (a > 0) { ... } else if (a == 0) { ... } else { ... }
# Python: 没有括号！没有括号！没有括号！
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:      # 注意: 不是 else if，是 elif！
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

# 简写（三元表达式）
# Java: String result = age >= 18 ? "成人" : "未成年"
# Python:
result = "成人" if age >= 18 else "未成年"

# 真值判断（Python 特色）
# 以下值被视为 False: None, 0, "", [], {}, ()
# 其他都是 True
if not name:           # 等价于 name == null || name.isEmpty()
    print("名字为空")

if nums:               # 等价于 nums != null && !nums.isEmpty()
    print("列表有元素")
```

#### 循环

```python
# Java: for (int i = 0; i < 10; i++) { ... }

# Python 的 for 循环是 for-each
for i in range(10):          # 0,1,2,...9
    print(i)

for i in range(3, 10):       # 3,4,5,...9
    print(i)

for i in range(0, 10, 2):    # 0,2,4,6,8
    print(i)

# while 循环
count = 0
while count < 5:
    print(count)
    count += 1      # Python 没有 count++ 语法！

# break 和 continue 用法和 Java 一样
```

#### 函数

```python
# Java: public String greet(String name, int age) { return "Hi"; }
# Python: def 函数名(参数): return 返回值

def greet(name: str, age: int) -> str:  # -> 表示返回类型（可选）
    return f"Hi, I'm {name}, {age} years old"

# 调用
result = greet("张三", 28)

# 参数默认值（Java 的 @Builder 或重载）
def create_user(name: str, age: int = 18, city: str = "未知"):
    return {"name": name, "age": age, "city": city}

create_user("张三")                               # 只用必填参数
create_user("张三", 25)                           # 按位置
create_user("张三", city="北京")                   # 按名称
create_user(name="张三", age=25, city="北京")      # 全部按名称

# 可变参数（Java 的 ...）
def sum_all(*args):      # *args = 任意数量位置参数
    return sum(args)

sum_all(1, 2, 3, 4, 5)   # 15

def print_info(**kwargs):  # **kwargs = 任意数量关键字参数
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="张三", age=25, skill="Python")
```

#### 类与对象

```python
# Java:
# public class User {
#     private String name;
#     public User(String name) { this.name = name; }
#     public String greet() { return "Hi " + name; }
# }

# Python: 简洁到极致
class User:
    def __init__(self, name: str):     # 构造方法，self = this
        self.name = name               # self.name 就是成员变量
        self._private = "约定下划线开头表示私有"  # 只是约定，不强制

    def greet(self) -> str:
        return f"Hi {self.name}"

    # 静态方法 = @staticmethod
    @staticmethod
    def create_guest():
        return User("访客")

# 使用
user = User("张三")
print(user.greet())         # Hi 张三
guest = User.create_guest()

# 继承
class AdminUser(User):
    def __init__(self, name: str, role: str):
        super().__init__(name)      # super() = Java 的 super
        self.role = role

    def greet(self) -> str:
        return f"[管理员] {super().greet()}"
```

#### 异常处理

```python
# Java: try { ... } catch (Exception e) { ... } finally { ... }
try:
    result = 10 / 0
except ZeroDivisionError as e:     # 具体异常类型
    print(f"除零错误: {e}")
except Exception as e:             # 通用异常（类似 Exception）
    print(f"未知错误: {e}")
else:                              # 没有异常时执行（Java 没有）
    print("一切正常")
finally:
    print("无论如何都执行")        # 释放资源

# 抛异常
raise ValueError("参数不合法")     # throw new IllegalArgumentException()

# 自定义异常
class NotFoundError(Exception):    # 继承 Exception
    pass

raise NotFoundError("用户不存在")
```

#### 模块导入

```python
# Java: import java.util.List; import java.util.*;
# Python 导入
import os                         # import os
import json                       # import json
from datetime import datetime     # import java.time.LocalDateTime
from typing import List, Dict     # 只导入需要的部分

# 常用的内置模块
import os       # 文件和路径操作
import sys      # 系统参数
import json     # JSON 处理
import re       # 正则表达式
import math     # 数学函数
import random   # 随机数
import hashlib  # MD5/SHA 哈希
from pathlib import Path  # 现代路径操作
```

### Java 工程师最常踩的坑

| Python 写法 | 你以为像 Java | 但其实... | 正确理解 |
|------------|-------------|-----------|---------|
| `if not list:` | `list != null && !list.isEmpty()` | ✅ 就是这意思 | Python 的真值判断 |
| `dict[key]` | `map.get(key)` | 但 key 不存在会抛 KeyError | 用 `dict.get(key, default)` |
| `10 / 3` | `3`（整数除法） | 结果是 `3.333...` | `10 // 3` 才是整数除法 |
| `"1" + 1` | 编译错误或类型转换 | 抛 TypeError | 用 `int("1") + 1` 或 `"1" + str(1)` |
| `==` | 比较引用 | 是比较值（equals） | 引用比较用 `is`：`a is None` |
| `list.sort()` | 返回排序后的新列表 | **原地排序**，返回 None | 想要新列表用 `sorted(list)` |
| `for i in list:` | for-each 迭代 | 但**不能**在循环中修改 list | 用 `list[:]` 拷贝一份再遍历 |

### 第一个 Python Agent

学完上面的语法，你已经能看懂下面的代码了：

```python
"""
第一个 Python Agent - 用你刚学的语法理解它
"""
import json
from openai import OpenAI

client = OpenAI(api_key="your-key", base_url="https://api.deepseek.com")

# 定义一个搜索工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索互联网信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

# Agent 循环 - 自动分析和调用工具
def run_agent(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    for step in range(5):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:  # 没有工具调用 = 直接回答
            return msg.content

        # 执行工具
        for tc in msg.tool_calls:
            result = f"搜索结果: {json.loads(tc.function.arguments)['query']}"
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

    return "超时"

print(run_agent("2026年AI发展趋势"))
```

**上面的代码里你全都学过了**：函数、列表、字典、if 判断、for 循环、try/except、字符串、导入。Python 就这些，没别的了。

## 常见误区

- **误区1**: "Python 没有类型，写大项目会乱" —— 可以用类型注解（`name: str`）和 mypy 做静态检查。当然确实不如 Java 严格。
- **误区2**: "循环用 range 太麻烦" —— 实际上 Python 的 for-each 遍历是最常用的，range 只在需要索引时才用。
- **误区3**: "动态类型导致运行时才发现错误" —— 对，所以推荐写类型注解 + 写测试。但 Agent 开发大部分场景是写脚本和调用 API，动态类型反而是优势（快速迭代）。

## 参考来源

- Python 官方教程: https://docs.python.org/3/tutorial/
- Python 速查表: https://quickref.me/python
- 相关笔记: `Java手册/00-Python基础/02-Python高级特性.md`
