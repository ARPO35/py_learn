"""pl ls：列出章节或练习。"""

from __future__ import annotations

from pathlib import Path

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
    chapter_arg = args.chapter

    if chapter_arg:
        _list_exercises_in_chapter(chapter_arg, exercises, chapters)
    else:
        _list_chapters(chapters)


def _list_chapters(chapters: dict[str, Chapter]) -> None:
    """列出章节树。"""
    if not chapters:
        print("暂无任何章节。")
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

    for root in roots:
        print(root.display_title())
        _print_sub_chapters(root, chapters, children_map, indent=0)


def _print_sub_chapters(
    chapter: Chapter,
    chapters: dict[str, Chapter],
    children_map: dict[str | None, list[Chapter]],
    indent: int,
) -> None:
    """递归打印子章节。"""
    sub = children_map.get(chapter.id, [])
    sub.sort(key=lambda c: c.order)
    for child in sub:
        prefix = "|--" if indent == 0 else "   " * indent + "|--"
        print(f"{prefix} {child.display_title()}")
        _print_sub_chapters(child, chapters, children_map, indent + 1)


def _list_exercises_in_chapter(
    chapter_id: str,
    exercises: dict[str, Exercise],
    chapters: dict[str, Chapter],
) -> None:
    """列出指定章节的练习。"""
    if chapter_id not in chapters:
        print(f"未找到章节: {chapter_id}")
        return

    chapter = chapters[chapter_id]
    print(chapter.display_title())

    # 过滤属于此章节的练习
    chapter_exercises = [
        ex for ex in exercises.values() if ex.chapter and ex.chapter.id == chapter_id
    ]
    chapter_exercises.sort(key=lambda e: e.order)

    if not chapter_exercises:
        print("  （该章节暂无练习）")
        return

    for ex in chapter_exercises:
        print(f"|-- {ex.display_title()}")
