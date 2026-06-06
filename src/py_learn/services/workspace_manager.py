"""答题目录管理。"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from ..domain.models import Exercise
from ..io.ignore import Plignore
from .snapshot_store import SnapshotStore

PL_DIR = ".pl"
STATE_FILE = "state.json"
MANIFEST_FILE = "manifest.json"
PLIGNORE_FILE = ".plignore"


class WorkspaceManager:
    """管理答题目录的切换、保存和恢复。"""

    def __init__(
        self,
        snapshot_store: SnapshotStore,
        exercises: dict[str, Exercise],
    ) -> None:
        self.snapshot_store = snapshot_store
        self.exercises = exercises

    def get_current_exercise_id(self, workspace_path: Path) -> str | None:
        """获取当前答题目录承载的练习编号。"""
        state_path = workspace_path / PL_DIR / STATE_FILE
        if not state_path.exists():
            return None
        try:
            data = json.loads(state_path.read_text(encoding="utf-8"))
            return data.get("exercise_id")
        except (json.JSONDecodeError, OSError):
            return None

    def get_current_source_path(self, workspace_path: Path) -> Path | None:
        """获取当前练习的原始路径。"""
        state_path = workspace_path / PL_DIR / STATE_FILE
        if not state_path.exists():
            return None
        try:
            data = json.loads(state_path.read_text(encoding="utf-8"))
            path_str = data.get("source_path")
            return Path(path_str) if path_str else None
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, workspace_path: Path) -> bool:
        """保存当前答题进度。返回是否成功保存。"""
        current_id = self.get_current_exercise_id(workspace_path)
        if not current_id:
            print("当前答题目录没有承载任何练习。")
            return False

        plignore = self._get_plignore(workspace_path)
        saved = self.snapshot_store.save(current_id, workspace_path, plignore)
        print(f"已保存练习 {current_id} 的进度（{len(saved)} 个文件）。")
        return True

    def new(self, exercise_id: str, workspace_path: Path) -> None:
        """从原始练习开始。"""
        exercise = self.exercises.get(exercise_id)
        if not exercise:
            print(f"未找到练习: {exercise_id}")
            return

        current_id = self.get_current_exercise_id(workspace_path)

        # 跨练习切换时保存当前进度
        if current_id and current_id != exercise_id:
            self.save(workspace_path)

        # 当前练习不保存（直接丢弃未保存修改）

        # 清理
        self._clean_workspace(workspace_path)

        # 复制练习源
        manifest_files = self._copy_exercise_source(exercise, workspace_path)

        # 保存状态
        self._save_state(workspace_path, exercise_id, exercise.source_path, manifest_files)

        print(f"已切换到练习 {exercise_id}: {exercise.title}")

    def resume(self, exercise_id: str, workspace_path: Path) -> None:
        """恢复练习的上一次答题进度。"""
        exercise = self.exercises.get(exercise_id)
        if not exercise:
            print(f"未找到练习: {exercise_id}")
            return

        current_id = self.get_current_exercise_id(workspace_path)

        # 跨练习切换时保存当前进度
        if current_id and current_id != exercise_id:
            self.save(workspace_path)

        # 当前练习不保存

        # 清理
        self._clean_workspace(workspace_path)

        # 先复制练习源（确保学习材料存在）
        manifest_files = self._copy_exercise_source(exercise, workspace_path)

        # 恢复快照
        if self.snapshot_store.has_snapshot(exercise_id):
            restored = self.snapshot_store.load(exercise_id, workspace_path)
            manifest_files.extend(restored)
            print(
                f"已恢复练习 {exercise_id}: {exercise.title}（{len(restored)} 个文件）"
            )
        else:
            print(
                f"练习 {exercise_id}: {exercise.title} 没有保存的进度，已从原始练习开始。"
            )

        # 保存状态
        self._save_state(
            workspace_path, exercise_id, exercise.source_path, manifest_files
        )

    def next(self, workspace_path: Path) -> None:
        """跳到下一个练习。"""
        # 排序所有练习
        def _sort_key(eid: str):
            ex = self.exercises[eid]
            ch = ex.chapter
            return (
                ch.order if ch else 0,
                ch.id if ch else "",
                ex.order,
            )

        sorted_ids = sorted(self.exercises.keys(), key=_sort_key)

        if not sorted_ids:
            print("没有找到任何练习。")
            return

        current_id = self.get_current_exercise_id(workspace_path)

        # 保存当前进度
        if current_id:
            self.save(workspace_path)

        # 查找下一个
        if current_id and current_id in sorted_ids:
            idx = sorted_ids.index(current_id)
            if idx + 1 < len(sorted_ids):
                next_id = sorted_ids[idx + 1]
                exercise = self.exercises[next_id]
                if self.snapshot_store.has_snapshot(next_id):
                    self.resume(next_id, workspace_path)
                else:
                    self.new(next_id, workspace_path)
            else:
                print("已经是最后一个练习了。")
        else:
            # 从第一个开始
            first_id = sorted_ids[0]
            exercise = self.exercises[first_id]
            if self.snapshot_store.has_snapshot(first_id):
                self.resume(first_id, workspace_path)
            else:
                self.new(first_id, workspace_path)

    def _copy_exercise_source(
        self, exercise: Exercise, workspace_path: Path
    ) -> list[str]:
        """复制练习源文件到答题目录，返回管理文件列表。"""
        workspace_path.mkdir(parents=True, exist_ok=True)

        source = exercise.source_path
        exclude = {
            "exercise.toml",
            exercise.cases_path,
        }
        manifest_files: list[str] = []

        for item in source.iterdir():
            if item.name in exclude:
                continue
            if item.name.startswith("."):
                # 跳过隐藏文件（但 .pl 由我们自己管理）
                continue

            relative_name = item.name
            dest = workspace_path / relative_name

            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                manifest_files.append(relative_name)
            else:
                shutil.copy2(item, dest)
                manifest_files.append(relative_name)

        # 处理 .plignore
        pl_dir = workspace_path / PL_DIR
        pl_dir.mkdir(exist_ok=True)

        plignore_src = source / ".plignore"
        if plignore_src.exists():
            dest_ignore = pl_dir / PLIGNORE_FILE
            shutil.copy2(plignore_src, dest_ignore)
        else:
            # 写入默认忽略规则
            ignore = Plignore.default()
            ignore.write_default(pl_dir / PLIGNORE_FILE)

        return manifest_files

    def _clean_workspace(self, workspace_path: Path) -> None:
        """安全清理答题目录中的 CLI 管理文件。"""
        manifest_path = workspace_path / PL_DIR / MANIFEST_FILE
        if not manifest_path.exists():
            return

        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            files = data.get("managed_files", [])
        except (json.JSONDecodeError, OSError):
            files = []

        for f in files:
            target = workspace_path / f
            if target.is_dir():
                if target.exists():
                    shutil.rmtree(target)
            elif target.exists():
                target.unlink()

        # 清理 manifest 文件自身
        if manifest_path.exists():
            manifest_path.unlink()

    def _save_state(
        self,
        workspace_path: Path,
        exercise_id: str,
        source_path: Path,
        manifest_files: list[str],
    ) -> None:
        """写入状态和 manifest 文件。"""
        pl_dir = workspace_path / PL_DIR
        pl_dir.mkdir(exist_ok=True)

        state = {"exercise_id": exercise_id, "source_path": str(source_path)}
        (pl_dir / STATE_FILE).write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        manifest = {"managed_files": list(set(manifest_files))}
        (pl_dir / MANIFEST_FILE).write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _get_plignore(self, workspace_path: Path) -> Plignore:
        """获取当前答题目录的忽略规则。"""
        ignore_path = workspace_path / PL_DIR / PLIGNORE_FILE
        if ignore_path.exists():
            return Plignore.from_file(ignore_path)
        return Plignore.default()
