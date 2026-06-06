# 验证用例文件：A.2 打印问候语

RUN_CASES = [
    {
        "name": "打印问候-小明",
        "args": ("小明",),
        "expected_stdout": "你好，小明\n",
    },
    {
        "name": "打印问候-世界",
        "args": ("世界",),
        "expected_stdout": "你好，世界\n",
    },
]

SUBMIT_CASES = [
    {
        "name": "打印问候-Python",
        "args": ("Python",),
        "expected_stdout": "你好，Python\n",
    },
    {
        "name": "打印问候-学习者",
        "args": ("学习者",),
        "expected_stdout": "你好，学习者\n",
    },
    {
        "name": "打印问候-空字符串",
        "args": ("",),
        "expected_stdout": "你好，\n",
    },
]
