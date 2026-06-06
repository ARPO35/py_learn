# Py Learn 快速入门

## 安装

```bash
# 克隆或进入项目目录
cd py_learn

# 创建虚拟环境并安装
uv venv
uv pip install -e .

# 验证安装
pl --help
```

## 基本使用流程

### 1. 查看可用练习

```bash
# 列出所有章节
pl ls

# 查看特定章节的练习
pl ls A      # 基础语法
pl ls B1     # 了解类
```

输出示例：
```
A. 基础语法
|-- 1. 两数之和
|-- 2. 打印问候
B. 面向对象基础
|-- B1. 了解类
    |-- 1. 定义类
    |-- 2. 类方法
```

### 2. 开始练习

```bash
# 开始练习 A.1
pl new A.1

# 查看题目说明
more q.md

# 编辑答案
code a.py
```

### 3. 测试你的答案

```bash
# 运行调试测试（使用 RUN_CASES）
pl run
```

输出示例：
```
运行调试用例: A.1 - 返回两个数之和

╭─ 用例 1 [两个正整数相加] [PASS] ──╮
│ 参数 1: 1                         │
│ 参数 2: 2                         │
│                                   │
│ 耗时: 0.0000s                     │
╰───────────────────────────────────╯
程序原始输出 ─────────────────────────
(无输出)

╭─ 用例 2 [较大数相加] [PASS] ───────╮
│ 参数 1: 100                       │
│ 参数 2: 200                       │
│                                   │
│ 耗时: 0.0000s                     │
╰───────────────────────────────────╯
程序原始输出 ─────────────────────────
(无输出)

调试结果: 2/2 通过
总耗时:        0.0001s
近似峰值内存:  1.9 KB
```

### 4. 提交答案

```bash
# 提交验证（使用 SUBMIT_CASES）
pl submit
```

全部测试通过后会自动保存进度。

### 5. 继续学习

```bash
# 进入下一题
pl next

# 或者指定练习
pl new A.2
```

## 命令速查表

| 命令 | 说明 | 示例 |
|------|------|------|
| `pl ls` | 列出章节 | `pl ls` |
| `pl ls <章节>` | 列出练习 | `pl ls A` |
| `pl new <题目>` | 创建新练习 | `pl new A.1` |
| `pl run` | 运行调试测试 | `pl run` |
| `pl submit` | 提交答案 | `pl submit` |
| `pl save` | 手动保存进度 | `pl save` |
| `pl resume <题目>` | 恢复练习 | `pl resume A.1` |
| `pl next` | 进入下一题 | `pl next` |

## 工作区文件说明

当你运行 `pl new A.1` 后，工作目录会包含：

```
工作目录/
├── q.md              # 题目说明（只读）
├── a.py              # 你的答案（编辑这个文件）
└── .pl/              # 状态目录（勿手动编辑）
    ├── state.json       # 当前练习信息
    ├── manifest.json    # CLI 管理的文件列表
    └── .plignore        # 忽略规则（不保存到快照）
```

## 编写答案

### 返回值模式

```python
def py_learn(a, b):
    """返回 a + b"""
    return a + b
```


## 常见问题

### Q: 如何查看测试结果详情？

运行 `pl run` 或 `pl submit` 会以 Rich 美化界面展示每个测试用例的详细结果：
- 每个用例独立框显，标明 PASS/FAIL。
- 传入参数逐行列出（位置参数一行一个，关键字参数标注名称）。
- `程序原始输出` 区展示 `print()` 输出或异常报错。
- 底部汇总显示通过数、总耗时、近似峰值内存。


### Q: 我的进度保存在哪里？

快照保存在 `%LOCALAPPDATA%\py_learn\snapshots\`（Windows）或 `~/.local/share/py_learn/snapshots/`（Linux/Mac）。

### Q: 如何重置练习？

```bash
# 重新创建练习会覆盖工作区文件
pl new A.1
```

注意：之前的快照仍然保留，可以用 `pl resume A.1` 恢复。

### Q: 如何跳过已完成的练习？

```bash
pl next
```

会自动进入下一个未完成的练习。

### Q: 中文显示乱码？

建议使用 Windows Terminal，或者在 PowerShell 中运行：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 示例练习

### A.1 - 两数之和

**题目**：实现 `py_learn(a, b)` 返回两个数的和

**答案模板**：
```python
def py_learn(a, b):
    return a + b
```

### A.2 - 打印问候

**题目**：实现 `py_learn(name)` 打印 "你好，{name}"

**答案模板**：
```python
def py_learn(name):
    print(f"你好，{name}")
```

### B1.1 - 定义类

**题目**：定义 `Person` 类并返回实例的名字

**答案模板**：
```python
class Person:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

def py_learn(name):
    p = Person(name)
    return p.get_name()
```

## 创建自定义练习

参见 `docs/exercise-design.md` 了解详情。

基本步骤：

1. 创建练习目录：`content/我的练习/`
2. 创建 `exercise.toml`
3. 创建 `q.md`（题目）
4. 创建 `a.py`（答案模板）
5. 创建 `cases.py`（测试用例）
6. 运行 `pl new 我的练习`

## 下一步

- 查看详细文档：`docs/exercise-design.md`
- 查看实现细节：`IMPLEMENTATION_SUMMARY.md`
- 查看开发计划：`plan.md`
