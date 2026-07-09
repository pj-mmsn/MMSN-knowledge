---
title: DeepSeek API双协议调用
created: 2026-07-08
updated: 2026-07-08
type: log
tags: [AI, LLM, API, 排错]
---

# DeepSeek API 双协议调用

<!-- DeepSeek 同时支持 OpenAI 和 Anthropic 两种协议，端点、消息格式、SDK 都不一样，混用必炸 -->

---

## 2026-07-08 DeepSeek API 双协议调用踩坑全记录

**场景**：学习 Agent 开发第一周，从零调用 DeepSeek API。用 OpenAI SDK 一次调通，但切换到 Anthropic 协议时连踩三个坑（404、格式错误、编码错误）。

**根因**：DeepSeek V4 提供两种协议入口，但两者的路径、消息结构、SDK 完全隔离，不能混搭。

**结论**：

### 协议对比总览

| | OpenAI 协议 | Anthropic 协议 |
|---|---|---|
| 端点 | `https://api.deepseek.com` | `https://api.deepseek.com/anthropic` |
| 完整路径 | `.../v1/chat/completions`（SDK 自动拼） | `.../anthropic/v1/messages` |
| SDK | `openai` 包 | `anthropic` 包 |
| 鉴权方式 | `Bearer {key}`（SDK 自动加） | `x-api-key` 头 |
| content 格式 | `"字符串"` | `[{"type":"text","text":"字符串"}]` |
| system 消息 | 在 `messages` 数组里 | 顶层 `system` 字段 |
| model ID | `deepseek-v4-pro` | `deepseek-v4-pro`（相同） |

### 三大坑

**坑1：404 Not Found — 路径混搭**

```
❌ /anthropic/v1/chat/completions  → OpenAI 路径拼到 Anthropic 端点
❌ /anthropic                     → 缺了 /v1/messages
✅ /anthropic/v1/messages         → 这才是完整路径
```

**坑2：content 格式不匹配**

Anthropic 协议中 `content` 必须是**数组**，每个元素是 `{"type":"text", "text":"..."}`：

```python
# ❌ OpenAI 格式（Anthropic 端点不认）
{"messages": [{"role": "user", "content": "你好"}]}

# ✅ Anthropic 格式
{"messages": [{"role": "user", "content": [{"type": "text", "text": "你好"}]}]}
```

**坑3：urllib 原生调用 data 必须是 bytes**

```python
# ❌ str 直接传入 → TypeError
data = json.dumps(body)

# ✅ 必须 encode
data = json.dumps(body).encode("utf-8")
```

### 两种调用方式完整代码

**方式1：OpenAI SDK（推荐，最简单）**

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.deepseek.com"    # 不加任何后缀
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": "你是什么模型"}]
)
print(response.choices[0].message.content)
```

**方式2：urllib + Anthropic 协议（理解底层）**

```python
import urllib.request
import json

body = json.dumps({
    "model": "deepseek-v4-pro",
    "max_tokens": 1024,
    "messages": [{
        "role": "user",
        "content": [{"type": "text", "text": "你是什么模型"}]
    }]
})

req = urllib.request.Request(
    "https://api.deepseek.com/anthropic/v1/messages",
    data=body.encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-api-key": "sk-xxx",
        "anthropic-version": "2023-06-01",
    },
    method="POST",
)

resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
print(data)
```

**关键命令/代码**：
```bash
# 验证 openai 包已安装
pip show openai
```

```bash
# 确认 Python 环境正确
.venv/Scripts/python.exe -c "from openai import OpenAI; print('OK')"
```

**相关**：
- 02-Areas: [Agent开发环境搭建指南](../02-Areas/AI与Agent/05-实战与运维/Agent开发环境搭建指南.md)
- 02-Areas: [常见问题排错](../02-Areas/AI与Agent/05-实战与运维/常见问题排错.md)（PyCharm venv 识别问题）
- 02-Areas: [Python AI开发生态概览](../02-Areas/AI与Agent/03-Python-AI开发/Python AI开发生态概览.md)

---
