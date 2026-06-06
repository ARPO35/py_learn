# 验证用例文件：D.2 列表推导式

RUN_CASES = [
    {
        "name": "基本示例",
        "args": ([1, 2, 3, 4, 5],),
        "expected_return": [4, 16],
    },
    {
        "name": "连续偶数",
        "args": ([10, 11, 12, 13],),
        "expected_return": [100, 144],
    },
    {
        "name": "没有偶数",
        "args": ([1, 3, 5, 7],),
        "expected_return": [],
    },
    {
        "name": "全部偶数",
        "args": ([2, 4, 6, 8],),
        "expected_return": [4, 16, 36, 64],
    },
    {
        "name": "包含负数偶数",
        "args": ([-4, -3, -2, 0, 2],),
        "expected_return": [16, 4, 0, 4],
    },
]

SUBMIT_CASES = [
    {
        "name": "空列表",
        "args": ([],),
        "expected_return": [],
    },
    {
        "name": "单个偶数",
        "args": ([7],),
        "expected_return": [],
    },
    {
        "name": "单个偶数",
        "args": ([6],),
        "expected_return": [36],
    },
    {
        "name": "较大数值",
        "args": ([20, 21, 22],),
        "expected_return": [400, 484],
    },
    {
        "name": "零值",
        "args": ([0, 1, 2],),
        "expected_return": [0, 4],
    },
]
