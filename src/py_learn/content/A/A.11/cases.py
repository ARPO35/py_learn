# 验证用例文件：A.11 列表操作进阶

RUN_CASES = [
    {
        "name": "整数存在",
        "args": ([1, 2, 3], 2),
        "expected_return": True,
    },
    {
        "name": "整数不存在",
        "args": ([1, 2, 3], 5),
        "expected_return": False,
    },
    {
        "name": "字符串存在",
        "args": (["a", "b", "c"], "b"),
        "expected_return": True,
    },
]

SUBMIT_CASES = [
    {
        "name": "空列表查询",
        "args": ([], 1),
        "expected_return": False,
    },
    {
        "name": "重复元素存在",
        "args": ([3, 1, 4, 1, 5], 1),
        "expected_return": True,
    },
    {
        "name": "大数值存在",
        "args": ([1000, 2000, 3000], 2000),
        "expected_return": True,
    },
    {
        "name": "大数值不存在",
        "args": ([1000, 2000, 3000], 999),
        "expected_return": False,
    },
    {
        "name": "布尔值查找",
        "args": ([True, False, True], False),
        "expected_return": True,
    },
]
