# GitHub 推送指南 —— 把本地项目/知识库推上 GitHub

> 记录于 2026-07-03,实际操作:把 `E:\知识库` 推送到 GitHub 公共仓 `MMSN-knowledge`。

---

## 两种场景,两种方案

### 场景 A:传单个文件到仓库

适合:临时分享一个脚本、截图、文档到已有仓库。

| 工具 | 方式 |
|------|------|
| `gh api` | 调 GitHub Contents API,`PUT /repos/{owner}/{repo}/contents/{path}`,文件内容 base64 编码后直接写入 |
| 内置技能 `github-upload` | 封装了上面的流程,自动处理建仓库、查 sha(同名覆盖)、base64 编码 |

**优点**:不用 clone,不用本地 git 工作区。  
**缺点**:每个文件一次 API 调用,大批量文件不划算;没有版本历史。

### 场景 B:推送整个目录(本项目) ← 当前方案

适合:知识库、项目代码、笔记仓库等需要版本管理的目录。

核心就是标准 git 流程:

```bash
# 1. 进入目录,初始化 git
cd /path/to/project
git init

# 2. 添加所有文件,创建第一个提交
git add -A
git commit -m "init: 初始导入"

# 3. 用 gh CLI 一键创建远程仓库并推送
gh repo create MMSN-knowledge --public --source=. --remote=origin --push
```

`gh repo create ... --push` 这一行等价于手动执行:

```bash
gh repo create MMSN-knowledge --public    # 在 GitHub 上建空仓库
git remote add origin https://github.com/<你的用户名>/MMSN-knowledge.git
git branch -M main
git push -u origin main
```

**优点**:一次 push 全部文件,后续 `git commit + git push` 即可增量更新,天然带版本历史。  
**缺点**:需要 git 工作区(几百 KB 的 `.git` 目录)。

---

## 前置:安装和配置 gh CLI

### Windows

```powershell
winget install --id GitHub.cli -e
```

### 登录(Git Bash 里)

```bash
# 确保 gh 在 PATH 里(winget 安装后可能需要新开终端)
export PATH="$PATH:/c/Program Files/GitHub CLI"

# 浏览器登录(推荐,不用手输 token)
gh auth login --hostname github.com --web --git-protocol https
```

会弹出类似:
```
! First copy your one-time code: XXXX-XXXX
Open this URL to continue in your web browser: https://github.com/login/device
```

打开浏览器访问 `https://github.com/login/device`,输入验证码,点授权即完成。以后这台机器上 `gh` 和 `git` 都自动走这个认证。

### 验证

```bash
gh auth status    # 应显示你的 GitHub 用户名
gh repo list      # 列出你的仓库
```

### 配置代理(国内环境必需)

gh CLI 走系统代理通常自动生效,但 **git 需要单独配代理**才能 push/pull:

```bash
# Clash 默认端口 7890,其他梯子换成对应端口
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 验证
git config --global --get http.proxy
```

如果哪天直连恢复了,取消代理:

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

> **为什么 `gh repo create` 能成功但 `git push` 会超时?** 因为 gh CLI 用的是 Windows 系统代理,git 用的是自己的配置,两者独立。

---

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 第一次推送整个目录 | `gh repo create <仓库名> --public --source=. --push` |
| 后续增量推送 | `git add -A && git commit -m "更新说明" && git push` |
| 查看远程地址 | `git remote -v` |
| 克隆回来 | `git clone https://github.com/<用户名>/<仓库名>.git` |
| 拉取远程更新 | `git pull` |
| 查看提交历史 | `git log --oneline` |
| 给已有本地项目关联远程 | `git remote add origin https://github.com/<用户名>/<仓库名>.git` |

---

## 扩展:如果目录里有不想上传的文件

在项目根目录创建 `.gitignore`:

```gitignore
# 忽略敏感配置
.env
*.key
credentials.json

# 忽略大文件
*.iso
*.zip
```

然后 `git add -A` 会自动跳过这些文件。

---

## 2026-07-04 ⚠ gh CLI 在 Git Bash 中的路径陷阱

