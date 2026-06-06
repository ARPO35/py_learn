# 练习 D.2：列表推导式

## 题目说明

编写函数 `py_learn`，接收一个整数列表 `numbers`，使用列表推导式（list comprehension）筛选出所有偶数，并将每个偶数平方后返回。

## 示例

```python
py_learn([1, 2, 3, 4, 5])      # 返回 [4, 16]
py_learn([10, 11, 12, 13])     # 返回 [100, 144]
py_learn([1, 3, 5, 7])         # 返回 []
```

## 提示

- 列表推导式语法：`[表达式 for 变量 in 列表 if 条件]`
- 判断偶数：`num % 2 == 0`
- 计算平方：`num ** 2`
- 完整写法：`[num ** 2 for num in numbers if num % 2 == 0]`

## 要求

- 函数签名：`def py_learn(numbers):`
- 必须使用列表推导式实现
- 返回值类型：`list`
