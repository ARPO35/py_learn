# 练习 B2.1：简单继承

## 题目说明

编写函数 `py_learn`，接收一个字符串 `animal_name` 和一个整数 `age`。

1. 定义一个 `Animal` 基类，包含 `__init__` 方法接收 `name` 和 `age` 参数
2. 定义一个 `Dog` 类，继承自 `Animal`，添加 `bark()` 方法，返回 `"汪汪"`
3. `py_learn` 函数创建 `Dog` 实例并返回 `bark()` 的结果

## 示例

```python
py_learn("旺财", 3)  # 返回 "汪汪"
py_learn("小黑", 5)  # 返回 "汪汪"
```

## 提示

- 使用 `class Dog(Animal):` 实现继承
- `super().__init__(name, age)` 调用父类构造方法
- 在 `Dog` 类中定义 `bark(self)` 方法

## 要求

- 函数签名：`def py_learn(animal_name, age):`
- 必须定义 `Animal` 基类和 `Dog` 子类
- 返回值类型：`str`
