# 练习 B1.2：self 函数

## 题目说明

编写函数 `py_learn`，接收一个整数 `n`，定义一个 `Counter` 类，包含一个 `increment` 方法和一个 `get_value` 方法。创建实例后调用 `increment` `n` 次，返回当前计数值。

## 示例

```python
py_learn(3)  # 返回 3
py_learn(0)  # 返回 0
```

## 提示

- 在类方法中使用 `self` 访问实例属性
- `self.value = 0` 在 `__init__` 中初始化计数器
- `self.value += 1` 在 `increment` 中递增

## 要求

- 函数签名：`def py_learn(n):`
- 定义 `Counter` 类，包含 `value` 属性
- 包含 `increment()` 方法（每次 +1）
- 包含 `get_value()` 方法（返回当前值）
- 返回调用 `n` 次 `increment` 后的值
