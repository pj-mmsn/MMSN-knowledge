---
title: AI小说家
created: 2026-07-08
updated: 2026-07-08
type: archive
tags: [AI, Agent, Prompt, 项目复盘, Python]
---

# AI 小说家 — 项目实战经验

<!-- PyQt5 桌面端 AI 写作工具，从零构建到完善的完整踩坑记录 -->

---

## 📋 项目概览

| 维度 | 详情 |
|------|------|
| 项目 | AI 小说家 (ai-video-studio / desktop novelist) |
| 技术栈 | Python 3.12 + PyQt5 + SQLite + DeepSeek V4 Pro |
| 代码量 | 3227 行 (novelist_qt 1802L + utils 368L + repository 507L + prompts 202L + theme 132L + llm_client 146L) |
| 模式 | 💡构思 → 📋大纲 → ✍️写作 → 📝修订 → 🔍审稿 |
| 模型 | DeepSeek V4 Pro (1M context), DeepSeek V4 Flash (备选) |
| 架构 | 单体 Agent + Prompt 工程，无外部框架 |

---

## 2026-07-06 LLM Prompt 工程 — 提示词设计的五条实战经验

**场景**：为 AI 小说家设计了 5 种 System Prompt（构思/大纲/写作/修订/审稿），经历了多轮迭代。

### 经验 1：短 Prompt 比长 Prompt 更有效

**问题**：最初的大纲 Prompt 有详细的"红线规则"，但模型仍然把节名拼进章名、给 title 加编号前缀。

**根因**：指令太多会稀释关键约束的权重。模型对 15 条规则和 3 条规则的服从度差不多，但 15 条时每条被注意到的概率更低。

**解决**：把 Prompt 从 50 行压缩到 15 行，只保留 3-5 条绝对禁止项，用 `**` 加粗和 `❌` `✅` 对比标记。

**教训**：
- 每个 Prompt 控制在 15 行以内
- 用 `✅ 正确` / `❌ 错误` 对比比纯文字规则有效 10 倍
- 把最重要的约束放在 Prompt 第一句和最后一句（首尾效应）

### 经验 2：Few-shot 示例是性价比最高的改进

**问题**：大纲 Prompt 反复强调"不要加编号"，模型依然输出 `"第一卷：火种觉醒"`。

**解决**：在 Prompt 中加入一个完整的 JSON 示例：
```json
{"volumes":[{"title":"废土觉醒","chapters":[
  {"title":"辐射巢穴","summary":"...","sections":[...]}
]}]}
```

**效果**：加入示例后，模型输出格式的合规率从 ~60% 提升到 ~95%。

**教训**：示例比规则强 100 倍。与其写 10 条"不要XXX"，不如给 1 个"正确的长这样"。

### 经验 3：System Prompt 和 User Prompt 要标签对齐

**问题**：改了 System Prompt 里的输入标签（`【大纲】` `【前情提要】` `【原文】` `【修改意见】`），但 User Prompt 构造代码没同步，导致模型看到的标签和 System Prompt 说的不一致。

**解决**：统一标签命名规范——System Prompt 写明"你会依次收到【大纲】【前情提要】..."，User Prompt 严格用相同标签。

**教训**：Prompt 改了就要全局搜索引用，确认标签一致。终端打印 `_print_prompt` 可以看到实际发给模型的内容，每次改 Prompt 后跑一遍验证。

### 经验 4：用"接续锚点"解决模型断层问题

**问题**：模型写第 3 节时与第 2 节结尾脱节，即使发了完整上文。

**根因**：模型看了 16 节全文后，注意力分散，不知道该从哪个具体位置接续。

**解决**：在前情提要末尾追加一个"接续锚点"——上一节的最后 2-3 个完整段落：
```
---
⚠️ 上一节结尾（请从这里接续，不要另起开头）：
（上一节最后几段）
```

**效果**：加上锚点后，模型 80% 的情况下能从正确位置接续。

**教训**：不是数据不够，是注意力引导不够。给模型一个明确的"起跑线"比给更多上下文更有效。

### 经验 5：修订 Prompt 不能只说"最小改动"

**问题**：修订 Prompt 最初定位为"审稿编辑"，强调"最小改动"。用户说"和前面脱节"，模型只改了一句话，问题没解决。

