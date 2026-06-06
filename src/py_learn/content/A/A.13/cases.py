# 验证用例文件：A.13 for 循环与 range

RUN_CASES = [
    {
        "name": "5 的累加和",
        "args": (5,),
        "expected_return": 15,
    },
    {
        "name": "10 的累加和",
        "args": (10,),
        "expected_return": 55,
    },
    {
        "name": "100 的累加和（高斯求和）",
        "args": (100,),
        "expected_return": 5050,
    },
]

SUBMIT_CASES = [
    {
        "name": "边界：n=1",
        "args": (1,),
        "expected_return": 1,
    },
    {
        "name": "边界：n=0",
        "args": (0,),
        "expected_return": 0,
    },
    {
        "name": "较大值：n=1000",
        "args": (1000,),
        "expected_return": 500500,
    },
    {
        "name": "简单值：n=3",
        "args": (3,),
        "expected_return": 6,
    },
    {
        "name": "简单值：n=6",
        "args": (6,),
        "expected_return": 21,
    },
]
