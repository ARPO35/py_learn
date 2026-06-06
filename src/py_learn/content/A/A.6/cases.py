# 验证用例文件：A.6 字符串回文判断

RUN_CASES = [
    {
        "name": "回文字符串 level",
        "args": ("level",),
        "expected_return": True,
    },
    {
        "name": "非回文字符串 python",
        "args": ("python",),
        "expected_return": False,
    },
    {
        "name": "大小写混合 Racecar",
        "args": ("Racecar",),
        "expected_return": True,
    },
    {
        "name": "单字符",
        "args": ("a",),
        "expected_return": True,
    },
    {
        "name": "空字符串",
        "args": ("",),
        "expected_return": True,
    },
]

SUBMIT_CASES = [
    {
        "name": "回文 abba",
        "args": ("abba",),
        "expected_return": True,
    },
    {
        "name": "大小写 Madam",
        "args": ("Madam",),
        "expected_return": True,
    },
    {
        "name": "非回文 hello",
        "args": ("hello",),
        "expected_return": False,
    },
    {
        "name": "回文 rotator",
        "args": ("rotator",),
        "expected_return": True,
    },
    {
        "name": "非回文 abcdef",
        "args": ("abcdef",),
        "expected_return": False,
    },
]
