# 验证用例文件：B1.2 self 函数

RUN_CASES = [
    {
        "name": "计数 3 次",
        "args": (3,),
        "expected_return": 3,
    },
    {
        "name": "计数 0 次",
        "args": (0,),
        "expected_return": 0,
    },
    {
        "name": "计数 10 次",
        "args": (10,),
        "expected_return": 10,
    },
]

SUBMIT_CASES = [
    {
        "name": "计数 5 次",
        "args": (5,),
        "expected_return": 5,
    },
    {
        "name": "计数 1 次",
        "args": (1,),
        "expected_return": 1,
    },
    {
        "name": "计数 100 次",
        "args": (100,),
        "expected_return": 100,
    },
    {
        "name": "计数 0 次",
        "args": (0,),
        "expected_return": 0,
    },
]
