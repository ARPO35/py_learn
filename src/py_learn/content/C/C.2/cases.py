# 验证用例文件：C.2 字典字符计数

RUN_CASES = [
    {
        "name": "Hello 单词",
        "args": ("Hello",),
        "expected_return": {"h": 1, "e": 1, "l": 2, "o": 1},
    },
    {
        "name": "重复字母 abab",
        "args": ("abab",),
        "expected_return": {"a": 2, "b": 2},
    },
    {
        "name": "空格分隔的数字",
        "args": ("123 456",),
        "expected_return": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
    },
    {
        "name": "大小写混合",
        "args": ("AaBb",),
        "expected_return": {"a": 2, "b": 2},
    },
    {
        "name": "包含标点",
        "args": ("hi!",),
        "expected_return": {"h": 1, "i": 1},
    },
]

SUBMIT_CASES = [
    {
        "name": "空字符串",
        "args": ("",),
        "expected_return": {},
    },
    {
        "name": "全数字",
        "args": ("123321",),
        "expected_return": {"1": 2, "2": 2, "3": 2},
    },
    {
        "name": "长字符串",
        "args": ("abcabcabc",),
        "expected_return": {"a": 3, "b": 3, "c": 3},
    },
    {
        "name": "仅标点",
        "args": ("!@#$",),
        "expected_return": {},
    },
]
