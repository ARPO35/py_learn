# 验证用例文件：A.2 认识变量

RUN_CASES = [
    {
        "name": "中文名",
        "args": ("小明",),
        "expected_return": "你好，小明！欢迎学习 Python。",
    },
    {
        "name": "英文名",
        "args": ("Alice",),
        "expected_return": "你好，Alice！欢迎学习 Python。",
    },
    {
        "name": "单字名",
        "args": ("张",),
        "expected_return": "你好，张！欢迎学习 Python。",
    },
]

SUBMIT_CASES = [
    {
        "name": "空字符串",
        "args": ("",),
        "expected_return": "你好，！欢迎学习 Python。",
    },
    {
        "name": "带空格的名字",
        "args": ("李 明",),
        "expected_return": "你好，李 明！欢迎学习 Python。",
    },
    {
        "name": "长名字",
        "args": ("亚历山大·冯·洪堡",),
        "expected_return": "你好，亚历山大·冯·洪堡！欢迎学习 Python。",
    },
    {
        "name": "英文全名",
        "args": ("John Doe",),
        "expected_return": "你好，John Doe！欢迎学习 Python。",
    },
    {
        "name": "特殊字符",
        "args": ("O'Brien",),
        "expected_return": "你好，O'Brien！欢迎学习 Python。",
    },
]
