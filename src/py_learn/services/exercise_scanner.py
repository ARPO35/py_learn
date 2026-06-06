"""练习扫描与元数据继承。"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from ..domain.models import Chapter, Exercise


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """按字段级合并两个字典，override 覆盖 base。"""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _scan_toml_files(root: Path) -> list[dict[str, Any]]:
    """递归查找所有 exercise.toml 并解析。

    返回按目录深度的列表，浅层在前。
    """
    results: list[dict[str, Any]] = []
    for toml_path in sorted(root.rglob("exercise.toml"), key=lambda p: len(p.parts)):
        try:
            data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
        except Exception as e:
            raise RuntimeError(f"无法解析 {toml_path}: {e}") from e
        data["_toml_path"] = toml_path
        data["_dir"] = toml_path.parent
        results.append(data)
    return results


def build_exercises(
    content_dirs: list[Path],
) -> tuple[dict[str, Exercise], dict[str, Chapter]]:
    """扫描所有内容目录，构建练习和章节。

    返回 (exercises, chapters)。
    - exercises: {exercise_id: Exercise}
    - chapters: {chapter_id: Chapter}
    """
    exercises: dict[str, Exercise] = {}
    chapters: dict[str, Chapter] = {}

    for content_dir in content_dirs:
        if not content_dir.exists():
            continue

        tomls = _scan_toml_files(content_dir)

        # 第一遍：收集所有章节元数据（包括路径继承链）
        # 路径继承链：按目录前缀构建
        # 例如 root/A/B/C/exercise.toml 继承 root/A/exercise.toml 和 root/A/B/exercise.toml
        chapter_tomls_by_dir: dict[Path, dict[str, Any]] = {}
        exercise_tomls: list[dict[str, Any]] = []

        for data in tomls:
            toml_type = data.get("type", "")
            if toml_type == "chapter":
                chapter_tomls_by_dir[data["_dir"]] = data
            elif toml_type == "exercise":
                exercise_tomls.append(data)
            else:
                raise RuntimeError(
                    f"未知 type: {toml_type!r} in {data['_toml_path']}"
                )

        # 第二遍：处理章节，构建章节字典
        # 先按目录深度排序，确保父目录先处理
        sorted_chapter_dirs = sorted(
            chapter_tomls_by_dir.keys(), key=lambda p: len(p.parts)
        )

        for cdir in sorted_chapter_dirs:
            data = chapter_tomls_by_dir[cdir]
            chapter_data = data.get("chapter", {})
            if not chapter_data:
                continue

            cid = chapter_data.get("id")
            if not cid:
                raise RuntimeError(f"章节缺少 id: {data['_toml_path']}")

            parent = chapter_data.get("parent")
            # 如果未显式声明 parent，尝试从路径推断
            if parent is None:
                parent_dir = cdir.parent
                if parent_dir in chapter_tomls_by_dir:
                    parent_chapter_data = chapter_tomls_by_dir[parent_dir].get(
                        "chapter", {}
                    )
                    parent = parent_chapter_data.get("id")

            chapters[cid] = Chapter(
                id=cid,
                title=chapter_data.get("title", ""),
                order=int(chapter_data.get("order", 0)),
                parent=parent,
            )

        # 第三遍：处理练习，合并继承元数据
        for data in exercise_tomls:
            exercise_dir = data["_dir"]

            # 收集路径上所有 chapter.toml
            inherited: dict[str, Any] = {}
            current = exercise_dir
            ancestor_chain: list[dict[str, Any]] = []
            while True:
                if current in chapter_tomls_by_dir:
                    ancestor_chain.append(chapter_tomls_by_dir[current])
                parent_dir = current.parent
                if parent_dir == current or parent_dir == content_dir.parent:
                    break
                current = parent_dir

            # 反转，从最外层开始合并
            ancestor_chain.reverse()
            for anc in ancestor_chain:
                anc_chapter = anc.get("chapter", {})
                inherited = _deep_merge(inherited, {"chapter": anc_chapter})

            # 合并练习自身元数据
            merged = _deep_merge(inherited, data)

            eid = merged.get("id")
            if not eid:
                raise RuntimeError(f"练习缺少 id: {data['_toml_path']}")

            if eid in exercises:
                existing = exercises[eid]
                raise RuntimeError(
                    f"Exercise ID 冲突: {eid!r}\n"
                    f"  已有: {existing.source_path}\n"
                    f"  新发现: {exercise_dir}"
                )

            # 提取或注册章节
            chapter_info = merged.get("chapter", {})
            chapter = None
            if chapter_info:
                cid = chapter_info.get("id", "")
                if cid and cid not in chapters:
                    # 练习自身声明了章节，但之前没被 chapter.toml 声明
                    # 推断父章节
                    parent_id = chapter_info.get("parent")
                    chapters[cid] = Chapter(
                        id=cid,
                        title=chapter_info.get("title", ""),
                        order=int(chapter_info.get("order", 0)),
                        parent=parent_id,
                    )
                if cid and cid in chapters:
                    chapter = chapters[cid]

            exercises[eid] = Exercise(
                id=eid,
                title=merged.get("title", ""),
                order=int(merged.get("order", 0)),
                chapter=chapter,
                source_path=Path(exercise_dir),
                question_path=merged.get("question", "q.md"),
                answer_path=merged.get("answer", "a.py"),
                cases_path=merged.get("cases", "cases.py"),
            )

    return exercises, chapters
