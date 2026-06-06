"""pl ls：列出章节或练习。"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.tree import Tree

from ..domain.models import Chapter, Exercise
from ..services.workspace_manager import WorkspaceManager


def handle(
    args,
    wm: WorkspaceManager,
    exercises: dict[str, Exercise],
    chapters: dict[str, Chapter],
    workspace_path: Path,
) -> None:
    """处理 ls 命令。"""
    console = Console()
    chapter_arg = args.chapter

    if chapter_arg:
        _list_exercises_in_chapter(console, chapter_arg, exercises, chapters)
    else:
        _list_chapters(console, chapters)


def _list_chapters(console: Console, chapters: dict[str, Chapter]) -> None:
    """列出章节树。"""
    if not chapters:
        console.print("[dim]暂无任何章节。[/dim]")
        return

    # 构建父子关系
    children_map: dict[str | None, list[Chapter]] = {}
    for ch in chapters.values():
        parent = ch.parent
        children_map.setdefault(parent, []).append(ch)

    # 排序
    for k in children_map:
        children_map[k].sort(key=lambda c: c.order)

    # 找到根章节（没有 parent 或 parent 不在 chapters 中）
    roots = [ch for ch in chapters.values() if ch.parent is None]
    roots.sort(key=lambda c: c.order)

    tree = Tree("[bold]章节列表[/bold]")
    for root in roots:
        root_branch = tree.add(root.display_title())
        _add_sub_chapters(root_branch, root.id, children_map)

    console.print(tree)


def _add_sub_chapters(
    branch: Tree,
    parent_id: str,
    children_map: dict[str | None, list[Chapter]],
) -> None:
    """递归添加子章节到 Tree 分支。"""
    sub = children_map.get(parent_id, [])
    for child in sub:
        child_branch = branch.add(child.display_title())
        _add_sub_chapters(child_branch, child.id, children_map)


def _list_exercises_in_chapter(
    console: Console,
    chapter_id: str,
    exercises: dict[str, Exercise],
    chapters: dict[str, Chapter],
) -> None:
    """列出指定章节的练习。"""
    if chapter_id not in chapters:
        console.print(f"[red]未找到章节: {chapter_id}[/red]")
        return

    chapter = chapters[chapter_id]
    tree = Tree(chapter.display_title())

    # 过滤属于此章节的练习
    chapter_exercises = [
        ex for ex in exercises.values() if ex.chapter and ex.chapter.id == chapter_id
    ]
    chapter_exercises.sort(key=lambda e: e.order)

    if not chapter_exercises:
        tree.add("[dim]（该章节暂无练习）[/dim]")
    else:
        for ex in chapter_exercises:
            tree.add(ex.display_title())

    console.print(tree)
