---
name: knowledge-sync
description: 知识库同步到 GitHub 或上传单个文件。支持两种模式:(1)默认:同步 E:\知识库 所有变更到 pj-mmsn/MMSN-knowledge;(2)单文件:上传任意文件到任意 GitHub 仓库。当用户说"同步知识库/推送知识库/知识库推到 GitHub/更新 kb/commit 知识库",或"把这个文件传到 GitHub/上传到 repo/推到仓库"时使用本技能。
---

# knowledge-sync

把本地文件或整个知识库推送到 GitHub。一个技能,两种模式。

## 模式 A:知识库同步(默认)

将 `E:\知识库` 的所有本地变更一键 `git add → commit → push`。

```bash
python C:/Users/Administrator/.agents/skills/knowledge-sync/scripts/sync.py
```

或带自定义消息:

```bash
python C:/Users/Administrator/.agents/skills/knowledge-sync/scripts/sync.py "新增 Spring 笔记"
```

自动执行:
1. 检查 git 仓库 + 远程 origin
2. 检查 git 代理
3. 缺 README.md → 自动生成
4. 技能源码有更新 → 自动备份到 `经验笔记/技能-knowledge-sync/`
5. `git add -A` → 生成中文提交消息 → `git commit` → `git push`
6. 打印 GitHub URL

## 模式 B:单文件上传

把任意本地文件传到任意 GitHub 仓库(走 Contents API,不建本地 git 工作区)。仓库不存在时可自动创建。

```bash
python C:/Users/Administrator/.agents/skills/knowledge-sync/scripts/sync.py \
    --file "C:\work\report.md" \
    --repo pj-mmsn/my-notes \
    [--branch main] \
    [--create-repo public] \
    [--message "上传报告"]
```

| 参数 | 必填 | 说明 |
|------|:--:|------|
| `--file` | ✅ | 本地文件路径 |
| `--repo` | ✅ | OWNER/REPO |
| `--branch` | ❌ | 默认 `main` |
| `--create-repo` | ❌ | 仓库不存在时新建,加 `public`/`private` 指定可见性 |
| `--message` | ❌ | 提交消息,默认 `Upload <文件名>` |

## 触发词

- **知识库同步**: "同步知识库"、"推一下知识库"、"知识库更新到 GitHub"、"commit 知识库"
- **单文件上传**: "把这个文件传到 GitHub"、"上传到我的 repo"、"推到仓库"
