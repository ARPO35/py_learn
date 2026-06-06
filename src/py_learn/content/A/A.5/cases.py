# 验证用例文件：A.5 while 循环求阶乘

RUN_CASES = [
    {
        "name": "5 的阶乘",
        "args": (5,),
        "expected_return": 120,
    },
    {
        "name": "3 的阶乘",
        "args": (3,),
        "expected_return": 6,
    },
    {
        "name": "0 的阶乘",
        "args": (0,),
        "expected_return": 1,
    },
    {
        "name": "1 的阶乘",
        "args": (1,),
        "expected_return": 1,
    },
]

SUBMIT_CASES = [
    {
        "name": "6 的阶乘",
        "args": (6,),
        "expected_return": 720,
    },
    {
        "name": "2 的阶乘",
        "args": (2,),
        "expected_return": 2,
    },
    {
        "name": "4 的阶乘",
        "args": (4,),
        "expected_return": 24,
    },
    {
        "name": "8 的阶乘",
        "args": (8,),
        "expected_return": 40320,
    },
    {
        "name": "10 的阶乘",
        "args": (10,),
        "expected_return": 3628800,
    },
]
