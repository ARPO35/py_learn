# Py Learn 项目实现总结

## 项目概述

Py Learn 是一个 Python 学习 CLI 工具，提供类似 LeetCode 的交互式练习体验，专为 Python 初学者设计。

## 已实现功能

### 核心命令

| 命令 | 功能 | 状态 |
|------|------|------|
| `pl new <id>` | 创建新练习工作区 | ✅ 完成 |
| `pl resume <id>` | 恢复练习 | ✅ 完成 |
| `pl save` | 保存进度 | ✅ 完成 |
| `pl run` | 运行测试用例 | ✅ 完成 |
| `pl submit` | 提交答案 | ✅ 完成 |
| `pl ls [chapter]` | 列出章节和练习 | ✅ 完成 |
| `pl next` | 进入下一题 | ✅ 完成 |

### 核心特性

#### 1. 练习管理系统
- **练习元数据**：通过 `exercise.toml` 定义练习信息
- **章节继承**：支持章级别配置自动继承到练习
- **练习发现**：递归扫描内容目录，自动发现练习
- **扁平或嵌套**：支持 `content/A.1/` 或 `content/基础/A.1/` 两种结构

#### 2. 工作区管理
- **自动复制**：`pl new` 自动复制练习文件到工作区
- **进度保存**：`pl save` 保存 `a.py` 到快照目录
- **进度恢复**：`pl resume` 从快照恢复练习
- **安全忽略**：使用 `.pl/.plignore` 控制保存的文件
- **清单追踪**：`manifest.json` 记录 CLI 管理的文件

#### 3. 测试框架与界面
- **双模式测试**：`RUN_CASES`（调试）和 `SUBMIT_CASES`（提交）
- **返回值验证**：支持 `expected_return` 精确匹配
- **输出验证**：支持 `expected_stdout` 捕获 `print()` 输出
- **Rich 美化报告**：每个用例独立框显，传入参数逐行列出，原始输出区展示 `print()` 输出和异常；底部汇总显示通过数、耗时、内存使用
- **自动保存**：`submit` 全部通过后自动保存

#### 4. 练习内容
提供了 4 个示例练习：
- **A.1** - 基本函数返回值
- **A.2** - 使用 `print()` 输出
- **B1.1** - 基础类定义
- **B1.2** - 类方法和 `self`

## 技术架构

### 项目结构

```
V:\Program\python\py_learn\
├── pyproject.toml                 # 项目配置
├── src/py_learn/
│   ├── __init__.py
│   ├── cli.py                     # CLI 入口
│   ├── domain/
│   │   ├── models.py              # 数据模型
│   ├── services/
│   │   ├── exercise_scanner.py    # 练习发现和元数据解析
│   │   ├── workspace_manager.py   # 工作区管理
│   │   ├── snapshot_store.py      # 快照管理
│   │   └── validator.py           # 测试运行器
│   ├── io/
│   │   ├── paths.py               # 路径管理
│   │   └── ignore.py              # 忽略文件处理
│   ├── commands/                  # CLI 命令实现
│   │   ├── new.py, resume.py, save.py
│   │   ├── run.py, submit.py
│   │   ├── ls.py, next.py
│   └── content/                   # 内置练习内容
└── tests/
    └── test_core.py               # 32 个测试用例
```

### 数据流

```
练习发现：
  content/**/exercise.toml
    ↓ (递归扫描 + 继承合并)
  Exercise 对象

pl new A.1：
  1. 读取 workdir/.pl/state.json（当前练习）
  2. 保存当前练习 → snapshot
  3. 清理 workdir（基于 manifest.json）
  4. 复制 content/A.1/ → workdir/
  5. 写入 state.json + manifest.json + .plignore

pl run：
  1. 读取 .pl/state.json → exercise_id
  2. 定位 content/*/exercise.toml
  3. 导入 a.py → py_learn()
  4. 加载 cases.py → RUN_CASES
  5. 执行测试 → 通过 Rich 渲染器输出美化报告

pl submit：
  1-5. 同 run，使用 SUBMIT_CASES
  6. 全部通过 → 自动调 save()
pl save：
  1. 读取 .plignore
  2. 扫描 workdir（排除 .pl/ 和忽略的文件）
  3. 复制文件 → snapshots/{exercise_id}/

pl resume：
  1. 保存当前练习 → snapshot（如果不同）
  2. 清理 workdir
  3. 复制 content → workdir
  4. 复制 snapshot → workdir（覆盖 a.py）
```

