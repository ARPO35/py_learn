"""pl submit：提交验证。"""

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
    """处理 submit 命令。"""
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
        _, submit_cases = load_cases(cases_path)
    except Exception as e:
        print(f"加载验证文件失败: {e}")
        return

    if not submit_cases:
        print("该练习没有提交验证用例（SUBMIT_CASES）。")
        return

    console = Console()
    console.print(f"提交验证: {current_id} - {exercise.title}\n")

    report = run_cases(py_learn_func, submit_cases)
    render_validation_report(console, report, "提交")

    if report.all_passed:
        console.print("\n[bold green]全部通过！自动保存进度...[/]")
        wm.save(workspace_path)
    else:
        console.print("\n[bold yellow]部分用例未通过，请修改后重试。[/]")