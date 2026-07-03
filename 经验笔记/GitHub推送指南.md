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