**根因**：模型按字面理解"最小改动"，对"脱节"这种需要结构性调整的问题判断不准。

**解决**：改成"改动范围判断表"：

| 意见类型 | 做法 |
|---------|------|
| 改名字/称呼/错别字 | 仅替换 |
| 某句话/某段有问题 | 只改那一处 |
| 和前面脱节 | 改开头 1-2 段，加过渡句 |
| 全部重写 | 全文重写 |

**教训**：不能指望模型自己判断改动范围。用"如果A→做X，如果B→做Y"的决策表，比"尽量少改"这种模糊指令有效得多。

---

## 2026-07-06 SQLite 表设计 — 树形结构改平铺的惨痛教训

**场景**：大纲表最初用 `parent_id + level` 的树形结构（类似部门组织架构），重构为 `volume_title + chapter_title + section_order` 的平铺三列。

### 原设计（树形）的问题

```sql
-- 原表：自引用树
CREATE TABLE outline_nodes (
  id, parent_id, level, title, sort_order, ...
);
-- 数据：190(volume) → 191(chapter) → 192(section)
```

**三个致命缺陷**：
1. **查询需要递归**：找"当前卷所有节"要往上追溯到 volume 再往下找，SQL 复杂易错
2. **parent_id 容易断裂**：删除/迁移时父子关系错乱，孤儿节点难以清理
3. **显示要递归构建**：`_rebuild_tree()` 写了 30 行递归代码，每次 Debug 都要手动模拟调用栈

### 新设计（平铺）

```sql
CREATE TABLE outline_nodes (
  volume_title TEXT,     -- 卷名
  chapter_title TEXT,    -- 章名
  section_order INTEGER, -- 第几节
  section_title TEXT,    -- 节名
  sort_order INTEGER     -- 全局排序号
);
-- 查询极简：WHERE volume_title = ? AND chapter_title = ? ORDER BY sort_order
```

**迁移踩坑**：
- Python 的 `sqlite3` 默认 autocommit，但和显式 `commit()` 混用时行为不一致
- `ALTER TABLE ADD COLUMN` 对新表无效（`CREATE TABLE IF NOT EXISTS` 只对新库生效），对已有库必须单独跑 ALTER
- 删旧列时误删了同名新列（`sort_order` 既是旧列名也是新列名），导致排序全乱

### 经验总结

| 坑 | 教训 |
|---|------|
| 树形结构 | 不要用自引用表做层级数据，除非真的需要无限深度嵌套 |
| 迁移脚本 | 迁移逻辑和正常业务逻辑分开，加 `try/except` 容错 |
| 列名冲突 | 新旧列不同名，迁移完再删旧列，不要复用列名 |
| 排序 | 永远用整数 `sort_order` 排序，不要依赖字母序或 id 序 |

**相关**：`E:\AI项目\ai-video-studio\src\db\novel_repository.py` L103-238

---

## 2026-07-06 PyQt5 桌面应用 — 从原型到 1800 行的教训

**场景**：单文件从 558 行膨胀到 1802 行，经历了 UI 卡死、滚动条消失、样式散落等典型问题。

### 经验 1：QTextEdit + QScrollArea 冲突

**问题**：右边面板设置了 `ScrollBarAlwaysOn` 但滚动条不显示。

**根因**：`QTextEdit` 自带滚动机制，外层又包了 `QScrollArea`，两者冲突导致滚动条被隐藏。

**解决**：QTextEdit 直接加 Tab，不要外层 QScrollArea，滚动策略用 `ScrollBarAsNeeded`。

### 经验 2：同步网络调用卡死 UI

**问题**：写作用同步 `chat()` 阻塞 UI 线程，30-90 秒窗口假死。

**解决**：改用 `StreamThread(QThread)` + `chat_stream()` 流式调用，thinking 块过滤内置在 `llm_client.py` 的 SSE 解析中。

**关键代码模式**：
```python
class StreamThread(QThread):
    chunk = pyqtSignal(str)
    done = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        chat_stream(cfg, sys, usr,
                    on_chunk=lambda t: (buf.append(t), self.chunk.emit(t)))
```

### 经验 3：CSS 样式集中管理

