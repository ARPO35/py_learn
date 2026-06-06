# 验证用例文件：D.1 默认参数

RUN_CASES = [
    {
        "name": "仅传入 text",
        "args": ("Hello",),
        "expected_return": "Hello",
    },
    {
        "name": "传入 text 和 n",
        "args": ("Hi", 3),
        "expected_return": "Hi Hi Hi",
    },
    {
        "name": "传入三个参数",
        "args": ("X", 3, "-"),
        "expected_return": "X-X-X",
    },
    {
        "name": "传入 text 和 sep",
        "kwargs": {"sep": ","},
        "args": ("Go",),
        "expected_return": "Go",
    },
]

SUBMIT_CASES = [
    {
        "name": "重复5次空格分隔",
        "args": ("abc", 5),
        "expected_return": "abc abc abc abc abc",
    },
    {
        "name": "用点分隔",
        "args": ("dot", 4, "."),
        "expected_return": "dot.dot.dot.dot",
    },
    {
        "name": "用逗号分隔两次",
        "args": ("word", 2, ","),
        "expected_return": "word,word",
    },
    {
        "name": "仅传 text（单词）",
        "args": ("Python",),
        "expected_return": "Python",
    },
]
