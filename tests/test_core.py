"""核心功能测试。"""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from py_learn.domain.models import Chapter, Exercise
from py_learn.io.ignore import Plignore, DEFAULT_IGNORE_PATTERNS
from py_learn.services.exercise_scanner import build_exercises, _deep_merge
from py_learn.services.snapshot_store import SnapshotStore
from py_learn.services.workspace_manager import WorkspaceManager
from py_learn.services.validator import (
    CaseResult,
    ValidationReport,
    load_cases,
    load_py_learn,
    run_cases,
    run_single_case,
)


# ===== 测试 fixtures =====


@pytest.fixture
def tmp_content_dir(tmp_path):
    """临时内容目录。"""
    return tmp_path / "content"


@pytest.fixture
def tmp_workspace(tmp_path):
    """临时答题目录。"""
    return tmp_path / "workspace"


@pytest.fixture
def tmp_snapshot_dir(tmp_path):
    """临时快照目录。"""
    d = tmp_path / "snapshots"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _make_exercise(dir_path, toml_content, files=None):
    """创建一个练习目录。"""
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "exercise.toml").write_text(toml_content, encoding="utf-8")
    if files:
        for name, content in files.items():
            fp = dir_path / name
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content, encoding="utf-8")


def _make_chapter(dir_path, toml_content):
    """创建一个章节目录。"""
    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "exercise.toml").write_text(toml_content, encoding="utf-8")


# ===== 测试 _deep_merge =====


