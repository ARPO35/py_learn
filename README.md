# py_learn

面向 Python 初学者的命令行学习工具。按章节组织练习，在本地环境中编码、运行测试、提交验证，所有进度本地保存。

## 安装

```bash
git clone https://github.com/ARPO35/py_learn.git
cd py_learn
uv venv
uv pip install -e .
```

验证安装：

```bash
pl --help
```

## 快速开始

```bash
# 查看所有章节
pl ls

# 查看章节内的练习
pl ls A

# 开始做题
pl new A.1

# 查看题目说明
more q.md

# 编辑答案后运行调试测试
pl run

# 通过后提交验证
pl submit

# 进入下一题
pl next
```

## 命令

| 命令 | 说明 |
|------|------|
| `pl ls [章节]` | 列出章节或练习 |
| `pl new <编号>` | 从原始练习开始 |
| `pl run` | 运行调试用例 |
| `pl submit` | 提交验证 |
| `pl save` | 保存当前进度 |
| `pl resume <编号>` | 恢复练习进度 |
| `pl next` | 跳到下一练习 |
| `pl status` | 查看学习进度 |

## 工作区结构

```
工作目录/
├── q.md        # 题目说明
├── a.py        # 你的答案
└── .pl/        # 内部状态（勿手动编辑）
```

## 编写答案

所有练习统一入口为 `py_learn` 函数：

```python
# 返回值模式
def py_learn(a, b):
    return a + b
```

```python
# 输出模式
def py_learn(name):
    print(f"你好，{name}")
```

## 系统要求

- Python >= 3.11
- 支持 Windows / Linux / macOS

## 文档

- [快速入门](QUICKSTART.md)
- [练习设计指南](docs/exercise-design.md)
- [题目编写规范](docs/q-md-writing-guide.md)
- [章节设计](docs/chapter-a-design.md)

## 许可

MIT
