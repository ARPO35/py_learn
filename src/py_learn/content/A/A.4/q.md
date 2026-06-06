# 练习 A.4：for 循环求和

## 题目说明

编写函数 `py_learn`，接收一个整数列表 `numbers`，使用 `for` 循环计算列表中所有元素的总和并返回。

## 示例

```python
py_learn([1, 2, 3, 4, 5])    # 返回 15
py_learn([10, 20, 30])       # 返回 60
py_learn([-5, 5, 10])        # 返回 10
```

## 提示

- 使用 `for` 循环遍历列表：`for num in numbers:`
- 初始化一个变量 `total = 0`，在循环中累加
- 使用 `+=` 运算符累加：`total += num`

## 要求

- 函数签名：`def py_learn(numbers):`
- 必须使用 `for` 循环实现
- 返回值类型：`int`
