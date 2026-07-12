---
title: 向量数据库实战 — Chroma 与 pgvector
created: 2026-07-11
updated: 2026-07-11
type: area
tags: [AI, RAG, 向量数据库, Python, 实战]
difficulty: 进阶
---

# 向量数据库实战 — Chroma 与 pgvector

> **一句话**:RAG 的心脏是向量数据库——存文本向量、做相似度检索。Chroma 是轻量首选，pgvector 适合和现有 PG 整合。

## 基本原理

```
文本 → Embedding 模型 → 向量 [0.12, -0.34, 0.56, ...] → 存入向量数据库
                                                           ↓
查询"公积金怎么提取" → 同个 Embedding 模型 → 查询向量 → 相似度搜索 → Top-K 结果
```

```
相似度度量：
  • 余弦相似度（最常用）：cos(θ) = A·B / (|A|·|B|)
  • 欧氏距离：sqrt((A-B)²)
  • 点积：A·B
```

## Chroma — 轻量级首选

```python
import chromadb
from chromadb.utils import embedding_functions

# 初始化
client = chromadb.PersistentClient(path="./chroma_db")  # 持久化到磁盘
# client = chromadb.Client()  # 或内存模式

# 创建 collection
collection = client.create_collection(
    name="knowledge_base",
    embedding_function=embedding_functions.DefaultEmbeddingFunction(),
    # 或用自己的：embedding_fn=my_embedding_function
)

# 添加文档
collection.add(
    documents=[
        "公积金提取需要身份证和申请表",
        "公积金贷款最高额度为 50 万元",
        "公积金可用于偿还住房贷款",
    ],
    metadatas=[
        {"source": "公积金政策.pdf", "page": 1},
        {"source": "公积金政策.pdf", "page": 3},
        {"source": "公积金政策.pdf", "page": 5},
    ],
    ids=["doc1", "doc2", "doc3"],
)

# 查询
results = collection.query(
    query_texts=["怎么提取公积金"],
    n_results=2,  # Top-2
)

for doc, meta, distance in zip(results["documents"][0],
                                 results["metadatas"][0],
                                 results["distances"][0]):
    print(f"[{meta['source']}] {doc}  (距离={distance:.4f})")
```

## pgvector — 和 PostgreSQL 整合

```sql
-- 安装 pgvector 扩展
CREATE EXTENSION vector;

-- 建表（向量列指定维度）
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- OpenAI text-embedding-3-small 是 1536 维
);

-- 创建索引（加速检索）
-- IVFFlat：近似最近邻，适合百万级数据
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
-- HNSW：图索引，速度更快但构建慢
-- CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

```python
import psycopg2
from openai import OpenAI

client = OpenAI()

# 写入文档
def insert_document(content: str):
    # 1. 文本 → Embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=content
    )
    embedding = response.data[0].embedding

    # 2. 存入 PG
    conn.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (content, embedding)
    )

# 查询
def search(query: str, top_k: int = 5):
    # 1. 查询文本 → Embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vec = response.data[0].embedding

    # 2. 余弦相似度检索
    rows = conn.execute("""
        SELECT content, 1 - (embedding <=> %s) AS similarity
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT %s
    """, (query_vec, query_vec, top_k)).fetchall()

    return rows
# <=> 是 pgvector 的余弦距离运算符
# 1 - 距离 = 相似度，越接近 1 越相似
```

## 常用 Embedding 模型选型

| 模型 | 维度 | 中文效果 | 价格 | 适合 |
|------|:--:|:--:|------|------|
| OpenAI text-embedding-3-small | 1536 | ⭐⭐⭐ | $0.02/1M tokens | 通用 |
| BGE-large-zh-v1.5 | 1024 | ⭐⭐⭐⭐⭐ | 免费（本地跑） | **中文场景首选** |
| text2vec-large-chinese | 1024 | ⭐⭐⭐⭐ | 免费 | 中文 |
| Cohere embed-v3 | 1024 | ⭐⭐⭐ | 收费 | 多语言 |

## Chunking 策略（RAG 性能的关键）

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 方案A：固定大小（最简单）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # 每块 500 字符
    chunk_overlap=100,       # 重叠 100 字符（防止语义断开）
    separators=["\n\n", "\n", "。", ".", " "]  # 优先按段落/句子切
)
chunks = splitter.split_text(document)

# 方案B：按 Markdown 标题层级切
from langchain.text_splitter import MarkdownHeaderTextSplitter
headers_to_split_on = [
    ("#", "h1"), ("##", "h2"), ("###", "h3")
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
chunks = splitter.split_text(markdown_document)

# 方案C：语义切分（高级）
# 计算相邻句子的 embedding 相似度
# 相似度陡降的地方就是切分点
```

## 提高检索精度 — 混合检索 + Rerank

```python
# 混合检索 = 向量相似度 + BM25 关键词检索
from rank_bm25 import BM25Okapi
import numpy as np

def hybrid_search(query: str, documents: list, embeddings: list, top_k: int = 5):
    # 1. 向量检索得分
    query_vec = get_embedding(query)
    vector_scores = cosine_similarity(query_vec, embeddings)

    # 2. BM25 关键词得分
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    bm25_scores = bm25.get_scores(query.split())

    # 3. 归一化 + 加权融合
    vector_scores = (vector_scores - vector_scores.min()) / (vector_scores.max() - vector_scores.min())
    bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min())

    # alpha 控制向量和关键词的权重
    alpha = 0.7  # 向量权重 70%，关键词 30%
    final_scores = alpha * vector_scores + (1 - alpha) * bm25_scores

    # 4. Rerank：用 CrossEncoder 对 Top-K 精排
    from sentence_transformers import CrossEncoder
    reranker = CrossEncoder('BAAI/bge-reranker-large')
    pairs = [[query, doc] for doc in top_docs]
    rerank_scores = reranker.predict(pairs)

    return sorted(zip(documents, rerank_scores), key=lambda x: x[1], reverse=True)[:top_k]
```

## 面试话术

「RAG 项目最核心的经验不是选哪个向量数据库，而是检索策略。纯向量检索在专业术语上不如关键词检索，所以我们用了混合检索——向量相似度 + BM25 关键词，再加 Rerank 重排序。这个组合让准确率提升了 15 个点。Chunking 策略也迭代了多版——从固定 500 字到按 Markdown 标题层级切分，语义完整性明显变好。」
