# 验证用例文件：B2.2 多态与面积计算

RUN_CASES = [
    {
        "name": "矩形 3x4",
        "args": ("rectangle", [3, 4]),
        "expected_return": 12,
    },
    {
        "name": "圆形半径 5",
        "args": ("circle", [5]),
        "expected_return": 78.5,
    },
    {
        "name": "矩形 5x10",
        "args": ("rectangle", [5, 10]),
        "expected_return": 50,
    },
    {
        "name": "圆形半径 1",
        "args": ("circle", [1]),
        "expected_return": 3.14,
    },
]

SUBMIT_CASES = [
    {
        "name": "矩形 2x8",
        "args": ("rectangle", [2, 8]),
        "expected_return": 16,
    },
    {
        "name": "圆形半径 10",
        "args": ("circle", [10]),
        "expected_return": 314.0,
    },
    {
        "name": "矩形 7x7（正方形）",
        "args": ("rectangle", [7, 7]),
        "expected_return": 49,
    },
    {
        "name": "圆形半径 0",
        "args": ("circle", [0]),
        "expected_return": 0.0,
    },
]
