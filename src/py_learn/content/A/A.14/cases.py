# 验证用例文件：A.14 while 循环

RUN_CASES = [
    {
        "name": "123 各位之和",
        "args": (123,),
        "expected_return": 6,
    },
    {
        "name": "4567 各位之和",
        "args": (4567,),
        "expected_return": 22,
    },
    {
        "name": "100 各位之和",
        "args": (100,),
        "expected_return": 1,
    },
]

SUBMIT_CASES = [
    {
        "name": "n=0",
        "args": (0,),
        "expected_return": 0,
    },
    {
        "name": "n=1",
        "args": (1,),
        "expected_return": 1,
    },
    {
        "name": "五个9",
        "args": (99999,),
        "expected_return": 45,
    },
    {
        "name": "大数1到9",
        "args": (123456789,),
        "expected_return": 45,
    },
    {
        "name": "两位数",
        "args": (78,),
        "expected_return": 15,
    },
]