**问题**：每个控件 `setStyleSheet(f"...{C['accent']}...")`，改配色要改几十处。

**解决**：提取 `theme.py`——配色常量 `C` + 10 个工厂函数 (`accent_btn_style()`, `input_style()` 等)。

**教训**：Python 里也能做"CSS 变量"，不要等到改配色的时候才后悔。

### 经验 4：Prompt 模板抽离

**问题**：5 个 Prompt 写死在主窗口代码里，每次调试都要在主文件中翻。

**解决**：`prompts.py` 独立文件，每个 Prompt 一个变量，注释标明输入输出格式。

---

## 2026-07-06 LLM 上下文策略 — 1M Token 窗口的正确用法

**场景**：DeepSeek V4 Pro 支持 1M Token 上下文，但用好它需要策略。

### 三个关键发现

**1. "越多越好"是错的**

最初把整卷所有节全文发给模型（16 节 × ~2000 字 = 32000 字），模型反而找不到接续点。

**正确做法**：前卷全文 + 当前卷已写内容 + 上一节接续锚点。让模型有"历史感"又有"起跑线"。

**2. SQL 子查询取最新版本**

`save_section` 最初用 INSERT 追加新版本。LEFT JOIN 时返回旧数据——因为之前重写同一节时老版本没删。

**修复**：改用 `UPDATE OR INSERT` 模式，每节只留一行。

**3. max_tokens 不能卡太紧**

最初 `max_tokens: 4096`，中文约 2000 字。模型写到高潮处经常被截断。

**修复**：提到 8192（约 4000-5000 字），够写完一节且有缓冲区。

---

## 2026-07-06 Agent 架构选型 — 为什么没上多 Agent 框架

**场景**：评估了 LangGraph / CrewAI / AutoGen / MCP+A2A 后，决定保持单体 Agent。

### 决策矩阵

| 维度 | 单体 Agent | 多 Agent 框架 | 本项目选择 |
|------|-----------|-------------|:--:|
| 任务复杂度 | 串行流水线 | 并行+协作 | 单体 ✅ |
| 工具调用 | 无 | 需要 | 单体 ✅ |
| 上下文共享 | 全局变量 | RAG/向量DB | 单体 ✅ |
| 开发成本 | 低 | 高 | 单体 ✅ |
| 可维护性 | 单文件 1802 行 | 多文件多类 | ⚠️ 待拆分 |

### 决定因素

1. **5 个模式是串行的**：构思 → 大纲 → 写作 → 修订 → 审稿，不是并行的，不需要多 Agent 协调
2. **不需要工具调用**：模型不调 API、不读文件，所有数据通过 SQLite + Prompt 传入
3. **1M 上下文消除了 RAG 需求**：全文直接塞 context，不需要向量检索

### 如果将来升级

优先级排序：
1. **接入视频生成 API**（即梦/Kling）→ 需要 MCP 工具调用
2. **Vector DB 角色/伏笔检索** → 长篇小说 (>10卷) 时 1M 不够
3. **A2A 多 Agent** → 导演/分镜/摄像师 Agent 协作

---

## 2026-07-06 开发流程反模式 — 踩过的坑

### 反模式 1：改了 DB 不跑迁移测试

**现象**：改了 `outline_nodes` 表结构，代码里用了新列，但忘了 `CREATE TABLE IF NOT EXISTS` 对已有库不生效。

**教训**：每次改 DB schema 先跑 `PRAGMA table_info(xxx)` 确认列存在。迁移脚本加 `try/except`。

### 反模式 2：修 Bug 不删缓存

**现象**：改了 `prompts.py` 和 `novelist_qt.py`，用户说"还是老样子"——Python `.pyc` 缓存没刷新，跑的旧代码。

**教训**：说"重启"时要先清 `__pycache__`，或者在 PyCharm 里直接 Run（自动处理）。

### 反模式 3：过度设计排序

**现象**：为排序问题迭代了 5 次——字母序、id 序、MIN(id)序、章节号序、最终用 `sort_order` 整数列。

**教训**：**永远用独立的 `sort_order` 整数列做排序**。不要依赖任何隐式顺序（id、字母、时间戳）。加这一列的成本是一次 ALTER TABLE，不加的成本是 5 次 Debug。
