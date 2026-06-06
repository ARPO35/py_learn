"""领域模型定义。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Chapter:
    """章节。"""

    id: str
    title: str = ""
    order: int = 0
    parent: Optional[str] = None

    def display_title(self) -> str:
        """章节显示标题：编号 + 标题"""
        if self.title:
            return f"{self.id}. {self.title}"
        return self.id


@dataclass
class Exercise:
    """练习。"""

    id: str
    title: str = ""
    order: int = 0
    chapter: Optional[Chapter] = None
    source_path: Path = field(default_factory=Path)
    question_path: str = "q.md"
    answer_path: str = "a.py"
    cases_path: str = "cases.py"

    def display_title(self) -> str:
        """练习显示标题：序号 + 标题"""
        if self.title:
            return f"{self.order}. {self.title}"
        return f"{self.order}. {self.id}"

    def exercise_toml_relative_path(self) -> Path:
        """该练习的 exercise.toml 绝对路径"""
        return self.source_path / "exercise.toml"
