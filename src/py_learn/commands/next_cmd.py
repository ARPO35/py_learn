"""pl next：跳到下一练习。"""

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
    """处理 next 命令。"""
    wm.next(workspace_path)
