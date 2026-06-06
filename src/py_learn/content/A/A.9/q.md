# 练习 A.9：逻辑运算符

去电影院看电影时，检票员需要检查你是否有票、年龄是否符合规定——这些条件往往要同时判断。Python 的逻辑运算符（`and`、`or`、`not`）就是用来组合多个条件，得出一个最终的 True 或 False。

## 概念讲解

### `and` —— 并且
`A and B`：**两边都为 True，结果才是 True**。只要有一个是 False，结果就是 False。

| A | B | A and B |
|---|---|---------|
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | False |

### `or` —— 或者
`A or B`：**至少一边为 True，结果就是 True**。两边都是 False 时才是 False。

| A | B | A or B |
|---|---|--------|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | False |

### `not` —— 取反
`not A`：把 True 变成 False，False 变成 True。

| A | not A |
|---|-------|
| True | False |
| False | True |

## 代码示例

```python
# 示例 1：and 两边都要满足
age = 15
has_ticket = True
print(age >= 12 and has_ticket)   # True（年龄够且有票）

age = 10
has_ticket = True
print(age >= 12 and has_ticket)   # False（年龄不够，即使有票也不行）

# 示例 2：or 满足其一即可
score = 85
bonus = 5
print(score >= 90 or bonus >= 10) # False（两个都不满足）

score = 95
bonus = 3
print(score >= 90 or bonus >= 10) # True（分数够了）

# 示例 3：not 取反
is_raining = True
print(not is_raining)             # False
print(not (10 > 5))               # False
```

## 常见错误

**错误 1：混淆 and 和 or 的逻辑**
写条件时代入日常语言的习惯，却用了错误的运算符。例如"儿童或老人免费"中的"或"在编程里可能是 `or`，但要仔细确认到底是"任意一个满足"还是"两个都要满足"。

**错误 2：忘记运算符优先级**
`and` 的优先级高于 `or`，这可能导致意想不到的结果：
```python
# 想表达：(age >= 12 and has_ticket) or (age >= 65)
# 如果不加括号：
age >= 12 and has_ticket or age >= 65
# Python 会理解为：(age >= 12 and has_ticket) or (age >= 65)
# 这条因为 and 优先于 or，所以结果恰好一样。但更复杂的条件就可能出问题。
```
**建议**：只要组合了 and 和 or，就主动加上括号，让意图一目了然。

## 题目要求

编写函数 `py_learn(age, has_ticket)`，判断一个人是否可以进入电影院。

- **参数**：
  - `age`：年龄（int）
  - `has_ticket`：是否有票（bool）
- **返回值**：`bool`，满足以下**任一**条件即可入场：
  1. 年龄 >= 12 **并且** has_ticket 为 True
  2. 年龄 >= 65（老年人免票入场）

## 提示

- 把题目中的两个条件分别写成布尔表达式，然后用 `or` 连接
- 第一个条件包含两个子条件，需要用 `and` 连接
- 整体结构：`(条件1 and 条件2) or (条件3)`
