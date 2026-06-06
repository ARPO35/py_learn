# 验证用例文件：A.15 函数综合实战：质数判断

RUN_CASES = [
    {
        "name": "7 是质数",
        "args": (7,),
        "expected_return": True,
    },
    {
        "name": "9 不是质数",
        "args": (9,),
        "expected_return": False,
    },
    {
        "name": "2 是最小质数",
        "args": (2,),
        "expected_return": True,
    },
    {
        "name": "11 是质数",
        "args": (11,),
        "expected_return": True,
    },
]

SUBMIT_CASES = [
    {
        "name": "1 不是质数",
        "args": (1,),
        "expected_return": False,
    },
    {
        "name": "4 不是质数",
        "args": (4,),
        "expected_return": False,
    },
    {
        "name": "17 是质数",
        "args": (17,),
        "expected_return": True,
    },
    {
        "name": "97 是质数",
        "args": (97,),
        "expected_return": True,
    },
    {
        "name": "100 不是质数",
        "args": (100,),
        "expected_return": False,
    },
    {
        "name": "大质数 997 是质数",
        "args": (997,),
        "expected_return": True,
    },
]
