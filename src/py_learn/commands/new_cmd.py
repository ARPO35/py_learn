"""pl new：从原始练习开始。"""

from __future__ import annotations

from pathlib import Path
from rich.console import Console


from ..domain.models import Exercise
from ..services.workspace_manager import WorkspaceManager


def handle(
    args,
    wm: WorkspaceManager,
    exercises: dict[str, Exercise],
    workspace_path: Path,
) -> None:
    """处理 new 命令。"""
    exercise_id = args.exercise_id

    if exercise_id not in exercises:
        console = Console()
        console.print(f"[red]未找到练习: {exercise_id}[/red]")
        return

    wm.new(exercise_id, workspace_path)
