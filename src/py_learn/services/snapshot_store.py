"""答题进度快照存储。"""

from __future__ import annotations

import shutil
from pathlib import Path

from ..io.ignore import Plignore


class SnapshotStore:
    """管理练习的答题进度快照。"""

    def __init__(self, store_dir: Path) -> None:
        self.store_dir = store_dir
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def _snapshot_dir(self, exercise_id: str) -> Path:
        """获取特定练习的快照目录。"""
        safe_id = exercise_id.replace("/", "_").replace("\\", "_")
        return self.store_dir / safe_id

    def has_snapshot(self, exercise_id: str) -> bool:
        """检查是否存在该练习的快照。"""
        snap_dir = self._snapshot_dir(exercise_id)
        return snap_dir.exists() and any(snap_dir.iterdir())

    def save(
        self,
        exercise_id: str,
        workspace_path: Path,
        plignore: Plignore,
    ) -> list[str]:
        """保存答题目录到快照（排除 plignore 匹配项）。

        返回保存的文件相对路径列表。
        """
        snap_dir = self._snapshot_dir(exercise_id)
        # 清空旧快照
        if snap_dir.exists():
            shutil.rmtree(snap_dir)
        snap_dir.mkdir(parents=True, exist_ok=True)

        saved_files: list[str] = []
        for item in workspace_path.rglob("*"):
            if item == snap_dir:
                continue
            rel = str(item.relative_to(workspace_path)).replace("\\", "/")

            # 忽略 .pl 目录
            if rel.startswith(".pl"):
                continue

            # 检查 plignore
            if plignore.should_ignore(rel):
                continue

            if item.is_file():
                dest = snap_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                saved_files.append(rel)

        return saved_files

    def load(
        self,
        exercise_id: str,
        workspace_path: Path,
    ) -> list[str]:
        """从快照恢复文件到答题目录。

        返回恢复的文件相对路径列表。
        """
        snap_dir = self._snapshot_dir(exercise_id)
        if not snap_dir.exists():
            return []

        restored_files: list[str] = []
        for item in snap_dir.rglob("*"):
            if item.is_file():
                rel = str(item.relative_to(snap_dir)).replace("\\", "/")
                dest = workspace_path / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                restored_files.append(rel)

        return restored_files

    def clear(self, exercise_id: str) -> None:
        """删除指定练习的快照。"""
        snap_dir = self._snapshot_dir(exercise_id)
        if snap_dir.exists():
            shutil.rmtree(snap_dir)
