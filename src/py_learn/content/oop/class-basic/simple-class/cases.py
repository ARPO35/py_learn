# 验证用例文件：B1.1 定义简单类

RUN_CASES = [
    {
        "name": "创建小明实例",
        "args": ("小明", 18),
        "expected_return": "小明",
    },
    {
        "name": "创建小红实例",
        "args": ("小红", 20),
        "expected_return": "小红",
    },
]

SUBMIT_CASES = [
    {
        "name": "创建 Alice 实例",
        "args": ("Alice", 25),
        "expected_return": "Alice",
    },
    {
        "name": "创建 Bob 实例",
        "args": ("Bob", 30),
        "expected_return": "Bob",
    },
    {
        "name": "创建空名字实例",
        "args": ("", 0),
        "expected_return": "",
    },
]
