# 验证用例文件：C.1 列表去重排序

RUN_CASES = [
    {
        "name": "包含重复元素",
        "args": ([3, 1, 2, 3, 2, 1],),
        "expected_return": [1, 2, 3],
    },
    {
        "name": "全部不同",
        "args": ([5, 4, 3, 2, 1],),
        "expected_return": [1, 2, 3, 4, 5],
    },
    {
        "name": "全部重复",
        "args": ([10, 10, 10],),
        "expected_return": [10],
    },
    {
        "name": "空列表",
        "args": ([],),
        "expected_return": [],
    },
    {
        "name": "单个元素",
        "args": ([99],),
        "expected_return": [99],
    },
]

SUBMIT_CASES = [
    {
        "name": "包含负数",
        "args": ([-3, 1, -3, 5, 1],),
        "expected_return": [-3, 1, 5],
    },
    {
        "name": "乱序带重复",
        "args": ([7, 2, 1, 7, 2, 8],),
        "expected_return": [1, 2, 7, 8],
    },
    {
        "name": "零值重复",
        "args": ([0, 0, 0, 1, 2],),
        "expected_return": [0, 1, 2],
    },
    {
        "name": "已排序有重复",
        "args": ([1, 1, 2, 2, 3, 3],),
        "expected_return": [1, 2, 3],
    },
]
