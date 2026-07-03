#!/usr/bin/env python3
"""Sync the knowledge base (E:\\知识库) to GitHub in one shot.

Usage: sync.py [--message MSG]
"""
from __future__ import annotations

import subprocess
import sys
import datetime
import os

KB = r"E:\知识库"


def run(cmd: list[str], cwd: str = KB) -> subprocess.CompletedProcess:
    """Run a command in the KB directory, return completed process."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def die(msg: str, code: int = 1) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(code)


def ok(msg: str) -> None:
    print(f"✓ {msg}")


def ensure_proxy() -> None:
    """Make sure git has a proxy configured so it can reach GitHub."""
    cp = run(["git", "config", "--global", "--get", "http.proxy"])
    if cp.returncode != 0 or not cp.stdout.strip():
        die(
            "git 代理未配置,无法连接 GitHub。\n"
            "请先配置: git config --global http.proxy http://127.0.0.1:7890"
        )


def ensure_repo() -> None:
    """Make sure we're in a git repo with a remote named origin."""
    cp = run(["git", "rev-parse", "--git-dir"])
    if cp.returncode != 0:
        die(f"{KB} 不是 git 仓库,请先 git init 并关联远程。")
    cp = run(["git", "remote", "get-url", "origin"])
    if cp.returncode != 0:
        die("没有配置远程仓库 origin。")


def has_changes() -> bool:
    """True if there is anything to commit (tracked changes + new files)."""
    # Stage everything first, then check if the index differs from HEAD.
    run(["git", "add", "-A"])
    cp = run(["git", "diff", "--cached", "--quiet"])
    return cp.returncode != 0  # --quiet exits 1 when there ARE changes


def build_message(base: str | None) -> str:
    """Build a commit message. If base is given use it; otherwise summarize."""
    if base:
        return base

    # List changed/new/deleted files
    cp = run(["git", "diff", "--cached", "--name-status"])
    lines = [l for l in cp.stdout.strip().split("\n") if l]

    if not lines:
        return f"sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"

    # Group by top-level directory
    groups: dict[str, list[str]] = {}
    for line in lines:
        parts = line.split("\t")
        filename = parts[-1]
        top = filename.split("/")[0]
        groups.setdefault(top, []).append(filename)

    summarise: list[str] = []
    for top, files in groups.items():
        if len(files) <= 2:
            summarise.append(f"{top}({', '.join(f.split('/')[-1] for f in files)})")
        else:
            summarise.append(f"{top}({len(files)}个文件)")
    return "sync: " + "; ".join(summarise)


def ensure_readme() -> bool:
    """If README.md is missing from KB root, create one. Returns True if created."""
    readme = os.path.join(KB, "README.md")
    if os.path.exists(readme):
        return False

    # Scan top-level directories (exclude .git, __pycache__, hidden dirs)
    dirs: list[str] = []
    files: list[str] = []
    try:
        for name in sorted(os.listdir(KB)):
            if name.startswith(".") or name == "README.md":
                continue
            full = os.path.join(KB, name)
            if os.path.isdir(full):
                dirs.append(name)
            elif not name.endswith(".bak"):
                files.append(name)
    except OSError:
        pass

    lines = [
        "# 知识库",
        "",
        "个人技术知识沉淀。",
        "",
    ]
    if dirs:
        lines.append("## 目录")
        lines.append("")
        for d in dirs:
            lines.append(f"- **{d}**")
        lines.append("")
    if files:
        lines.append("## 文件")
        lines.append("")
        for f in files:
            lines.append(f"- {f}")
        lines.append("")

    lines.append("---")
    lines.append("> 通过 knowledge-sync 技能自动维护。")
    lines.append("")

    with open(readme, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return True


def ensure_skill_backup() -> bool:
    """Copy the skill's own source into the KB so it's version-controlled too."""
    import shutil
    skill_dir = os.path.expandvars(r"%USERPROFILE%\.agents\skills\knowledge-sync")
    kb_dir = os.path.join(KB, "经验笔记", "技能-knowledge-sync")

    # Source files to mirror
    src_script = os.path.join(skill_dir, "scripts", "sync.py")
    src_skill = os.path.join(skill_dir, "SKILL.md")
    dst_script = os.path.join(kb_dir, "sync.py")
    dst_skill = os.path.join(kb_dir, "SKILL.md")

    changed = False
    os.makedirs(kb_dir, exist_ok=True)

    if not os.path.exists(dst_script) or _files_differ(src_script, dst_script):
        shutil.copy2(src_script, dst_script)
        changed = True
    if not os.path.exists(dst_skill) or _files_differ(src_skill, dst_skill):
        shutil.copy2(src_skill, dst_skill)
        changed = True

    return changed


def _files_differ(a: str, b: str) -> bool:
    """Quick content comparison by size + hash."""
    try:
        import hashlib
        def h(p):
            with open(p, "rb") as f:
                return hashlib.sha256(f.read()).digest()
        return h(a) != h(b)
    except Exception:
        return True  # treat errors as "differ"


def main() -> None:
    message = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--message" and len(sys.argv) > 2:
            message = sys.argv[2]
        elif not sys.argv[1].startswith("--"):
            message = sys.argv[1]

    print("知识库同步 → GitHub\n")

    # 1. Pre-flight
    ensure_repo()
    ensure_proxy()

    # 2. 确保 README 存在
    if ensure_readme():
        ok("自动生成 README.md")

    # 3. 同步技能自身代码到知识库
    if ensure_skill_backup():
        ok("技能代码已同步到知识库")

    # 4. Stage
    ok("已暂存所有变更")
    if not has_changes():
        ok("没有新变更,无需推送。")
        return

    # 3. Commit
    msg = build_message(message)
    cp = run(["git", "commit", "-m", msg])
    if cp.returncode != 0:
        die(f"提交失败:\n{cp.stderr}")

    ok(f"提交: {msg}")

    # 4. Push
    print("  推送中...", end=" ", flush=True)
    cp = run(["git", "push"])
    if cp.returncode != 0:
        die(f"推送失败:\n{cp.stderr}")

    ok("推送完成！")
    print(f"\n  https://github.com/pj-mmsn/MMSN-knowledge")


if __name__ == "__main__":
    main()
