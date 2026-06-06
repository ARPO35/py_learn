# 练习 B2.2：多态与面积计算

## 题目说明

编写函数 `py_learn`，接收两个参数：`shape_type`（字符串，`"rectangle"` 或 `"circle"`）和 `dimensions`（包含尺寸的列表）。

1. 定义一个 `Shape` 基类，包含 `area()` 方法（返回 0）
2. 定义 `Rectangle` 类，继承自 `Shape`，接收 `width` 和 `height`，重写 `area()` 返回面积
3. 定义 `Circle` 类，继承自 `Shape`，接收 `radius`，重写 `area()` 返回面积（使用 3.14 作为圆周率）
4. `py_learn` 根据 `shape_type` 创建对应实例并返回面积

## 示例

```python
py_learn("rectangle", [3, 4])   # 返回 12
py_learn("circle", [5])         # 返回 78.5
```

## 提示

- 圆的面积 = 3.14 × 半径 × 半径
- 矩形的面积 = 宽 × 高
- 使用 `isinstance()` 或 `if/elif` 判断形状类型

## 要求

- 函数签名：`def py_learn(shape_type, dimensions):`
- 必须使用继承和多态（父类定义接口，子类实现具体逻辑）
- 圆的面积用 3.14 作为 π
- 返回值类型：`float`