### 关键设计决策

1. **练习目录结构**：支持扁平 `A.1/` 或嵌套 `基础/A.1/`
2. **元数据继承**：章级 `exercise.toml` 自动被练习继承
3. **快照存储**：`%LOCALAPPDATA%\py_learn\snapshots\{exercise_id}\`
4. **工作区状态**：`.pl/` 目录包含 `state.json`、`manifest.json`、`.plignore`
5. **文件复制策略**：使用 manifest.json 追踪 CLI 管理的文件，避免误删用户文件
6. **测试框架**：直接导入 `a.py` 的 `py_learn()` 函数，支持返回值和 stdout 验证
6. **Rich 报告渲染**：`io/report_renderer.py` 负责美化输出，`run.py` / `submit.py` 共享同一渲染器；无需直接调用 `py_learn()` 文案，参数逐行列出
7. **自动保存触发**：`submit` 全部通过后自动保存，`run` 不保存
## 测试结果

### 单元测试：39/39 通过
- `TestDeepMerge` (3/3)：元数据合并算法
- `TestExerciseScanner` (5/5)：练习发现和继承
- `TestPlignore` (4/4)：忽略文件处理
- `TestSnapshotStore` (3/3)：快照保存和恢复
- `TestValidator` (8/8)：测试运行逻辑
- `TestWorkspaceManager` (7/7)：工作区管理（new、resume、save）
- `TestReportRenderer` (7/7)：Rich 报告渲染器输出格式
- `TestCLI` (2/2)：CLI 入口

### 端到端测试：全部通过
- ✅ `pl new` 正确创建工作区
- ✅ `pl run` 正确执行测试并报告
- ✅ `pl submit` 全部通过后自动保存
- ✅ `pl save` 保存进度到快照目录
- ✅ `pl resume` 从快照恢复练习
- ✅ `pl ls` 正确列出章节和练习

## 使用示例

```bash
# 安装
uv pip install -e .

# 查看所有章节
pl ls

# 查看 B1 章节的练习
pl ls B1

# 开始新练习
pl new A.1

# 运行调试测试
pl run

# 提交答案（自动保存）
pl submit

# 手动保存进度
pl save

# 恢复练习
pl resume A.1

# 进入下一题
pl next
```

## 创建新练习

1. 创建练习目录：`content/新练习/`
2. 创建 `exercise.toml`：
   ```toml
   type = "exercise"
   id = "X.1"
   title = "练习标题"
   question = "q.md"
   answer = "a.py"
   cases = "cases.py"
   ```
3. 创建 `q.md`（题目说明）
4. 创建 `a.py`（代码模板）：
   ```python
   def py_learn(a, b):
       pass
   ```
5. 创建 `cases.py`（测试用例）：
   ```python
   RUN_CASES = [
       {"args": (1, 2), "expected_return": 3}
   ]
   SUBMIT_CASES = [
       {"args": (10, 20), "expected_return": 30}
   ]
   ```

## 已知问题

- **Windows 控制台编码**：PowerShell 默认编码可能导致中文显示乱码，建议使用 Windows Terminal 或设置 UTF-8
- **内存统计精度**：使用 `tracemalloc`，仅为近似值
- **超时控制**：未实现子进程超时，恶意或死循环代码可能卡住

## 未来改进方向

1. **stdin/stdout 支持**：支持传统 `input()`/`print()` 工作流
2. **超时和沙箱**：使用子进程隔离执行，设置超时限制
3. **性能对比**：显示用户答案与参考答案的性能对比
4. **多语言支持**：支持 C++、Java 等其他语言
5. **进度统计**：显示完成进度和统计信息
6. **Web 界面**：提供浏览器界面查看和提交练习
7. **答案提示**：提交失败后显示解题提示
8. **练习生成器**：命令行工具快速创建练习模板

## 依赖
- Python >= 3.11
- [Rich](https://rich.readthedocs.io/) >= 13.0（终端美化）
- 开发依赖：pytest 9.0.3

## 安装

```bash
# 创建虚拟环境
uv venv

# 安装项目（开发模式）
uv pip install -e .

# 安装测试依赖
uv pip install pytest

# 运行测试
uv run pytest

# 使用命令
pl --help
```
