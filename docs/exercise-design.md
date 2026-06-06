# 练习格式设计

本文档描述 `py_learn` 的 **Exercise Source（原始练习）** 格式、继承元数据规则、答题目录复制规则与验证用例接口。

## 目标

- 每个练习都能作为独立文件夹维护。
- 练习可以默认扁平存放，也可以按章节放入任意深度的文件夹。
- 练习自身可以完全自描述。
- 上层文件夹可以声明章节相关继承元数据，减少重复配置。
- 答题目录只暴露学习者需要阅读或编辑的文件。
- 验证文件保留在原始练习中，由 CLI 自动调用，不复制到答题目录。
- 所有练习统一使用 `py_learn` 函数作为答案入口。

## 目录结构

### 扁平结构

```text
content/
  A.1/
    exercise.toml
    q.md
    a.py
    cases.py
    .plignore
  A.2/
    exercise.toml
    q.md
    a.py
    cases.py
```

### 嵌套结构

```text
content/
  oop/
    exercise.toml
    class-basic/
      exercise.toml
      self-method/
        exercise.toml
        q.md
        a.py
        cases.py
        .plignore
```

CLI 递归扫描内容目录中的 `exercise.toml`，不依赖固定目录深度。

## `exercise.toml`

`exercise.toml` 必须包含 `type` 字段，用于区分当前文件夹的含义。

```toml
type = "chapter"
```

表示当前文件夹只声明章节相关的 **Inherited Exercise Metadata（继承练习元数据）**。

```toml
type = "exercise"
```

表示当前文件夹是一个真正的 **Exercise Source（原始练习）**。

## 章节继承元数据

上层文件夹可以声明章节信息：

```toml
type = "chapter"

[chapter]
id = "B"
title = "基础面向对象"
order = 2
```

更深层章节可以继续声明：

```toml
type = "chapter"

[chapter]
id = "B1"
title = "了解类(class)"
parent = "B"
order = 1
```

继承规则：

- 继承只在扫描时合并到内存模型。
- 不会把上层元数据写回下层 `exercise.toml`。
- 按字段合并。
- 下层只覆盖自己声明的字段。
- 未声明字段继续使用上层值。
- `type = "exercise"` 文件中的练习自身元数据优先级最高。

## 练习元数据

一个最小练习示例：

```toml
type = "exercise"

id = "B1.2"
title = "self 函数"
order = 2

question = "q.md"
answer = "a.py"
cases = "cases.py"
```

如果没有上层章节元数据，练习也可以完全自描述：

```toml
type = "exercise"

id = "B1.2"
title = "self 函数"
order = 2

question = "q.md"
answer = "a.py"
cases = "cases.py"

[chapter]
id = "B1"
title = "了解类(class)"
parent = "B"
order = 1
```

## 答题入口

所有练习统一使用 `py_learn` 函数作为答案入口。

```python
def py_learn(...):
    ...
```

练习可以通过两种方式验证：

- 检查 `py_learn` 的返回值。
- 捕获并检查 `py_learn` 执行期间的标准输出。

返回值示例：

```python
# 输入：两个整数 a, b
# 输出：返回两个整数之和

def py_learn(a, b):
    pass
```

输出示例：

```python
# 输入：一个名字 name
# 输出：打印“你好，{name}”

def py_learn(name):
    pass
```

第一版不支持传统 stdin/stdout 整文件判题，不要求学习者处理 `input()` 驱动的整文件执行。

## 验证用例文件

每个原始练习使用一个验证文件，同时声明调试用例和提交验证用例。

默认文件名建议为：

```text
cases.py
```

`cases.py` 示例：

```python
RUN_CASES = [
    {
        "name": "两个正整数相加",
        "args": (1, 2),
        "expected_return": 3,
    },
    {
        "name": "打印问候语",
        "args": ("小明",),
        "expected_stdout": "你好，小明\n",
    },
]

SUBMIT_CASES = [
    {
        "name": "零和正数",
        "args": (0, 5),
        "expected_return": 5,
    },
]
```

支持关键字参数：

```python
RUN_CASES = [
    {
        "name": "关键字参数",
        "args": (),
        "kwargs": {"name": "小明"},
        "expected_stdout": "你好，小明\n",
    },
]
```

比较规则：

- 声明 `expected_return` 时比较返回值。
- 声明 `expected_stdout` 时比较标准输出。
- 两者都声明时必须都通过。
- 未声明的部分不参与比较。
- 用例执行异常视为该用例失败。

CLI 负责：

- 加载答题目录中的 `a.py`。
- 获取 `py_learn`。
- 加载原始练习中的 `cases.py`。
- 调用 `py_learn(*args, **kwargs)`。
- 捕获返回值、标准输出和异常。
- 输出统一报告。
- 统计耗时。
- 使用 `tracemalloc` 近似统计峰值内存。

验证文件不会复制到答题目录。

## 复制到答题目录的文件

默认复制：

```text
q.md
a.py
```

允许复制其他学习材料，例如：

```text
assets/
README.md
data/example.txt
```

不复制：

```text
exercise.toml
cases.py
```

## `.plignore`

每个原始练习可以包含 `.plignore`，语法类似 `.gitignore`。

`.plignore` 用于描述执行 `pl save` 时不进入 **Attempt Snapshot（答题进度快照）** 的文件。

使用练习时，CLI 会把原始练习中的 `.plignore` 复制到答题目录的 `.pl/.plignore`，不会复制到答题目录根目录。

如果原始练习没有 `.plignore`，默认忽略规则为：

```gitignore
q.md
.pl/
__pycache__/
*.pyc
```

`q.md` 是默认 **Learning Material（学习材料）**，默认不保存进答题进度快照。

## 保存模型

`pl save` 使用黑名单模型：

- 保存答题目录中除 `.pl/.plignore` 匹配项外的文件。
- 永远不保存 `.pl/` 内部状态。
- 默认不保存 `q.md`。
- 会保存学习者创建的 `helper.py`、`notes.md` 等辅助文件。

## 答题目录状态

答题目录中的 `.pl/` 是本地状态目录，用于识别当前目录是否承载某个练习。

建议结构：

```text
.pl/
  state.json
  manifest.json
  .plignore
```

`state.json` 记录当前练习：

```json
{
  "exercise_id": "B1.2",
  "source_path": "..."
}
```

`manifest.json` 记录 CLI 复制到答题目录的管理文件：

```json
{
  "managed_files": [
    "q.md",
    "a.py",
    "assets/demo.txt"
  ]
}
```

切换练习时，CLI 只删除 `manifest.json` 中记录的管理文件。

不得使用通配符清空答题目录，也不得删除未被记录的用户文件。

## 内容来源

第一版同时支持：

- 随包内置内容目录。
- 用户配置的额外内容目录。

扫描时合并多个内容来源。若出现重复 Exercise ID，应报错并提示冲突来源。
