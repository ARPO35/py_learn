"""pl status：显示答题目录状态和学习进度。"""

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
    """处理 status 命令。"""
    print("=== 答题目录状态 ===")
    print(f"答题目录: {workspace_path}")

    current_id = wm.get_current_exercise_id(workspace_path)

    if current_id is None:
        print("当前练习: (无)")
        print()
        print("使用 pl new <编号> 或 pl resume <编号> 开始练习")
        print()
        _print_progress(chapters, exercises, wm)
        return

    current_exercise = exercises.get(current_id)
    if current_exercise is None:
        print(f"当前练习: {current_id} (练习不存在)")
        print()
        _print_progress(chapters, exercises, wm)
        return

    print(f"当前练习: {current_id} -- {current_exercise.display_title()}")

    # 所属章节
    chapter = current_exercise.chapter
    if chapter:
        print(f"所属章节: {chapter.display_title()}")

    # 源路径
    source_path = wm.get_current_source_path(workspace_path)
    if source_path:
        print(f"源路径:    {source_path}")

    # 快照状态
    _print_snapshot_status(current_id, wm)

    print()
    _print_progress(chapters, exercises, wm)


def _print_snapshot_status(exercise_id: str, wm: WorkspaceManager) -> None:
    """打印当前练习的快照状态。"""
    store = wm.snapshot_store
    if store.has_snapshot(exercise_id):
        snap_dir = store._snapshot_dir(exercise_id)
        file_count = sum(1 for _ in snap_dir.rglob("*") if _.is_file())
        print(f"快照状态: 已保存 ({file_count} 个文件)")
    else:
        print("快照状态: 未保存")


def _print_progress(
    chapters: dict[str, Chapter],
    exercises: dict[str, Exercise],
    wm: WorkspaceManager,
) -> None:
    """按章节树打印学习进度。"""
    if not chapters:
        print("暂无任何章节。")
        return

    print("=== 学习进度 ===")

    # 构建父子关系
    children_map: dict[str | None, list[Chapter]] = {}
    for ch in chapters.values():
        parent = ch.parent
        children_map.setdefault(parent, []).append(ch)

    # 排序
    for k in children_map:
        children_map[k].sort(key=lambda c: c.order)

    # 根章节
    roots = [ch for ch in chapters.values() if ch.parent is None]
    roots.sort(key=lambda c: c.order)

    for root in roots:
        _print_chapter_progress(root, chapters, exercises, wm, children_map, indent=0)


def _print_chapter_progress(
    chapter: Chapter,
    chapters: dict[str, Chapter],
    exercises: dict[str, Exercise],
    wm: WorkspaceManager,
    children_map: dict[str | None, list[Chapter]],
    indent: int,
) -> None:
    """递归打印章节及其练习的完成状态。"""
    prefix = "  " * indent

    # 过滤此章节的练习
    chapter_exercises = [
        ex
        for ex in exercises.values()
        if ex.chapter and ex.chapter.id == chapter.id
    ]
    chapter_exercises.sort(key=lambda e: e.order)

    # 统计完成数
    completed = sum(
        1 for ex in chapter_exercises if wm.snapshot_store.has_snapshot(ex.id)
    )
    total = len(chapter_exercises)

    status_bar = _progress_bar(completed, total) if total > 0 else ""
    print(f"{prefix}{chapter.display_title()}  [{completed}/{total}] {status_bar}")

    # 打印子章节
    sub = children_map.get(chapter.id, [])
    for child in sub:
        _print_chapter_progress(child, chapters, exercises, wm, children_map, indent + 1)

    # 打印练习
    for ex in chapter_exercises:
        done = wm.snapshot_store.has_snapshot(ex.id)
        marker = "[OK]" if done else "[  ]"
        print(f"{prefix}  {marker} {ex.display_title()}")


def _progress_bar(completed: int, total: int, width: int = 10) -> str:
    """简单的进度条。"""
    if total == 0:
        return ""
    filled = round(completed / total * width)
    bar = "[" + "#" * filled + "-" * (width - filled) + "]"
    return bar
