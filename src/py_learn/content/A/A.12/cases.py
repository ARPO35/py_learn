# 验证用例文件：A.12 for 循环入门

RUN_CASES = [
    {
        "name": "1 到 5 求和",
        "args": ([1, 2, 3, 4, 5],),
        "expected_return": 15,
    },
    {
        "name": "整十数求和",
        "args": ([10, 20, 30],),
        "expected_return": 60,
    },
    {
        "name": "单个元素",
        "args": ([100],),
        "expected_return": 100,
    },
]

SUBMIT_CASES = [
    {
        "name": "空列表",
        "args": ([],),
        "expected_return": 0,
    },
    {
        "name": "负数列表",
        "args": ([-5, -3, -2],),
        "expected_return": -10,
    },
    {
        "name": "100 个 1",
        "args": ([1] * 100,),
        "expected_return": 100,
    },
    {
        "name": "包含 0 的列表",
        "args": ([0, 0, 0, 5],),
        "expected_return": 5,
    },
    {
        "name": "正负抵消",
        "args": ([10, -10, 20, -20],),
        "expected_return": 0,
    },
]
