---
title: FastAPI 后端开发实战
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [Python, API, 实战, 部署]
difficulty: 进阶
---

# FastAPI 后端开发实战

> **一句话**:FastAPI 是 Python 界的 Spring Boot——async 原生支持、自动生成 OpenAPI 文档、类型校验开箱即用。Agent 项目的 API 层首选。

## FastAPI vs Flask vs Spring Boot

| | FastAPI | Flask | Spring Boot |
|------|---------|-------|-------------|
| 性能 | **极高**（Starlette + asyncio） | 一般（同步） | 高 |
| 异步 | ✅ **原生 async/await** | ❌ 需插件 | ✅ WebFlux |
| 类型校验 | ✅ Pydantic 自动 | ❌ 手动 | ✅ Bean Validation |
| API 文档 | ✅ **自动生成 Swagger** | ❌ 需插件 | ✅ SpringDoc |
| 学习曲线 | 低 | **最低** | 中 |
| 生态 | 快速增长 | 最成熟 | 最成熟 |
| 适合 | **AI/Agent 服务** | 简单 API | 企业级 Java 项目 |

## 项目结构

```
agent-api/
├── main.py              # FastAPI 入口
├── config.py            # 配置（模型 key、DB 连接）
├── models/
│   ├── schemas.py       # Pydantic 请求/响应模型
│   └── database.py      # SQLAlchemy ORM 模型
├── routers/
│   ├── chat.py          # /api/chat 对话接口
│   ├── agent.py         # /api/agent Agent 接口
│   └── knowledge.py     # /api/knowledge 知识库接口
├── services/
│   ├── llm_service.py   # LLM 调用封装
│   ├── rag_service.py   # RAG 检索逻辑
│   └── agent_service.py # Agent 编排逻辑
├── middleware/
│   ├── auth.py          # JWT 鉴权
│   └── logging.py       # 请求日志
└── tests/
    ├── test_chat.py
    └── test_agent.py
```

## 核心代码

```python
# main.py — FastAPI 入口
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, agent, knowledge

app = FastAPI(title="Agent API", version="1.0.0")

# CORS（前后端分离必需）
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(agent.router, prefix="/api/agent", tags=["Agent"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])

# 自动生成：http://localhost:8000/docs（Swagger 文档）
# 自动生成：http://localhost:8000/redoc（ReDoc 文档）
```

```python
# routers/chat.py — 对话接口
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from services.llm_service import LLMService
from middleware.auth import get_current_user

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tokens_used: int

@router.post("/send", response_model=ChatResponse)
async def chat(request: ChatRequest, user=Depends(get_current_user)):
    """发送消息，返回 AI 回复"""
    llm = LLMService()
    reply, tokens = await llm.chat(request.message, request.session_id)
    return ChatResponse(reply=reply, session_id=request.session_id, tokens_used=tokens)
```

```python
# routers/agent.py — SSE 流式接口（Agent 对话实时展示）
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.agent_service import AgentService

router = APIRouter()

@router.post("/run")
async def run_agent(task: str):
    """运行 Agent，流式返回结果"""
    agent = AgentService()

    async def event_stream():
        async for event in agent.run_stream(task):
            yield f"data: {event.json()}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

```python
# services/llm_service.py — LLM 调用封装
import httpx
from config import settings

class LLMService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"

    async def chat(self, message: str, session_id: str = None) -> tuple[str, int]:
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "deepseek-v4-pro",
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
            }
        )
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        tokens = data["usage"]["total_tokens"]
        return reply, tokens
```

## 部署 — Docker + uvicorn

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
# 开发
uvicorn main:app --reload

# 生产（4 workers，每核一个）
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

## 面试话术

「Agent 项目的 API 层我用 FastAPI。三个理由：①async 原生支持，Agent 调用 LLM 时天然需要异步不阻塞 ②Pydantic 自动校验 + Swagger 文档，前后端联调效率很高 ③部署简单——uvicorn + Docker，一个进程跑几个 worker 就搞定。和 Spring Boot 比，轻量太多，适合 AI 服务这种快速迭代的场景。」