**场景**：在 Git Bash（或 ZCode 的 Bash 环境）中直接敲 `gh`，报 `command not found`，但实际上 `gh.exe` 已通过 winget 安装在 `C:\Program Files\GitHub CLI\`。

**根因**：Git Bash 的 PATH 继承自 Windows 系统 PATH，但 ZCode/Agent 的 Bash 会话可能没有完整继承。`C:\Program Files\GitHub CLI` 虽然在系统 PATH 里，但 Git Bash 不一定能解析到。

**结论**：别依赖 `gh` 简短命令。直接用完整路径：

```bash
"/c/Program Files/GitHub CLI/gh" repo list
"/c/Program Files/GitHub CLI/gh" auth status
```

或者先定位：

```bash
cmd.exe //c "where gh"    # 从 Windows cmd 查找
ls "/c/Program Files/GitHub CLI/gh.exe"   # 直接验证默认路径
```

**关键命令**：
```bash
# 验证 gh 可用
"/c/Program Files/GitHub CLI/gh" --version

# 创建仓库（必须用完整路径）
"/c/Program Files/GitHub CLI/gh" repo create pj-mmsn/项目名 --public

# 查看认证状态
"/c/Program Files/GitHub CLI/gh" auth status
```

> **为什么不用 `export PATH`？** 因为 ZCode 每个 Bash 调用是独立会话，shell 状态不持久化，export 不会保留到下次调用。每次都用完整路径最稳妥。

---

## 2026-07-04 多项目批量上传到 GitHub

**场景**：`E:\AI项目` 下面有两个项目 `ai-agent-java` 和 `ai-agent-starter`，需要分别创建独立仓库并推送。

**结论**：标准流程——建仓 → 初始化 git → 加 .gitignore → 推送。多个项目可以并行操作。

**完整流程**（以两个项目为例）：

```bash
# 第1步：并行创建两个空仓库（互不依赖，可同时跑）
"/c/Program Files/GitHub CLI/gh" repo create pj-mmsn/ai-agent-java --public
"/c/Program Files/GitHub CLI/gh" repo create pj-mmsn/ai-agent-starter --public

# 第2步：分别初始化并推送（各自独立，可并行）
cd "E:/AI项目/ai-agent-java" && \
  git init && git add -A && \
  git commit -m "init: ai-agent-java 项目初始化" && \
  git remote add origin https://github.com/pj-mmsn/ai-agent-java.git && \
  git branch -M main && git push -u origin main

cd "E:/AI项目/ai-agent-starter" && \
  git init && git add -A && \
  git commit -m "init: ai-agent-starter 项目初始化" && \
  git remote add origin https://github.com/pj-mmsn/ai-agent-starter.git && \
  git branch -M main && git push -u origin main
```

**踩坑记录**：

1. **`gh repo create --source=. --push` 报错 "not a git repository"**：这个命令要求目标目录已经是 git 仓库。如果目录还没 `git init`，必须分两步走——先 `gh repo create` 建空仓，再手动 `git init → add → commit → push`。

2. **不要忘了 .gitignore**：推送前检查有没有 `.gitignore`，否则 `target/`、`.venv/`、`.env`、`__pycache__/` 这些全会被推上去。按项目类型自动生成（见下方模板）。

3. **多个项目可以并行**：建仓互不依赖，推送也互不依赖——可以同时开两个 bash 调用来加速。

---

## 按项目类型生成 .gitignore

推送项目前，先判断项目类型，自动生成合适的 `.gitignore`：

| 判断依据 | 项目类型 | 应排除 |
|----------|----------|--------|
| 有 `pom.xml` / `build.gradle` | Java / Maven | `target/`, `.idea/`, `*.class`, `*.jar` |
| 有 `requirements.txt` / `setup.py` | Python | `__pycache__/`, `.venv/`, `*.pyc` |
| 有 `package.json` | Node.js | `node_modules/`, `dist/` |
| 以上都没有 | 通用 | `.idea/`, `.vscode/`, `.env`, `.DS_Store` |

**.env 文件铁律**：`.env` 绝不应提交（含 API Key 等密钥）。项目应提供 `.env.example` 作为模板，在 README 中说明用户需要复制并填写自己的密钥。

**相关**：
- 知识库同步：`knowledge-sync` 技能
- 单文件上传：`github-upload` 技能（场景 A）
- 技能目录：`C:\Users\Administrator\.agents\skills\github-upload\`
