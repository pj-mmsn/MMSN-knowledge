---
name: knowledge-sync
description: 一键同步知识库到 GitHub。执行 git add → commit → push 三部曲,自动生成中文提交信息。只要用户说"同步知识库/推送知识库/知识库推到 GitHub/更新 kb/commit 一下知识库",或提到需要把 E:盘知识库的变更推上 GitHub,就用本技能。
---

# knowledge-sync

把 `E:\知识库` 的所有本地变更一键推送到 GitHub 仓库 `pj-mmsn/MMSN-knowledge`。

## 触发

用户说类似:
- "同步知识库"
- "推一下知识库"
- "把知识库更新到 GitHub"
- "提交知识库的变更"

## 执行

跑一条命令即可:

```bash
python C:/Users/Administrator/.agents/skills/knowledge-sync/scripts/sync.py
```

也可以带自定义消息:

```bash
python C:/Users/Administrator/.agents/skills/knowledge-sync/scripts/sync.py "新增 Spring Boot 笔记"
```

脚本会自动:
1. 检查 `E:\知识库` 是否是 git 仓库、是否有关联远程
2. 检查 git 代理是否已配(没配会提示错误和修复命令)
3. **检查根目录是否有 `README.md`,没有则自动生成**(根据目录结构生成基础模板)
4. **技能自备份:把 `sync.py` 和 `SKILL.md` 最新版同步到 `经验笔记/技能-knowledge-sync/`**,确保技能代码跟知识库一起版本管理
5. `git add -A` 暂存所有变更
6. 自动生成中文提交消息(如 `sync: 经验笔记(Spring报错笔记.md); Java手册(2个文件)`)
7. `git commit` + `git push`
8. 打出来 GitHub 仓库链接

如果没有任何变更,脚本会输出"没有新变更,无需推送"并退出。

## 前置条件

执行前确保梯子开着(脚本只检查 git 代理配置,不检查代理是否可达)。如果之前配过 `git config --global http.proxy http://127.0.0.1:7890` 就无需重复操作。

## 常见问题排查

| 现象 | 根因 | 处理 |
|------|------|------|
| `git 代理未配置` | 没设 http.proxy | `git config --global http.proxy http://127.0.0.1:7890` |
| `不是 git 仓库` | E:\知识库 没初始化 | `cd E:\知识库 && git init && git remote add origin https://github.com/pj-mmsn/MMSN-knowledge.git` |
| `没有配置远程仓库 origin` | 没关联远程 | `git remote add origin https://github.com/pj-mmsn/MMSN-knowledge.git` |
| push 卡住 / 超时 | 代理不可达(梯子没开) | 确认梯子开着，`curl -x http://127.0.0.1:7890 https://github.com` 验证 |
| `failed to push` / `rejected` | 远程有新内容没 pull | `git pull --rebase` 后再推 |

## 环境速查

| 配置项 | 值 |
|--------|-----|
| 知识库路径 | `E:\知识库` |
| 远程仓库 | https://github.com/pj-mmsn/MMSN-knowledge |
| Git 代理 | http://127.0.0.1:7890 |
| 推送分支 | main |

## 相关技能

- **github-upload**：上传单个文件或整个项目目录到 GitHub（新建仓库、覆盖文件等）
- **knowledge-loop**：知识沉淀与问题诊断，排查完问题后把经验写进知识库

## 注意事项

- 如果你手动加了新的 markdown 文件到知识库目录，脚本的 `git add -A` 会自动包含。
- 提交消息会按顶级目录分组，方便日后翻 `git log`。
- 推送的是 `main` 分支。
- 脚本只检查代理是否配置，不检查代理是否可达 —— 推送前确保梯子开着。
