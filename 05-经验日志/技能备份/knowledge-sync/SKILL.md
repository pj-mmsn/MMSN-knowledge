---
name: knowledge-sync
description: >
  GitHub 上传/同步/推送——所有和 GitHub 有关的文件操作都用这个技能。
  触发词极广，只要用户提到以下任何一种就立即调用：
  - "传到 GitHub / 上传到 GitHub / 推到 GitHub / 推送到 GitHub / 同步到 GitHub"
  - "GitHub 上新建仓 / 建一个仓库 / 推到我的仓库 / 传一份到 GitHub"
  - "同步知识库 / 推送知识库 / commit 知识库 / 更新 kb"
  - "把这个项目推到 GitHub / 在 GitHub 同步 / GitHub 仓库"
  - 或者任何涉及「文件 → GitHub」的操作，哪怕用户没精确说出上面的词。
  支持两种模式:
  (1)默认:同步 E:\知识库 到 pj-mmsn/MMSN-knowledge
  (2)单文件/项目:上传任意文件到任意仓库（仓库不存在可自动新建）。
  不要自己手写 git 命令去推——调用本技能的 scripts/sync.py 即可完成所有 GitHub 操作。
---

# knowledge-sync

把本地文件或整个知识库推送到 GitHub。一个技能,两种模式。

## ⚡ 快速识别

**只要用户说「GitHub」+ 任何动词（传/推/同步/上传/建仓/新建）→ 直接调这个技能，别犹豫。**
不要自己手写 `git push`、`gh repo create` 等命令——用本技能的 `scripts/sync.py`。

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
