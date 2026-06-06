"""验证执行与判题。"""

from __future__ import annotations
import importlib.util
import io
import sys
import time
import traceback as tb
import tracemalloc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CaseResult:
    """单个验证用例的执行结果。"""

    name: str
    passed: bool
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    expected_return: Any = None
    expected_stdout: str | None = None
    actual_return: Any = None
    actual_stdout: str = ""
    exception: str | None = None
    traceback: str = ""
    failure_reasons: list[str] = field(default_factory=list)
    elapsed: float = 0.0


@dataclass
class ValidationReport:
    """验证报告。"""

    results: list[CaseResult] = field(default_factory=list)
    total_elapsed: float = 0.0
    peak_memory_bytes: int = 0

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def total_count(self) -> int:
        return len(self.results)


def load_py_learn(workspace_path: Path) -> Any:
    """从答题目录加载 py_learn 函数。"""
    a_py = workspace_path / "a.py"
    if not a_py.exists():
        raise FileNotFoundError(f"未找到答题文件: {a_py}")

    # 用唯一模块名避免缓存冲突
    module_name = f"_pl_answer_{a_py.stat().st_mtime_ns}"
    spec = importlib.util.spec_from_file_location(module_name, str(a_py))
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {a_py}")

    module = importlib.util.module_from_spec(spec)
    old_path = sys.path[:]
    sys.path.insert(0, str(workspace_path))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = old_path

    if not hasattr(module, "py_learn"):
        raise ValueError("a.py 中未找到 py_learn 函数")
    return module.py_learn


def load_cases(cases_path: Path) -> tuple[list[dict], list[dict]]:
    """加载验证文件，返回 (RUN_CASES, SUBMIT_CASES)。"""
    if not cases_path.exists():
        raise FileNotFoundError(f"未找到验证文件: {cases_path}")

    module_name = f"_pl_cases_{cases_path.stat().st_mtime_ns}"
    spec = importlib.util.spec_from_file_location(module_name, str(cases_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载验证模块: {cases_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    run_cases = getattr(module, "RUN_CASES", [])
    submit_cases = getattr(module, "SUBMIT_CASES", [])
    return run_cases, submit_cases


def run_single_case(py_learn_func: Any, case: dict) -> CaseResult:
    """执行单个验证用例。"""
    name = case.get("name", "未命名用例")
    args = case.get("args", ())
    kwargs = case.get("kwargs", {})
    expected_return = case.get("expected_return")
    expected_stdout = case.get("expected_stdout")

    start = time.perf_counter()
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    exception = None
    actual_return = None

    traceback_str = ""
    try:
        actual_return = py_learn_func(*args, **kwargs)
    except Exception as e:
        exception = f"{type(e).__name__}: {e}"
        traceback_str = tb.format_exc()
    finally:
        sys.stdout = old_stdout
    elapsed = time.perf_counter() - start

    actual_stdout = captured.getvalue()
    passed = True
    failure_reasons: list[str] = []

    if exception:
        passed = False
        failure_reasons.append(f"异常: {exception}")

    if "expected_return" in case and actual_return != expected_return:
        passed = False
        failure_reasons.append(
            f"返回值不匹配: 期望 {expected_return!r}, 实际 {actual_return!r}"
        )

    if "expected_stdout" in case and actual_stdout != expected_stdout:
        passed = False
        failure_reasons.append(
            f"输出不匹配: 期望 {expected_stdout!r}, 实际 {actual_stdout!r}"
        )

    return CaseResult(
        name=name,
        passed=passed,
        args=args,
        kwargs=kwargs,
        expected_return=expected_return if "expected_return" in case else None,
        expected_stdout=expected_stdout if "expected_stdout" in case else None,
        actual_return=actual_return,
        actual_stdout=actual_stdout,
        exception=exception,
        traceback=traceback_str,
        failure_reasons=failure_reasons,
        elapsed=elapsed,
    )


def run_cases(py_learn_func: Any, cases: list[dict]) -> ValidationReport:
    """运行一组验证用例，返回报告。"""
    tracemalloc.start()
    total_start = time.perf_counter()

    results: list[CaseResult] = []
    for case in cases:
        results.append(run_single_case(py_learn_func, case))

    total_elapsed = time.perf_counter() - total_start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return ValidationReport(
        results=results,
        total_elapsed=total_elapsed,
        peak_memory_bytes=peak,
    )
