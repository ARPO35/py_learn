# 验证用例文件：A.4 for 循环求和

RUN_CASES = [
    {
        "name": "正整数求和",
        "args": ([1, 2, 3, 4, 5],),
        "expected_return": 15,
    },
    {
        "name": "两位数和",
        "args": ([10, 20, 30],),
        "expected_return": 60,
    },
    {
        "name": "包含负数",
        "args": ([-5, 5, 10],),
        "expected_return": 10,
    },
    {
        "name": "单个元素",
        "args": ([42],),
        "expected_return": 42,
    },
    {
        "name": "全零",
        "args": ([0, 0, 0],),
        "expected_return": 0,
    },
]

SUBMIT_CASES = [
    {
        "name": "空列表",
        "args": ([],),
        "expected_return": 0,
    },
    {
        "name": "全部负数",
        "args": ([-1, -2, -3],),
        "expected_return": -6,
    },
    {
        "name": "大数相加",
        "args": ([1000, 2000, 3000],),
        "expected_return": 6000,
    },
    {
        "name": "混合正负",
        "args": ([100, -50, 200, -100],),
        "expected_return": 150,
    },
    {
        "name": "较长列表",
        "args": ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],),
        "expected_return": 55,
    },
]
