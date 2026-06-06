"""pl CLI 入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from .services.exercise_scanner import build_exercises
from .services.snapshot_store import SnapshotStore
from .services.workspace_manager import WorkspaceManager
from .io.paths import get_builtin_content_dir, get_extra_content_dirs, get_snapshot_store_dir


def build_parser() -> argparse.ArgumentParser:
    """构建参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="pl",
        description="Python 学习 CLI（pl）",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # ls
    ls_parser = subparsers.add_parser("ls", help="列出章节或练习")
    ls_parser.add_argument(
        "chapter",
        nargs="?",
        default=None,
        help="章节编号（可选），不指定则列出所有章节",
    )

    # new
    new_parser = subparsers.add_parser("new", help="从原始练习开始")
    new_parser.add_argument("exercise_id", help="练习编号，例如 A.1，B1.2")

    # resume
    resume_parser = subparsers.add_parser("resume", help="恢复练习进度")
    resume_parser.add_argument("exercise_id", help="练习编号")

    # save
    subparsers.add_parser("save", help="保存当前答题进度")

    # next
    subparsers.add_parser("next", help="跳到下一练习")

    # run
    subparsers.add_parser("run", help="运行调试用例")

    # submit
    subparsers.add_parser("submit", help="提交验证")
    # status
    subparsers.add_parser("status", help="显示答题目录状态和学习进度")

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI 主入口。"""
    console = Console(stderr=True)
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    # 收集内容目录
    content_dirs = []
    builtin = get_builtin_content_dir()
    if builtin.exists():
        content_dirs.append(builtin)
    content_dirs.extend(get_extra_content_dirs())

    if not content_dirs:
        console.print("[red]未找到任何内容目录。[/]")
        return 1

    # 扫描练习和章节
    try:
        exercises, chapters = build_exercises(content_dirs)
    except RuntimeError as e:
        console.print(Panel(str(e), title="[red]扫描练习失败[/]", border_style="red"))
        return 1

    # 初始化管理器
    snapshot_store = SnapshotStore(get_snapshot_store_dir())
    wm = WorkspaceManager(snapshot_store, exercises, console=console)
    workspace_path = Path.cwd()

    # 分派命令
    from .commands import (
        handle_ls,
        handle_new,
        handle_resume,
        handle_save,
        handle_run,
        handle_submit,
        handle_next,
        handle_status,
    )

    handlers = {
        "ls": lambda: handle_ls(args, wm, exercises, chapters, workspace_path),
        "new": lambda: handle_new(args, wm, exercises, workspace_path),
        "resume": lambda: handle_resume(args, wm, exercises, workspace_path),
        "save": lambda: handle_save(args, wm, exercises, workspace_path),
        "next": lambda: handle_next(args, wm, exercises, workspace_path),
        "run": lambda: handle_run(args, wm, exercises, workspace_path),
        "submit": lambda: handle_submit(args, wm, exercises, workspace_path),
        "status": lambda: handle_status(args, wm, exercises, chapters, workspace_path),
    }

    handler = handlers.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    try:
        handler()
    except Exception as e:
        console.print(f"[red]执行失败:[/] {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
