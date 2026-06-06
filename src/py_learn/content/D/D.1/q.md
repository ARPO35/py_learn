# 练习 D.1：默认参数

## 题目说明

编写函数 `py_learn`，接收三个参数 `text`（字符串）、`n`（重复次数，默认 1）、`sep`（分隔符，默认空格 `" "`）。

函数将 `text` 重复 `n` 次，每次之间用 `sep` 分隔，返回拼接后的字符串。

## 示例

```python
py_learn("Hello")            # 返回 "Hello"（默认 n=1）
py_learn("Hi", 3)            # 返回 "Hi Hi Hi"（默认 sep=" "）
py_learn("X", 3, "-")        # 返回 "X-X-X"
py_learn("Go", sep=",")      # 返回 "Go"（默认 n=1）
```

## 提示

- 函数定义：`def py_learn(text, n=1, sep=" "):`
- 用 `sep.join([text] * n)` 实现重复拼接
- 也可以用 for 循环拼接

## 要求

- 函数签名：`def py_learn(text, n=1, sep=" "):`
- `n` 默认值为 1
- `sep` 默认值为 `" "`（一个空格）
- 返回值类型：`str`
