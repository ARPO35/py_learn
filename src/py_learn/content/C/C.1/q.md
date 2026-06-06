# 练习 C.1：列表去重排序

## 题目说明

编写函数 `py_learn`，接收一个整数列表 `numbers`，先去除重复元素，再将剩余元素按升序排序，返回排序后的列表。

## 示例

```python
py_learn([3, 1, 2, 3, 2, 1])    # 返回 [1, 2, 3]
py_learn([5, 4, 3, 2, 1])       # 返回 [1, 2, 3, 4, 5]
py_learn([10, 10, 10])           # 返回 [10]
```

## 提示

- 使用 `set()` 去重：`set(numbers)` 返回一个无重复元素的集合
- 使用 `sorted()` 排序：`sorted(set(numbers))` 返回排序后的列表
- 也可以用 `list(set(numbers))` 转回列表，再 `.sort()`

## 要求

- 函数签名：`def py_learn(numbers):`
- 返回值类型：`list`
