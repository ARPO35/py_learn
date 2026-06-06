# 验证用例文件：A.5 类型转换


RUN_CASES = [
    {
        "name": "普通正整数",
        "args": ("42",),
        "kwargs": {},
        "expected_return": "结果：52",
    },
    {
        "name": "零",
        "args": ("0",),
        "kwargs": {},
        "expected_return": "结果：10",
    },
    {
        "name": "整百数",
        "args": ("100",),
        "kwargs": {},
        "expected_return": "结果：110",
    },
]

SUBMIT_CASES = [
    {
        "name": "负数",
        "args": ("-5",),
        "kwargs": {},
        "expected_return": "结果：5",
    },
    {
        "name": "大数",
        "args": ("999990",),
        "kwargs": {},
        "expected_return": "结果：1000000",
    },
    {
        "name": "前置零",
        "args": ("007",),
        "kwargs": {},
        "expected_return": "结果：17",
    },
    {
        "name": "一位数",
        "args": ("1",),
        "kwargs": {},
        "expected_return": "结果：11",
    },
    {
        "name": "接近边界的大数",
        "args": ("999999990",),
        "kwargs": {},
        "expected_return": "结果：1000000000",
    },
]
