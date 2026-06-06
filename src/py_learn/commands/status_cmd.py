"""pl status：显示答题目录状态和学习进度。"""

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..domain.models import Chapter, Exercise
from ..services.workspace_manager import WorkspaceManager


def _make_bar(completed: int, total: int, width: int = 10) -> Text:
    """构建 Rich Text 进度条（Unicode 块字符）。"""
    if total == 0:
        return Text("")
    filled = round(completed / total * width)
    bar = Text()
    bar.append("█" * filled, style="green")
    bar.append("░" * (width - filled), style="dim")
    return bar


def handle(
    args,
    wm: WorkspaceManager,
    exercises: dict[str, Exercise],
    chapters: dict[str, Chapter],
    workspace_path: Path,
) -> None:
    """处理 status 命令。"""
    console = Console(file=sys.stdout)
    current_id = wm.get_current_exercise_id(workspace_path)

    # ---- 答题目录状态 Panel ----
    status_lines = ["答题目录:"]
    status_lines.append(f"  {workspace_path}")

    if current_id is None:
        status_lines.append("当前练习: [dim](无)[/dim]")
    else:
        current_exercise = exercises.get(current_id)
        if current_exercise is None:
            status_lines.append(
                f"当前练习: [bold red]{current_id} (练习不存在)[/bold red]"
            )
        else:
            status_lines.append(
                f"当前练习: {current_id} -- {current_exercise.display_title()}"
            )

            chapter = current_exercise.chapter
            if chapter:
                status_lines.append(f"所属章节: {chapter.display_title()}")

            source_path = wm.get_current_source_path(workspace_path)
            if source_path:
                status_lines.append("源路径:")
                status_lines.append(f"  {source_path}")

            # 快照状态
            store = wm.snapshot_store
            if store.has_snapshot(current_id):
                snap_dir = store._snapshot_dir(current_id)
                file_count = sum(1 for _ in snap_dir.rglob("*") if _.is_file())
                status_lines.append(
                    f"快照状态: [green]已保存 ({file_count} 个文件)[/green]"
                )
            else:
                status_lines.append("快照状态: [yellow]未保存[/yellow]")

    console.print(
        Panel("\n".join(status_lines), title="答题目录状态", title_align="left")
    )

    # 无练习时的提示
    if current_id is None:
        console.print()
        console.print("[yellow]使用 pl new <编号> 或 pl resume <编号> 开始练习[/yellow]")

    # ---- 学习进度 ----
    console.print()
    _print_progress(console, chapters, exercises, wm)


def _print_progress(
    console: Console,
    chapters: dict[str, Chapter],
    exercises: dict[str, Exercise],
    wm: WorkspaceManager,
) -> None:
    """按章节打印学习进度（Rich Table + 练习列表）。"""
    if not chapters:
        console.print("[dim]暂无任何章节。[/dim]")
        return

    # 构建父子关系
    children_map: dict[str | None, list[Chapter]] = {}
    for ch in chapters.values():
        parent = ch.parent
        children_map.setdefault(parent, []).append(ch)

    for k in children_map:
        children_map[k].sort(key=lambda c: c.order)

    # 按章节分组练习
    chapter_exercises_map: dict[str, list[Exercise]] = {}
    for ex in exercises.values():
        if ex.chapter:
            chapter_exercises_map.setdefault(ex.chapter.id, []).append(ex)
    for v in chapter_exercises_map.values():
        v.sort(key=lambda e: e.order)

    # 构建 Table
    table = Table(title="学习进度", title_style="bold")
    table.add_column("章节", style="cyan", no_wrap=True)
    table.add_column("完成", justify="center", style="green")
    table.add_column("进度", justify="left")

    def add_rows(ch: Chapter, indent: int) -> None:
        ch_exs = chapter_exercises_map.get(ch.id, [])
        completed = sum(
            1 for ex in ch_exs if wm.snapshot_store.has_snapshot(ex.id)
        )
        total = len(ch_exs)
        count_str = f"{completed}/{total}" if total > 0 else "-"
        bar = _make_bar(completed, total) if total > 0 else Text("")

        prefix = "  " * indent
        table.add_row(f"{prefix}{ch.display_title()}", count_str, bar)

        # 子章节
        for child in children_map.get(ch.id, []):
            add_rows(child, indent + 1)

        # 练习条目
        for ex in ch_exs:
            done = wm.snapshot_store.has_snapshot(ex.id)
            marker = Text("✓", style="green") if done else Text("○", style="dim")
            ex_prefix = "  " * (indent + 1)
            ex_text = Text()
            ex_text.append(ex_prefix)
            ex_text.append(marker)
            ex_text.append(f" {ex.display_title()}")
            table.add_row(ex_text, Text(""), Text(""))

    roots = [ch for ch in chapters.values() if ch.parent is None]
    roots.sort(key=lambda c: c.order)

    for root in roots:
        add_rows(root, 0)

    console.print(table)
