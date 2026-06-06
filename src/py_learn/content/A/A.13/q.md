# 练习 A.13：for 循环与 range

## 生活场景

想象你在爬楼梯，从第 1 阶走到第 n 阶，每走一阶就在计数器上加 1。**for 循环**就是帮你「自动走完每一阶」的工具，而 **range()** 则是生成每一阶编号的「楼梯」。

## 概念讲解

### range() 函数

`range()` 是 Python 内置函数，用来生成一个整数序列。它有几种常用形式：

- **range(n)**：生成 0, 1, 2, ..., n-1（从 0 开始，不包括 n）
- **range(start, stop)**：生成 start, start+1, ..., stop-1
- **range(start, stop, step)**：按步长 step 生成

### for 循环配合 range

`for` 循环可以将 `range()` 生成的每个数字依次赋给循环变量：

```python
for i in range(5):
    print(i)   # 输出 0 1 2 3 4
```

```python
for i in range(1, 6):
    print(i)   # 输出 1 2 3 4 5
```

第二个参数是「终止值」，序列到此为止但不包含它。

## 累加模式

累加是编程中最基础的模式之一——用变量保存当前总和，循环中每次把当前数字加上去：

```python
total = 0
for i in range(1, 6):
    total = total + i   # 等价于 total += i
print(total)            # 输出 15
```

逐步演算：
- i=1：total = 0 + 1 = 1
- i=2：total = 1 + 2 = 3
- i=3：total = 3 + 3 = 6
- i=4：total = 6 + 4 = 10
- i=5：total = 10 + 5 = 15

## 常见错误

1. **range(n) 从 0 开始**：`range(n)` 生成 0 到 n-1，不是 1 到 n。计算 1+2+...+n 需要用 `range(1, n+1)`。
2. **忘记累加变量初始化**：累加前一定要给变量赋初值（通常为 0），否则会报错或得到意外结果。
3. **误以为 range(1, n) 包含 n**：range 的结束值不包含在内，1 到 n 要写成 `range(1, n+1)`。

## 题目要求

编写函数 `py_learn(n)`，接收一个正整数 n，返回 1 + 2 + 3 + ... + n 的和。

- 函数签名：`def py_learn(n):`
- 参数：正整数 n
- 返回值：整数，表示从 1 到 n 的累加和

示例：
```python
py_learn(5)    # 返回 15
py_learn(100)  # 返回 5050
```

## 提示

- 初始化一个变量 `total = 0` 用于保存累加结果
- 用 `for i in range(1, n+1):` 遍历 1 到 n
- 循环体内用 `total += i` 累加
- 循环结束后返回 `total`
