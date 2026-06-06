# 验证用例文件：A.1 返回两个数之和

RUN_CASES = [
    {
        "name": "两个正整数相加",
        "args": (1, 2),
        "expected_return": 3,
    },
    {
        "name": "较大数相加",
        "args": (100, 200),
        "expected_return": 300,
    },
    {
        "name": "正数与零相加",
        "args": (5, 0),
        "expected_return": 5,
    },
]

SUBMIT_CASES = [
    {
        "name": "正整数相加",
        "args": (3, 4),
        "expected_return": 7,
    },
    {
        "name": "负数与正数相加",
        "args": (-5, 5),
        "expected_return": 0,
    },
    {
        "name": "两个负数相加",
        "args": (-3, -7),
        "expected_return": -10,
    },
    {
        "name": "零与零相加",
        "args": (0, 0),
        "expected_return": 0,
    },
    {
        "name": "大数相加",
        "args": (999999, 1),
        "expected_return": 1000000,
    },
]
