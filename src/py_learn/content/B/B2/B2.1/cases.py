# 验证用例文件：B2.1 简单继承

RUN_CASES = [
    {
        "name": "创建旺财",
        "args": ("旺财", 3),
        "expected_return": "汪汪",
    },
    {
        "name": "创建小黑",
        "args": ("小黑", 5),
        "expected_return": "汪汪",
    },
    {
        "name": "不同名字和年龄",
        "args": ("大黄", 1),
        "expected_return": "汪汪",
    },
]

SUBMIT_CASES = [
    {
        "name": "英文名 Doggy",
        "args": ("Doggy", 2),
        "expected_return": "汪汪",
    },
    {
        "name": "大狗",
        "args": ("Max", 10),
        "expected_return": "汪汪",
    },
    {
        "name": "小狗",
        "args": ("Lucky", 1),
        "expected_return": "汪汪",
    },
]
