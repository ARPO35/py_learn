"""pl resume：恢复练习进度。"""

from __future__ import annotations

from pathlib import Path

from ..domain.models import Exercise
from ..services.workspace_manager import WorkspaceManager


def handle(
    args,
    wm: WorkspaceManager,
    exercises: dict[str, Exercise],
    workspace_path: Path,
) -> None:
    """处理 resume 命令。"""
    exercise_id = args.exercise_id

    if exercise_id not in exercises:
        print(f"未找到练习: {exercise_id}")
        return

    wm.resume(exercise_id, workspace_path)
