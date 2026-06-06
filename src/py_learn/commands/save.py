"""pl save：保存当前答题进度。"""

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
    """处理 save 命令。"""
    wm.save(workspace_path)
