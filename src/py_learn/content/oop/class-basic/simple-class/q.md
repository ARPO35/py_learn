# 练习 B1.1：定义简单类

## 题目说明

编写函数 `py_learn`，接收一个名字字符串 `name` 和一个整数 `age`，定义一个 `Person` 类并创建实例，返回该实例的名字。

## 示例

```python
py_learn("小明", 18)  # 返回 "小明"
```

## 提示

- 使用 `class` 关键字定义类
- `__init__` 方法用于初始化实例属性
- 使用 `self.` 访问实例属性

## 要求

- 函数签名：`def py_learn(name, age):`
- 定义一个 `Person` 类，包含 `name` 和 `age` 属性
- 返回实例的 `name` 属性
