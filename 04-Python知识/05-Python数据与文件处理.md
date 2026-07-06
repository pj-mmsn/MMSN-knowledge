---
title: Python 数据与文件处理
tags: [Python, JSON, CSV, 正则, 文件操作, Path, 数据处理]
难度: 基础
---

# Python 数据与文件处理

> **一句话**:Agent 开发的本质是"数据流"——从各种来源读数据（文件/API/数据库），处理它，再以某种格式输出。Python 在这块的便捷性远超 Java。

## 核心概念

### Java vs Python 文件处理对比

| 操作 | Java | Python |
|------|------|--------|
| 读文件 | `Files.readString(path)` | `open(path).read()` |
| 写文件 | `Files.writeString(path, text)` | `open(path, 'w').write(text)` |
| 解析 JSON | ObjectMapper/JSONArray | `json.loads()` / `json.dumps()` |
| 写 CSV | OpenCSV/Apache Commons | `csv.writer` |
| 遍历目录 | `Files.walk() / File.listFiles()` | `Path.iterdir() / glob()` |
| 正则匹配 | `Pattern.compile()` | `re.search()` / `re.findall()` |

## 代码实例

### 1. 文件读写

```python
# ===== 读文件 =====
# 读整个文件
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 按行读
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()       # 返回列表，每行是一个元素

# 逐行迭代（推荐，省内存）
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())    # strip() 去掉换行符

# ===== 写文件 =====
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行\n")

# 追加模式
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("新的日志行\n")

# ===== 二进制文件 =====
with open("image.jpg", "rb") as f:      # 二进制读
    data = f.read()

with open("copy.jpg", "wb") as f:       # 二进制写
    f.write(data)
```

### 2. 路径操作（Path vs Java Path）

```python
from pathlib import Path
import os

# ===== 现代 Python 用 Path，不用 os.path =====

# Path 基本操作
p = Path("C:/Users/Administrator/app/data.txt")

p.name          # "data.txt"
p.stem          # "data"（无后缀）
p.suffix        # ".txt"
p.parent        # Path("C:/Users/Administrator/app")
p.parents       # [Path(.../app), Path(...), ...] 所有父目录

# 拼接路径（比 Java 简单）
data_dir = Path("C:/Users/Administrator/data")
file_path = data_dir / "project" / "config.json"  # 用 / 拼接！

# 常用操作
Path(".").exists()          # 是否存在
Path(".").is_file()         # 是否是文件
Path(".").is_dir()          # 是否是目录
Path(".").mkdir(parents=True, exist_ok=True)  # 创建目录 (mkdir -p)

# 遍历目录
for f in Path(".").iterdir():
    print(f.name)

# 递归查找所有 .py 文件
for f in Path(".").glob("**/*.py"):
    print(f)

# 读写文件（一行搞定）
Path("hello.txt").write_text("Hello, World!", encoding="utf-8")
content = Path("hello.txt").read_text(encoding="utf-8")

# Java 对比：
# Java: Files.writeString(path, text)
# Python: Path(path).write_text(text)
```

### 3. JSON 处理

```python
import json

# ===== Python dict ↔ JSON =====

# dict → JSON 字符串（Java 的 ObjectMapper.writeValueAsString）
data = {
    "name": "张三",
    "age": 28,
    "skills": ["Java", "Python", "AI"],
    "active": True,
    "profile": None
}

json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON 字符串 → dict（Java 的 ObjectMapper.readValue）
json_str = '{"name": "张三", "age": 28}'
data = json.loads(json_str)
print(data["name"])  # 张三

# ===== 文件读写 =====

# 写入 JSON 文件
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取 JSON 文件
with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ===== Agent 开发中的 JSON 处理 =====

# LLM 输出 JSON → dict
llm_output = '{"intent": "查询天气", "city": "北京", "date": "2026-07-03"}'
parsed = json.loads(llm_output)
print(f"意图: {parsed['intent']}, 城市: {parsed['city']}")

# dict → LLM 输入（带中文，不转义 \uXXXX）
prompt_data = {"role": "assistant", "content": "你好"}
prompt_json = json.dumps(prompt_data, ensure_ascii=False)  # ensure_ascii=False 保留中文
```

### 4. CSV 处理

