"""Rich 报告渲染器。"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..services.validator import CaseResult, ValidationReport


def render_validation_report(
    console: Console, report: ValidationReport, mode: str
) -> None:
    """使用 Rich 渲染验证报告。

    参数：
        console: Rich Console 实例。
        report: 验证报告。
        mode: 模式名称，如 "调试" 或 "提交"。
    """
    for i, result in enumerate(report.results, 1):
        if i > 1:
            console.print()
        _render_case(console, result, i, mode)
    _render_summary(console, report, mode)


def _render_case(
    console: Console, result: CaseResult, index: int, mode: str
) -> None:
    """渲染单个用例。"""
    status_text = "[bold green][PASS][/]" if result.passed else "[bold red][FAIL][/]"
    panel_title = f"用例 {index} [{result.name}] {status_text}"

    content_lines: list[str] = []

    # 参数区：逐行列出传入参数
    param_lines = _format_params(result)
    if param_lines:
        content_lines.extend(param_lines)

    # 返回值区
    divider = "─" * max(20, (console.width or 80) - 4)
    content_lines.append(f"[dim]{divider}[/]")
    content_lines.append(f"[bold]返回值[/]: [cyan]{result.actual_return!r}[/]")
    content_lines.append("")

    # 判定区：失败原因
    if not result.passed:
        for reason in result.failure_reasons:
            content_lines.append(f"[red]{reason}[/]")

    elapsed_str = f"耗时: {result.elapsed:.4f}s"
    content_lines.append(f"[dim]{elapsed_str}[/]")

    panel_body = "\n".join(content_lines)
    console.print(Panel(panel_body, title=panel_title, title_align="left"))

    # 程序原始输出区
    _render_raw_output(console, result)


def _format_params(result: CaseResult) -> list[str]:
    """格式化参数为 Rich 标记行。返回空列表表示无参数。"""
    lines: list[str] = []

    for idx, arg in enumerate(result.args, 1):
        label = result.param_names[idx - 1] if idx <= len(result.param_names) else f"参数 {idx}"
        lines.append(f"[bold]{label}[/]: [cyan]{arg!r}[/]")

    for key, value in result.kwargs.items():
        lines.append(f"[bold]{key}[/]: [cyan]{value!r}[/]")

    return lines


def _render_raw_output(console: Console, result: CaseResult) -> None:
    """渲染程序原始输出区（print 输出、异常 traceback）。"""
    parts: list[str] = []

    if result.actual_stdout:
        parts.append(result.actual_stdout.rstrip("\n"))

    if result.traceback:
        if parts:
            parts.append("")
        parts.append(f"[red]{result.traceback.rstrip()}[/]")
    elif result.exception and not result.traceback:
        if parts:
            parts.append("")
        parts.append(f"[red]异常: {result.exception}[/]")

    if parts:
        console.print(
            Panel("\n".join(parts), title="程序原始输出", title_align="left", border_style="dim"),
        )
    else:
        console.print("[dim](无输出)[/]")


def _render_summary(
    console: Console, report: ValidationReport, mode: str
) -> None:
    """渲染汇总信息。"""
    summary_text = Text()
    summary_text.append(f"\n{mode}结果: ", style="bold")
    summary_text.append(
        f"{report.passed_count}/{report.total_count} 通过",
        style="bold green" if report.all_passed else "bold yellow",
    )

    memory_kb = report.peak_memory_bytes / 1024

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("总耗时:", f"{report.total_elapsed:.4f}s")
    table.add_row("近似峰值内存:", f"{memory_kb:.1f} KB")

    console.print(summary_text)
    console.print(table)