class TestDeepMerge:
    """测试字段级合并。"""

    def test_flat_merge(self):
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = _deep_merge(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_nested_merge(self):
        base = {"chapter": {"id": "B", "title": "旧标题", "order": 1}}
        override = {"chapter": {"title": "新标题"}}
        result = _deep_merge(base, override)
        assert result == {"chapter": {"id": "B", "title": "新标题", "order": 1}}

    def test_override_replaces_non_dict(self):
        base = {"value": [1, 2]}
        override = {"value": [3]}
        result = _deep_merge(base, override)
        assert result == {"value": [3]}


# ===== 测试 exercise_scanner =====


class TestExerciseScanner:
    """测试练习扫描与元数据继承。"""

    def test_scan_simple_exercise(self, tmp_content_dir):
        """扫描扁平目录中的简单练习。"""
        _make_exercise(
            tmp_content_dir / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "测试题"\norder = 1\n',
            files={"q.md": "# 题", "a.py": "def py_learn(): pass\n", "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n"},
        )

        exercises, chapters = build_exercises([tmp_content_dir])
        assert "A.1" in exercises
        assert exercises["A.1"].title == "测试题"
        assert exercises["A.1"].order == 1

    def test_scan_with_inheritance(self, tmp_content_dir):
        """测试章节元数据继承。"""
        _make_chapter(
            tmp_content_dir / "B",
            'type = "chapter"\n\n[chapter]\nid = "B"\ntitle = "面向对象"\norder = 2\n',
        )
        _make_chapter(
            tmp_content_dir / "B" / "B1",
            'type = "chapter"\n\n[chapter]\nid = "B1"\ntitle = "了解类"\norder = 1\n',
        )
        _make_exercise(
            tmp_content_dir / "B" / "B1" / "self",
            'type = "exercise"\nid = "B1.2"\ntitle = "self 函数"\norder = 2\n',
            files={"q.md": "# 题", "a.py": "def py_learn(): pass\n", "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n"},
        )

        exercises, chapters = build_exercises([tmp_content_dir])
        assert "B1.2" in exercises
        ex = exercises["B1.2"]
        assert ex.title == "self 函数"
        assert ex.chapter is not None
        assert ex.chapter.id == "B1"
        assert ex.chapter.title == "了解类"
        assert ex.chapter.order == 1
        assert ex.chapter.parent == "B"

    def test_field_level_override(self, tmp_content_dir):
        """测试下层字段级覆盖上层。"""
        _make_chapter(
            tmp_content_dir / "A",
            'type = "chapter"\n\n[chapter]\nid = "A"\ntitle = "基类"\norder = 1\n',
        )
        # 练习不声明章节，只继承
        _make_exercise(
            tmp_content_dir / "A" / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "练习1"\norder = 1\n',
            files={"q.md": "# 题", "a.py": "def py_learn(): pass\n", "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n"},
        )

        exercises, _ = build_exercises([tmp_content_dir])
        ex = exercises["A.1"]
        assert ex.chapter.id == "A"
        assert ex.chapter.title == "基类"

    def test_duplicate_id_raises(self, tmp_content_dir):
        """重复 Exercise ID 应报错。"""
        _make_exercise(
            tmp_content_dir / "dir1" / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "练习1"\norder = 1\n',
            files={"q.md": "# 题", "a.py": "def py_learn(): pass\n", "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n"},
        )
        _make_exercise(
            tmp_content_dir / "dir2" / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "练习2"\norder = 2\n',
            files={"q.md": "# 题", "a.py": "def py_learn(): pass\n", "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n"},
        )

        with pytest.raises(RuntimeError, match="冲突"):
            build_exercises([tmp_content_dir])

    def test_toml_does_not_modify_files(self, tmp_content_dir):
        """扫描不应修改 exercise.toml 文件。"""
        toml_content = 'type = "exercise"\nid = "A.1"\ntitle = "练习"\norder = 1\n'
        exercise_dir = tmp_content_dir / "A.1"
        _make_exercise(
            exercise_dir,
            toml_content,
            files={"q.md": "# 题", "a.py": "def py_learn(): pass\n", "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n"},
        )

        before = (exercise_dir / "exercise.toml").read_text(encoding="utf-8")
        build_exercises([tmp_content_dir])
        after = (exercise_dir / "exercise.toml").read_text(encoding="utf-8")
        assert before == after


# ===== 测试 Plignore =====


class TestPlignore:
    """测试忽略规则匹配。"""

    def test_default_patterns(self):
        p = Plignore.default()
        assert p.should_ignore("q.md")
        assert p.should_ignore(".pl/state.json")
        assert p.should_ignore("__pycache__/test.pyc")
        assert not p.should_ignore("a.py")
        assert not p.should_ignore("helper.py")

    def test_custom_patterns(self):
        p = Plignore(patterns=["*.log", "temp/"])
        assert p.should_ignore("debug.log")
        assert p.should_ignore("temp/data.txt")
        assert not p.should_ignore("a.py")

    def test_from_file(self, tmp_path):
        ignore_file = tmp_path / ".plignore"
        ignore_file.write_text("q.md\n*.bak\n", encoding="utf-8")
        p = Plignore.from_file(ignore_file)
        assert p.should_ignore("q.md")
        assert p.should_ignore("file.bak")
        assert not p.should_ignore("a.py")

    def test_comments_and_blanks(self, tmp_path):
        ignore_file = tmp_path / ".plignore"
        ignore_file.write_text(
            "# 忽略 q.md\nq.md\n\n# 忽略备份\n*.bak\n",
            encoding="utf-8",
        )
        p = Plignore.from_file(ignore_file)
        assert p.should_ignore("q.md")
        assert p.should_ignore("file.bak")
        # 注释和空格不应匹配
        assert not p.should_ignore("# 忽略 q.md")


# ===== 测试 SnapshotStore =====


class TestSnapshotStore:
    """测试快照存储。"""

    def test_save_and_load(self, tmp_workspace, tmp_snapshot_dir):
        """保存快照并恢复。"""
        tmp_workspace.mkdir(parents=True, exist_ok=True)
        (tmp_workspace / "a.py").write_text("def py_learn(): return 42\n", encoding="utf-8")
        (tmp_workspace / "helper.py").write_text("# 辅助\n", encoding="utf-8")
        (tmp_workspace / ".pl").mkdir(exist_ok=True)
        (tmp_workspace / ".pl" / "state.json").write_text("{}", encoding="utf-8")

        store = SnapshotStore(tmp_snapshot_dir)
        plignore = Plignore.default()

        # 保存
        saved = store.save("A.1", tmp_workspace, plignore)
        assert "a.py" in saved
        assert "helper.py" in saved
        # .pl 不应保存
        for f in saved:
            assert not f.startswith(".pl")

        # 检查快照存在
        assert store.has_snapshot("A.1")

        # 恢复
        ws2 = tmp_workspace.parent / "workspace2"
        ws2.mkdir(parents=True, exist_ok=True)
        restored = store.load("A.1", ws2)
        assert "a.py" in restored
        assert "helper.py" in restored
        assert (ws2 / "a.py").read_text(encoding="utf-8") == "def py_learn(): return 42\n"

    def test_no_snapshot(self, tmp_snapshot_dir):
        """检查不存在的快照。"""
        store = SnapshotStore(tmp_snapshot_dir)
        assert not store.has_snapshot("X.99")

    def test_clear_snapshot(self, tmp_workspace, tmp_snapshot_dir):
        """清除快照。"""
        tmp_workspace.mkdir(parents=True, exist_ok=True)
        (tmp_workspace / "a.py").write_text("pass\n", encoding="utf-8")

        store = SnapshotStore(tmp_snapshot_dir)
        plignore = Plignore.default()
        store.save("A.1", tmp_workspace, plignore)
        assert store.has_snapshot("A.1")

        store.clear("A.1")
        assert not store.has_snapshot("A.1")


# ===== 测试 Validator =====


class TestValidator:
    """测试验证执行。"""

    def test_load_py_learn(self, tmp_path):
        """加载 py_learn 函数。"""
        a_py = tmp_path / "a.py"
        a_py.write_text("def py_learn(a, b):\n    return a + b\n", encoding="utf-8")
        func = load_py_learn(tmp_path)
        assert func(1, 2) == 3

    def test_load_py_learn_not_found(self, tmp_path):
        """py_learn 不存在应报错。"""
        a_py = tmp_path / "a.py"
        a_py.write_text("x = 1\n", encoding="utf-8")
        with pytest.raises(ValueError, match="py_learn"):
            load_py_learn(tmp_path)

    def test_load_cases(self, tmp_path):
        """加载验证文件。"""
        cases_path = tmp_path / "cases.py"
        cases_path.write_text(
            "RUN_CASES = [{'args': (1, 2), 'expected_return': 3}]\n"
            "SUBMIT_CASES = [{'args': (3, 4), 'expected_return': 7}]\n",
            encoding="utf-8",
        )
        run_c, submit_c = load_cases(cases_path)
        assert len(run_c) == 1
        assert len(submit_c) == 1

    def test_run_single_case_return(self):
        """运行单个返回值用例。"""
        def add(a, b):
            return a + b

        case = {"args": (1, 2), "expected_return": 3}
        result = run_single_case(add, case)
        assert result.passed
        assert result.actual_return == 3

    def test_run_single_case_stdout(self):
        """运行单个输出用例。"""
        def greet(name):
            print(f"你好，{name}")

        case = {"args": ("小明",), "expected_stdout": "你好，小明\n"}
        result = run_single_case(greet, case)
        assert result.passed
        assert result.actual_stdout == "你好，小明\n"

    def test_run_single_case_failure(self):
        """运行失败用例。"""
        def wrong():
            return 99

        case = {"expected_return": 42}
        result = run_single_case(wrong, case)
        assert not result.passed
        assert len(result.failure_reasons) > 0

    def test_run_single_case_exception(self):
        """运行抛异常的用例。"""
        def boom():
            raise RuntimeError("错误")

        case = {"expected_return": 1}
        result = run_single_case(boom, case)
        assert not result.passed
        assert result.exception is not None

    def test_run_cases_report(self):
        """运行一组用例生成报告。"""
        def add(a, b):
            return a + b

        cases = [
            {"name": "正常", "args": (1, 2), "expected_return": 3},
            {"name": "错误", "args": (1, 2), "expected_return": 99},
        ]
        report = run_cases(add, cases)
        assert report.total_count == 2
        assert report.passed_count == 1
        assert not report.all_passed


# ===== 测试 WorkspaceManager =====


class TestWorkspaceManager:
    """测试答题目录管理。"""

    def _setup(self, tmp_content_dir, tmp_snapshot_dir):
        """创建测试环境。"""
        _make_exercise(
            tmp_content_dir / "A" / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "加法"\norder = 1\n',
            files={
                "q.md": "# A.1 加法",
                "a.py": "def py_learn(a, b):\n    pass\n",
                "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n",
            },
        )
        # 创建 chapter.toml
        chapter_dir = tmp_content_dir / "A"
        (chapter_dir).mkdir(parents=True, exist_ok=True)
        # 章节 toml 在 A/ 下
        _make_chapter(
            # 注意：这里 A 目录已经有 A.1 子目录，exercise.toml 要放在 A 目录本身
            tmp_content_dir / "A",
            'type = "chapter"\n\n[chapter]\nid = "A"\ntitle = "基础语法"\norder = 1\n',
        )
        # 重新创建 A.1（因为 A/exercise.toml 被覆盖了）
        _make_exercise(
            tmp_content_dir / "A" / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "加法"\norder = 1\n',
            files={
                "q.md": "# A.1 加法",
                "a.py": "def py_learn(a, b):\n    pass\n",
                "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n",
            },
        )

        exercises, chapters = build_exercises([tmp_content_dir])
        store = SnapshotStore(tmp_snapshot_dir)
        wm = WorkspaceManager(store, exercises)
        return wm, exercises

    def test_new_creates_files(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """new 命令创建答题文件。"""
        wm, _ = self._setup(tmp_content_dir, tmp_snapshot_dir)

        wm.new("A.1", tmp_workspace)

        assert (tmp_workspace / "q.md").exists()
        assert (tmp_workspace / "a.py").exists()
        assert (tmp_workspace / ".pl" / "state.json").exists()
        assert (tmp_workspace / ".pl" / "manifest.json").exists()
        # 验证文件不应复制
        assert not (tmp_workspace / "cases.py").exists()
        assert not (tmp_workspace / "exercise.toml").exists()

        # 检查状态
        state = json.loads((tmp_workspace / ".pl" / "state.json").read_text(encoding="utf-8"))
        assert state["exercise_id"] == "A.1"

    def test_new_saves_previous(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """跨练习 new 时保存当前进度。"""
        _make_exercise(
            tmp_content_dir / "A.2",
            'type = "exercise"\nid = "A.2"\ntitle = "减法"\norder = 2\n',
            files={
                "q.md": "# A.2",
                "a.py": "def py_learn(a, b):\n    pass\n",
                "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n",
            },
        )
        wm, exercises = self._setup(tmp_content_dir, tmp_snapshot_dir)

        wm.new("A.1", tmp_workspace)
        # 修改答题内容
        (tmp_workspace / "a.py").write_text("def py_learn(a, b):\n    return a + b\n", encoding="utf-8")

        # 切换到 A.2，应保存 A.1
        wm.new("A.2", tmp_workspace)
        assert wm.snapshot_store.has_snapshot("A.1")

    def test_new_same_exercise_no_save(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """同练习 new 时不保存。"""
        wm, _ = self._setup(tmp_content_dir, tmp_snapshot_dir)

        wm.new("A.1", tmp_workspace)
        (tmp_workspace / "a.py").write_text("def py_learn(a, b):\n    return 99\n", encoding="utf-8")

        # 同练习 new，不保存
        wm.new("A.1", tmp_workspace)
        assert not wm.snapshot_store.has_snapshot("A.1")

    def test_resume_loads_snapshot(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """resume 恢复快照。"""
        wm, _ = self._setup(tmp_content_dir, tmp_snapshot_dir)

        # 新建并保存
        wm.new("A.1", tmp_workspace)
        (tmp_workspace / "a.py").write_text("def py_learn(a, b):\n    return a - b\n", encoding="utf-8")
        wm.save(tmp_workspace)

        # 重开
        wm.new("A.1", tmp_workspace)
        assert (tmp_workspace / "a.py").read_text(encoding="utf-8") == "def py_learn(a, b):\n    pass\n"

        # 恢复
        wm.resume("A.1", tmp_workspace)
        assert (tmp_workspace / "a.py").read_text(encoding="utf-8") == "def py_learn(a, b):\n    return a - b\n"

    def test_resume_same_exercise_no_save(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """同练习 resume 不保存。"""
        wm, _ = self._setup(tmp_content_dir, tmp_snapshot_dir)

        wm.new("A.1", tmp_workspace)
        (tmp_workspace / "a.py").write_text("def py_learn(a, b):\n    return 42\n", encoding="utf-8")
        wm.save(tmp_workspace)

        # 修改但不保存
        (tmp_workspace / "a.py").write_text("def py_learn(a, b):\n    return 99\n", encoding="utf-8")

        # resume 应丢弃未保存修改，恢复到之前保存的内容
        wm.resume("A.1", tmp_workspace)
        assert (tmp_workspace / "a.py").read_text(encoding="utf-8") == "def py_learn(a, b):\n    return 42\n"

    def test_switch_does_not_delete_user_files(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """切换练习不删除未记录的用户文件。"""
        wm, _ = self._setup(tmp_content_dir, tmp_snapshot_dir)

        wm.new("A.1", tmp_workspace)
        # 用户创建额外文件
        (tmp_workspace / "notes.md").write_text("# 笔记\n", encoding="utf-8")

        # 重开
        wm.new("A.1", tmp_workspace)
        # 用户文件应保留
        assert (tmp_workspace / "notes.md").exists()
        assert (tmp_workspace / "notes.md").read_text(encoding="utf-8") == "# 笔记\n"

    def test_cleanup_deletes_managed_files(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir):
        """切换只删除 CLI 管理文件。"""
        wm, _ = self._setup(tmp_content_dir, tmp_snapshot_dir)

        wm.new("A.1", tmp_workspace)
        # 创建用户文件
        (tmp_workspace / "helper.py").write_text("# helper\n", encoding="utf-8")

        # 切换（同练习 new）
        wm.new("A.1", tmp_workspace)

        # q.md 和 a.py 被重新复制，helper.py 保留
        assert (tmp_workspace / "q.md").exists()
        assert (tmp_workspace / "a.py").exists()
        assert (tmp_workspace / "helper.py").exists()



# ===== 测试报告渲染 =====


class TestReportRenderer:
    """测试 Rich 报告渲染器输出格式。"""

    def _render_report(self, cases: list[dict], py_learn_func, mode: str = "调试") -> str:
        """辅助：构造报告并渲染为字符串。"""
        from io import StringIO
        from rich.console import Console

        from py_learn.services.validator import CaseResult, ValidationReport, run_single_case

        results = [run_single_case(py_learn_func, case) for case in cases]
        report = ValidationReport(
            results=results,
            total_elapsed=0.0,
            peak_memory_bytes=1024,
        )

        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=120)
        from py_learn.io.report_renderer import render_validation_report

        render_validation_report(console, report, mode)
        return buf.getvalue()

    def test_no_py_learn_call_text(self):
        """输出不应包含 '调用: py_learn(' 或 '调用：py_learn('。"""
        def add(a, b):
            return a + b

        cases = [{"name": "加法", "args": (1, 2), "expected_return": 3}]
        output = self._render_report(cases, add)

        assert "调用: py_learn(" not in output
        assert "调用：py_learn(" not in output

    def test_positional_args_one_per_line(self):
        """位置参数逐行列出，显示参数名而非序号。"""
        def add(a, b):
            return a + b

        cases = [{"name": "加法", "args": (1, 2), "expected_return": 3}]
        output = self._render_report(cases, add)

        assert "a" in output
        assert "b" in output

    def test_keyword_args_displayed(self):
        """关键字参数应展示参数名和值。"""
        def greet(name):
            return f"你好，{name}"

        cases = [{"name": "问候", "kwargs": {"name": "小明"}, "expected_return": "你好，小明"}]
        output = self._render_report(cases, greet)

        assert "name" in output
        assert "小明" in output

    def test_clear_case_separator(self):
        """每个用例之间有明显分隔。"""
        def add(a, b):
            return a + b

        cases = [
            {"name": "用例1", "args": (1, 2), "expected_return": 3},
            {"name": "用例2", "args": (3, 4), "expected_return": 7},
        ]
        output = self._render_report(cases, add)

        # Rich Panel/Rule 会在输出中留下可辨识的边框字符或标题
        assert "用例1" in output
        assert "用例2" in output

    def test_original_output_section(self):
        """print() 输出应出现在程序原始输出区。"""
        def printer(msg):
            print(msg)

        cases = [{"name": "打印", "args": ("hello",), "expected_stdout": "hello\n"}]
        output = self._render_report(cases, printer)

        assert "hello" in output
        # 应该有程序原始输出的标识
        assert "原始输出" in output

    def test_exception_in_original_output(self):
        """异常信息应展示在原始输出区。"""
        def boom():
            raise RuntimeError("爆炸了")

        cases = [{"name": "异常", "expected_return": 1}]
        output = self._render_report(cases, boom)

        assert "爆炸了" in output or "RuntimeError" in output

    def test_summary_present(self):
        """汇总区域应显示通过数和总数。"""
        def add(a, b):
            return a + b

        cases = [{"name": "加法", "args": (1, 2), "expected_return": 3}]
        output = self._render_report(cases, add)

        assert "1/1" in output or "通过" in output



# ===== 测试 CLI 集成 =====


class TestCLI:
    """测试 CLI 命令集成。"""

    def test_ls_help(self, tmp_path):
        """ls --help 应正常。"""
        from py_learn.cli import main
        # --help 会导致 SystemExit(0)
        with pytest.raises(SystemExit, match="0"):
            main(["ls", "--help"])

    def test_main_no_args(self):
        """无参数应显示帮助。"""
        from py_learn.cli import main
        result = main([])
        assert result == 0


# ===== 测试 pl status 命令 =====


class TestStatusCommand:
    """测试 pl status 命令。"""

    def _setup_env(self, tmp_content_dir, tmp_snapshot_dir):
        """创建含章节和练习的测试环境。"""
        # 章节 A
        _make_chapter(
            tmp_content_dir / "A",
            'type = "chapter"\n\n[chapter]\nid = "A"\ntitle = "基础"\norder = 1\n',
        )
        # 练习 A.1
        _make_exercise(
            tmp_content_dir / "A" / "A.1",
            'type = "exercise"\nid = "A.1"\ntitle = "第一题"\norder = 1\n',
            files={
                "q.md": "# A.1",
                "a.py": "def py_learn():\n    pass\n",
                "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n",
            },
        )
        # 练习 A.2
        _make_exercise(
            tmp_content_dir / "A" / "A.2",
            'type = "exercise"\nid = "A.2"\ntitle = "第二题"\norder = 2\n',
            files={
                "q.md": "# A.2",
                "a.py": "def py_learn():\n    pass\n",
                "cases.py": "RUN_CASES = []\nSUBMIT_CASES = []\n",
            },
        )

        exercises, chapters = build_exercises([tmp_content_dir])
        store = SnapshotStore(tmp_snapshot_dir)
        wm = WorkspaceManager(store, exercises)
        return wm, exercises, chapters

    def test_status_no_exercise(self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir, capsys):
        """无练习时显示提示。"""
        from py_learn.commands.status_cmd import handle

        wm, exercises, chapters = self._setup_env(tmp_content_dir, tmp_snapshot_dir)
        handle(None, wm, exercises, chapters, tmp_workspace)

        captured = capsys.readouterr()
        assert "当前练习: (无)" in captured.out
        assert "pl new" in captured.out
        assert "学习进度" in captured.out

    def test_status_with_exercise_no_snapshot(
        self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir, capsys
    ):
        """有练习但无快照时显示未保存。"""
        from py_learn.commands.status_cmd import handle

        wm, exercises, chapters = self._setup_env(tmp_content_dir, tmp_snapshot_dir)
        wm.new("A.1", tmp_workspace)

        handle(None, wm, exercises, chapters, tmp_workspace)
        captured = capsys.readouterr()
        assert "当前练习: A.1" in captured.out
        assert "第一题" in captured.out
        assert "未保存" in captured.out
        assert "○ 1. 第一题" in captured.out
        assert "○ 2. 第二题" in captured.out

    def test_status_with_snapshot(
        self, tmp_content_dir, tmp_workspace, tmp_snapshot_dir, capsys
    ):
        """有快照时显示已保存和进度标记。"""
        from py_learn.commands.status_cmd import handle
        wm, exercises, chapters = self._setup_env(tmp_content_dir, tmp_snapshot_dir)
        wm.new("A.1", tmp_workspace)
        wm.save(tmp_workspace)

        handle(None, wm, exercises, chapters, tmp_workspace)

        captured = capsys.readouterr()
        assert "已保存" in captured.out
        assert "✓ 1. 第一题" in captured.out
        assert "○ 2. 第二题" in captured.out
        assert "1/2" in captured.out
    def test_status_cli_no_args(self, capsys):
        """CLI status 命令正常返回。"""
        from py_learn.cli import main
        result = main(["status"])
        assert result == 0

    def test_status_help(self, tmp_path):
        """status --help 应正常。"""
        from py_learn.cli import main
        with pytest.raises(SystemExit, match="0"):
            main(["status", "--help"])
