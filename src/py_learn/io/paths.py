"""路径管理。"""

from pathlib import Path
import os
import sys


def get_builtin_content_dir() -> Path:
    """获取内置内容目录。"""
    return Path(__file__).resolve().parent.parent / "content"


def get_snapshot_store_dir() -> Path:
    """获取快照存储目录。"""
    if sys.platform == "win32":
        base = os.environ.get(
            "LOCALAPPDATA", str(Path.home() / "AppData" / "Local")
        )
    else:
        base = os.environ.get(
            "XDG_DATA_HOME", str(Path.home() / ".local" / "share")
        )
    return Path(base) / "py_learn" / "snapshots"


def get_config_dir() -> Path:
    """获取配置目录。"""
    if sys.platform == "win32":
        base = os.environ.get(
            "LOCALAPPDATA", str(Path.home() / "AppData" / "Local")
        )
    else:
        base = os.environ.get(
            "XDG_CONFIG_HOME", str(Path.home() / ".config")
        )
    return Path(base) / "py_learn"


def get_extra_content_dirs() -> list[Path]:
    """获取用户配置的额外内容目录。"""
    config_path = get_config_dir() / "config.toml"
    extra: list[Path] = []
    if config_path.exists():
        import tomllib
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
        for d in data.get("content_dirs", []):
            p = Path(d).expanduser().resolve()
            if p.exists():
                extra.append(p)
    return extra
