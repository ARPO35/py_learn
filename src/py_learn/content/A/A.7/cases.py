# 验证用例文件：A.7 条件判断 if/else

RUN_CASES = [
    {
        "name": "成年人（20岁）",
        "args": (20,),
        "expected_return": "已成年，可以进入",
    },
    {
        "name": "未成年人（15岁）",
        "args": (15,),
        "expected_return": "未成年，不可进入",
    },
    {
        "name": "刚满18岁",
        "args": (18,),
        "expected_return": "已成年，可以进入",
    },
]

SUBMIT_CASES = [
    {
        "name": "新生儿（0岁）",
        "args": (0,),
        "expected_return": "未成年，不可进入",
    },
    {
        "name": "高中生（17岁）",
        "args": (17,),
        "expected_return": "未成年，不可进入",
    },
    {
        "name": "老年人（100岁）",
        "args": (100,),
        "expected_return": "已成年，可以进入",
    },
    {
        "name": "负数年龄",
        "args": (-1,),
        "expected_return": "未成年，不可进入",
    },
    {
        "name": "刚成年（18岁，再次确认）",
        "args": (18,),
        "expected_return": "已成年，可以进入",
    },
]
