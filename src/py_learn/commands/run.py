"""pl run：运行调试用例。"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from ..domain.models import Exercise
from ..io.report_renderer import render_validation_report
from ..services.validator import load_cases, load_py_learn, run_cases
from ..services.workspace_manager import WorkspaceManager


def handle(
    args,
    wm: WorkspaceManager,
    exercises: dict[str, Exercise],
    workspace_path: Path,
) -> None:
    """处理 run 命令。"""
    current_id = wm.get_current_exercise_id(workspace_path)
    if not current_id:
        print("当前答题目录没有承载任何练习。请先使用 pl new 或 pl resume。")
        return

    exercise = exercises.get(current_id)
    if not exercise:
        print(f"内部错误：未找到练习 {current_id}")
        return

    source_path = wm.get_current_source_path(workspace_path)
    if not source_path:
        print(f"无法定位原始练习目录。请重新使用 pl new {current_id}。")
        return

    cases_path = source_path / exercise.cases_path

    try:
        py_learn_func = load_py_learn(workspace_path)
    except Exception as e:
        print(f"加载答题文件失败: {e}")
        return

    try:
        run_cases_list, _ = load_cases(cases_path)
    except Exception as e:
        print(f"加载验证文件失败: {e}")
        return

    if not run_cases_list:
        print("该练习没有调试用例（RUN_CASES）。")
        return

    console = Console()
    console.print(f"运行调试用例: {current_id} - {exercise.title}\n")

    report = run_cases(py_learn_func, run_cases_list)
    render_validation_report(console, report, "调试")