```python
import csv

# ===== 读 CSV =====
with open("data.csv", "r", encoding="utf-8-sig") as f:  # utf-8-sig 处理 BOM
    reader = csv.DictReader(f)  # 按字典读，第一行是列名
    for row in reader:
        print(row["name"], row["age"])

# 按列表读
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:  # row = ["张三", "28", "Java"]
        print(row[0], row[1])

# ===== 写 CSV =====
with open("output.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄", "技能"])     # 表头
    writer.writerow(["张三", 28, "Java"])
    writer.writerow(["李四", 25, "Python"])

# 用 DictWriter
with open("output.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "skill"])
    writer.writeheader()
    writer.writerow({"name": "张三", "age": 28, "skill": "Java"})
```

### 5. 正则表达式

```python
import re

# ===== 基础 =====
text = "我的电话是 138-1234-5678，邮箱是 test@example.com"

# 查找第一个匹配
phone = re.search(r"\d{3}-\d{4}-\d{4}", text)
if phone:
    print(phone.group())  # "138-1234-5678"

# 查找所有匹配
emails = re.findall(r"\w+@\w+\.\w+", text)
print(emails)  # ['test@example.com']

# 替换
masked = re.sub(r"\d{3}-\d{4}-\d{4}", "***-****-****", text)
print(masked)  # "我的电话是 ***-****-****，邮箱是 test@example.com"

# ===== Agent 开发中的正则使用 =====

# 1. 从 LLM 输出中提取 JSON
llm_raw = """我来帮你分析...
```json
{"result": "success", "data": [1, 2, 3]}
```
以上就是我的回答"""
json_match = re.search(r"```json\n(.*?)\n```", llm_raw, re.DOTALL)
if json_match:
    data = json.loads(json_match.group(1))
    print(data)  # {'result': 'success', 'data': [1, 2, 3]}

# 2. 提取 Markdown 标题
markdown = "# 一级标题\n## 二级标题"
headings = re.findall(r"^(#{1,6})\s+(.+)$", markdown, re.MULTILINE)
print(headings)  # [('#', '一级标题'), ('##', '二级标题')]

# 3. 清洗文本（去除多余空白）
dirty = "这是  一段  有  很多   空格的  文本"
clean = re.sub(r"\s+", " ", dirty).strip()
print(clean)  # "这是一段有很多空格的文本"

# 4. 提取 URL
urls = re.findall(r"https?://[^\s<>\"']+", "访问 https://example.com 了解更多")
print(urls)  # ['https://example.com']
```

### 6. 常用数据清洗

```python
from datetime import datetime

# ===== Agent 输出清洗 =====

def clean_llm_output(text: str) -> str:
    """清理 LLM 输出中的无关内容"""
    # 去除思维链过程（如果有 <thinking> 标签）
    text = re.sub(r"<thinking>.*?</thinking>", "", text, flags=re.DOTALL)
    # 去除多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 去除首尾空白
    text = text.strip()
    return text

# ===== 字符串格式化常用操作 =====
def format_result(data: dict) -> str:
    """格式化 Agent 返回的结构化数据"""
    parts = []
    for key, value in data.items():
        parts.append(f"{key}: {value}")
    return "\n".join(parts)

# ===== 日期处理 =====
now = datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M:%S")  # "2026-07-03 10:30:00"
date_only = now.strftime("%Y%m%d")            # "20260703"

# 解析日期字符串
date = datetime.strptime("2026-07-03", "%Y-%m-%d")
print(date)  # datetime(2026, 7, 3, 0, 0)
```

## 常见误区

- **误区1**: "用 `open()` 打开文件不需要指定编码" —— 在 Windows 上**一定**要指定 `encoding="utf-8"`，否则 Windows 默认用 GBK 编码读文本文件，会乱码。
- **误区2**: "CSV 用 ',' 分隔就行" —— 中文等场合经常用 `utf-8-sig` 编码（带 BOM）才能被 Excel 正确识别。用 `csv.writer` 时加 `newline=""` 参数避免空行。
- **误区3**: "正则试一次就不改了" —— 建议先在 https://regex101.com 上测试验证。正则写错会导致难以排查的 bug。

## 参考来源

- Python 官方文档 - 文件 I/O: https://docs.python.org/3/tutorial/inputoutput.html
- Python 官方文档 - json: https://docs.python.org/3/library/json.html
- Python 官方文档 - re 正则: https://docs.python.org/3/library/re.html
- Pathlib 教程: https://realpython.com/python-pathlib/
- 相关笔记: `Java手册/00-Python基础/01-Python速成-Java工程师视角.md`
