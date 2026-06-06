# 验证用例文件：A.9 逻辑运算符

RUN_CASES = [
    {
        "name": "成年有票",
        "args": (12, True),
        "expected_return": True,
    },
    {
        "name": "儿童有票",
        "args": (10, True),
        "expected_return": False,
    },
    {
        "name": "老人免票",
        "args": (65, False),
        "expected_return": True,
    },
    {
        "name": "成年人无票",
        "args": (30, False),
        "expected_return": False,
    },
]

SUBMIT_CASES = [
    {
        "name": "刚好12但无票",
        "args": (12, False),
        "expected_return": False,
    },
    {
        "name": "未到老人标准且无票",
        "args": (64, False),
        "expected_return": False,
    },
    {
        "name": "老人有票",
        "args": (66, True),
        "expected_return": True,
    },
    {
        "name": "幼童无票",
        "args": (5, False),
        "expected_return": False,
    },
    {
        "name": "刚好65有票",
        "args": (65, True),
        "expected_return": True,
    },
    {
        "name": "青少年有票",
        "args": (14, True),
        "expected_return": True,
    },
]
