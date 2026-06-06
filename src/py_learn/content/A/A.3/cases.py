# 验证用例文件：A.3 条件判断

RUN_CASES = [
    {
        "name": "优秀等级（95分）",
        "args": (95,),
        "expected_return": "优秀",
    },
    {
        "name": "良好等级（85分）",
        "args": (85,),
        "expected_return": "良好",
    },
    {
        "name": "及格等级（65分）",
        "args": (65,),
        "expected_return": "及格",
    },
    {
        "name": "不及格等级（45分）",
        "args": (45,),
        "expected_return": "不及格",
    },
    {
        "name": "边界值 90 分",
        "args": (90,),
        "expected_return": "优秀",
    },
    {
        "name": "边界值 80 分",
        "args": (80,),
        "expected_return": "良好",
    },
    {
        "name": "边界值 60 分",
        "args": (60,),
        "expected_return": "及格",
    },
]

SUBMIT_CASES = [
    {
        "name": "满分",
        "args": (100,),
        "expected_return": "优秀",
    },
    {
        "name": "零分",
        "args": (0,),
        "expected_return": "不及格",
    },
    {
        "name": "刚好不及格",
        "args": (59,),
        "expected_return": "不及格",
    },
    {
        "name": "中等分数",
        "args": (77,),
        "expected_return": "及格",
    },
    {
        "name": "高分",
        "args": (93,),
        "expected_return": "优秀",
    },
]
