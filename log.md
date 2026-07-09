# 知识库日志

> 按时间记录所有操作。追加写入，不修改历史条目。
> 格式：`## [YYYY-MM-DD] action | subject`
> action 类型：create | update | archive | delete | lint | ingest | query
> 超过 500 条时归档为 `log-YYYY.md`

---

## [2026-07-08] enhance | 三技能联动强化
- knowledge-loop: 标签数 22→31 修正；「定期维护」升级为 11 项「深度 Lint」（断裂链接/孤立页面/索引一致性/frontmatter/标签合规/质量信号/来源溯源/页面尺寸/归档/日志轮转/前沿刷新）；新增「标签热力图」
- knowledge-sync: SKILL.md 添加 pre-push 校验流程说明；sync.py 新增 `pre_push_check()` 函数（校验 frontmatter 完整性 + 标签合规 + type/difficulty 合法性）；集成到 sync_kb 流程中，问题阻塞 push
- 验证：pre-push 校验在当前知识库上全部通过 ✅

## [2026-07-08] normalize | 标签体系统一（148→31 标准标签）
- 标签审计：发现 148 个非标准标签，171 个标签实例分布在 66 篇笔记中
- 定义映射规则：产品名→框架类、同义词→标准标签、文件专属→父类
- 批量替换 58 篇笔记，收敛为 31 个标准标签
- 更新 SCHEMA.md 标签体系：从 22→31 标签，分 5 大类
- 修复 60 篇 frontmatter 格式（`---` 关闭标记后缺换行）
- 最终分布：[29] AI · [29] Java · [24] Agent · [10] Python · [10] 概念入门 · [9] 并发 · [6] LLM · [6] RAG · [6] 实战 · [5] Spring/LangChain/架构/排错 · [4] 工具/调研/向量数据库/Prompt/集合/框架 · [3] API/JVM/项目复盘 · [2] LangGraph/CrewAI/数据库/部署/学习方法/职业规划 · [1] AutoGen/Dify/分布式

## [2026-07-08] create | LLM Wiki 优化：SCHEMA.md + log.md
- 创建 SCHEMA.md — 标签体系（31个标签）、frontmatter 规范、页面创建规则、更新策略
- 创建 log.md — 操作日志
- 创建 index.md — 根目录总索引
- 初始化日志：基于现有目录结构记录基线
- 基线状态：01-Projects(1) | 02-Areas(52) | 03-Resources(470+) | 04-Archives(4) | 05-经验日志(5)

## [2026-07-08] update | 标签体系统一
- 67篇笔记 frontmatter 标准化：新增 created/updated/type 字段，难度→difficulty
- 9篇无frontmatter笔记补全
- 标签归一化：148个散装标签 → 31个标准标签
- 结果：全库标签 100% 在 taxonomy 内，无越界标签

## [2026-07-08] baseline | 知识库基线
- 现有结构：PARA 四象限 + 经验日志，Obsidian 管理，Git 版本控制
- 01-Projects/：8周Agent学习计划
- 02-Areas/AI与Agent/：25篇（Agent核心概念 → LangChain/LangGraph → RAG → 记忆系统 → Multi-Agent → 部署运维）
- 02-Areas/Java/：21篇（基础 → 集合 → 并发 → JVM → 数据库 → 框架 → 分布式）
- 02-Areas/Python/：6篇（Java工程师视角速成）
- 03-Resources/JavaGuide/：470+篇 Java 全栈参考（git submodule）
- 03-Resources/AI前沿追踪/：2026-AI技术前沿与生态更新
- 03-Resources/工具指南/：Git/GitHub 操作指南
- 04-Archives/：AI小说家、从零构建Agent、视频工作室、Agent框架选型-2026
- 05-经验日志/：DeepSeek API双协议调用、Prompt工程实战、RAG企业级落地方案、实战场景与解决方案、Spring启动报错
- 维护工具：knowledge-loop（自动维护索引）、knowledge-sync（GitHub同步）
