"""Ignore 文件匹配（类似 .gitignore 语义）。"""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path

DEFAULT_IGNORE_PATTERNS = [
    "q.md",
    ".pl/",
    "__pycache__/",
    "*.pyc",
]


class Plignore:
    """管理保存时的忽略规则。"""

    def __init__(
        self,
        patterns: list[str] | None = None,
    ) -> None:
        self.patterns: list[str] = list(patterns or [])

    @classmethod
    def from_file(cls, path: Path) -> Plignore:
        """从 .plignore 文件加载规则。"""
        instance = cls()
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    instance.patterns.append(line)
        return instance

    @classmethod
    def default(cls) -> Plignore:
        """返回默认忽略规则。"""
        return cls(patterns=list(DEFAULT_IGNORE_PATTERNS))

    def should_ignore(self, relative_path: str) -> bool:
        """判断相对路径是否应被忽略。"""
        rel = relative_path.replace("\\", "/")
        for pattern in self.patterns:
            pat = pattern.replace("\\", "/")
            # 目录模式
            if pat.endswith("/"):
                # 如果相对路径本身是前缀或子项
                if rel == pat.rstrip("/") or rel.startswith(pat):
                    return True
            # 通配符匹配
            if fnmatch(rel, pat):
                return True
            # 文件名匹配（非路径分隔符模式）
            if "/" not in pat and "/" not in rel:
                if fnmatch(rel, pat):
                    return True
        return False

    def write_default(self, path: Path) -> None:
        """写入默认忽略规则到指定路径。"""
        content = "\n".join(DEFAULT_IGNORE_PATTERNS) + "\n"
        path.write_text(content, encoding="utf-8")
