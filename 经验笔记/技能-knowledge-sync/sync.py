#!/usr/bin/env python3
"""One-shot tool: sync knowledge base OR upload a single file to GitHub.

KB sync mode (default):
    sync.py ["commit message"]

Single-file upload mode:
    sync.py --file LOCAL_PATH --repo OWNER/REPO [--branch BRANCH]
            [--create-repo [public|private|internal]]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import datetime
import os

KB = r"E:\知识库"


# ── KB sync helpers ──────────────────────────────────────────────

def run(cmd: list[str], cwd: str = KB) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def die(msg: str, code: int = 1) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(code)


def ok(msg: str) -> None:
    print(f"✓ {msg}")


def ensure_proxy() -> None:
    cp = run(["git", "config", "--global", "--get", "http.proxy"])
    if cp.returncode != 0 or not cp.stdout.strip():
        die(
            "git 代理未配置,无法连接 GitHub。\n"
            "请先配置: git config --global http.proxy http://127.0.0.1:7890"
        )


def ensure_repo() -> None:
    cp = run(["git", "rev-parse", "--git-dir"])
    if cp.returncode != 0:
        die(f"{KB} 不是 git 仓库,请先 git init 并关联远程。")
    cp = run(["git", "remote", "get-url", "origin"])
    if cp.returncode != 0:
        die("没有配置远程仓库 origin。")


def has_changes() -> bool:
    run(["git", "add", "-A"])
    cp = run(["git", "diff", "--cached", "--quiet"])
    return cp.returncode != 0


def build_message(base: str | None) -> str:
    if base:
        return base
    cp = run(["git", "diff", "--cached", "--name-status"])
    lines = [l for l in cp.stdout.strip().split("\n") if l]
    if not lines:
        return f"sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
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
    readme = os.path.join(KB, "README.md")
    if os.path.exists(readme):
        return False
    dirs: list[str] = []
    files_list: list[str] = []
    try:
        for name in sorted(os.listdir(KB)):
            if name.startswith(".") or name == "README.md":
                continue
            full = os.path.join(KB, name)
            if os.path.isdir(full):
                dirs.append(name)
            elif not name.endswith(".bak"):
                files_list.append(name)
    except OSError:
        pass
    lines = ["# 知识库", "", "个人技术知识沉淀。", ""]
    if dirs:
        lines.append("## 目录")
        lines.append("")
        for d in dirs:
            lines.append(f"- **{d}**")
        lines.append("")
    if files_list:
        lines.append("## 文件")
        lines.append("")
        for f in files_list:
            lines.append(f"- {f}")
        lines.append("")
    lines.append("---")
    lines.append("> 通过 knowledge-sync 技能自动维护。")
    lines.append("")
    with open(readme, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return True


def ensure_skill_backup() -> bool:
    import shutil
    skill_dir = os.path.expandvars(r"%USERPROFILE%\.agents\skills\knowledge-sync")
    kb_dir = os.path.join(KB, "经验笔记", "技能-knowledge-sync")
    src_script = os.path.join(skill_dir, "scripts", "sync.py")
    src_skill = os.path.join(skill_dir, "SKILL.md")
    dst_script = os.path.join(kb_dir, "sync.py")
    dst_skill = os.path.join(kb_dir, "SKILL.md")
    changed = False
    os.makedirs(kb_dir, exist_ok=True)
    for src, dst in ((src_script, dst_script), (src_skill, dst_skill)):
        if not os.path.exists(dst) or _files_differ(src, dst):
            shutil.copy2(src, dst)
            changed = True
    return changed


def _files_differ(a: str, b: str) -> bool:
    try:
        import hashlib
        def h(p):
            with open(p, "rb") as f:
                return hashlib.sha256(f.read()).digest()
        return h(a) != h(b)
    except Exception:
        return True


# ── KB sync main ────────────────────────────────────────────────

def sync_kb(message: str | None) -> None:
    """Full knowledge-base sync: git add → commit → push."""
    print("知识库同步 → GitHub\n")
    ensure_repo()
    ensure_proxy()

    if ensure_readme():
        ok("自动生成 README.md")

    if ensure_skill_backup():
        ok("技能代码已同步到知识库")

    ok("已暂存所有变更")
    if not has_changes():
        ok("没有新变更,无需推送。")
        return

    msg = build_message(message)
    cp = run(["git", "commit", "-m", msg])
    if cp.returncode != 0:
        die(f"提交失败:\n{cp.stderr}")
    ok(f"提交: {msg}")

    print("  推送中...", end=" ", flush=True)
    cp = run(["git", "push"])
    if cp.returncode != 0:
        die(f"推送失败:\n{cp.stderr}")
    ok("推送完成！")
    print(f"\n  https://github.com/pj-mmsn/MMSN-knowledge")


# ── Single-file upload (delegates to upload_file.py) ────────────

def upload_single_file(repo: str, local: str, remote: str,
                        branch: str, message: str, create_repo: str | None) -> None:
    """Upload one file via GitHub Contents API using upload_file.py."""
    script = os.path.join(os.path.dirname(__file__), "upload_file.py")
    cmd = [
        sys.executable, script,
        repo, local, remote,
        "--branch", branch,
        "--message", message or f"Update {remote}",
    ]
    if create_repo is not None:
        cmd += ["--create-repo", create_repo]

    cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if cp.returncode != 0:
        print(cp.stderr.strip() or cp.stdout.strip(), file=sys.stderr)
        sys.exit(cp.returncode)
    print(cp.stdout.strip())


# ── CLI ──────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(
        description="Sync knowledge base to GitHub, or upload a single file."
    )
    p.add_argument(
        "--file", metavar="LOCAL_PATH",
        help="Upload a single file to GitHub (instead of syncing KB)",
    )
    p.add_argument(
        "--repo", metavar="OWNER/REPO",
        help="Target repo (required when --file is used)",
    )
    p.add_argument("--branch", default="main", help="Target branch (default: main)")
    p.add_argument(
        "--create-repo", nargs="?", const="private", metavar="VISIBILITY",
        help="Create repo if missing. Value: public/private/internal (default private)",
    )
    p.add_argument(
        "--message",
        help="Commit message (auto-generated if omitted)",
    )
    p.add_argument(
        "extra", nargs="*",
        help="Legacy: positional commit message for KB sync",
    )

    args = p.parse_args()

    # ── Single-file mode ──
    if args.file:
        if not args.repo:
            die("--repo is required when using --file")
        if "/" not in args.repo or len(args.repo.split("/")) != 2:
            die("--repo must be OWNER/REPO, e.g. pj-mmsn/my-notes")
        # Derive remote path from local filename if not specified
        remote = os.path.basename(args.file)
        upload_single_file(
            repo=args.repo,
            local=args.file,
            remote=remote,
            branch=args.branch,
            message=args.message or f"Upload {remote}",
            create_repo=args.create_repo,
        )
        return

    # ── KB sync mode (default) ──
    msg = args.message if args.message else (" ".join(args.extra) if args.extra else None)
    sync_kb(msg)


if __name__ == "__main__":
    main()
