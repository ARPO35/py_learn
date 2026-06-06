# 验证用例文件：A.6 布尔值与比较

RUN_CASES = [
    {
        "name": "20岁——成年人",
        "args": (20,),
        "expected_return": True,
    },
    {
        "name": "15岁——未成年人",
        "args": (15,),
        "expected_return": False,
    },
    {
        "name": "18岁——刚好成年（边界）",
        "args": (18,),
        "expected_return": True,
    },
]

SUBMIT_CASES = [
    {
        "name": "0岁——婴儿",
        "args": (0,),
        "expected_return": False,
    },
    {
        "name": "100岁——老年人",
        "args": (100,),
        "expected_return": True,
    },
    {
        "name": "-1岁——无效年龄（负数边界）",
        "args": (-1,),
        "expected_return": False,
    },
    {
        "name": "17岁——差一岁成年",
        "args": (17,),
        "expected_return": False,
    },
]
