# 验证用例文件：A.8 多分支条件 elif

RUN_CASES = [
    {
        "name": "95分——优秀",
        "args": (95,),
        "expected_return": "优秀",
    },
    {
        "name": "85分——良好",
        "args": (85,),
        "expected_return": "良好",
    },
    {
        "name": "65分——及格",
        "args": (65,),
        "expected_return": "及格",
    },
    {
        "name": "45分——不及格",
        "args": (45,),
        "expected_return": "不及格",
    },
]

SUBMIT_CASES = [
    {
        "name": "90分边界——优秀",
        "args": (90,),
        "expected_return": "优秀",
    },
    {
        "name": "89分边界前一——良好",
        "args": (89,),
        "expected_return": "良好",
    },
    {
        "name": "80分——良好",
        "args": (80,),
        "expected_return": "良好",
    },
    {
        "name": "79分——及格",
        "args": (79,),
        "expected_return": "及格",
    },
    {
        "name": "60分边界——及格",
        "args": (60,),
        "expected_return": "及格",
    },
    {
        "name": "59分边界前一——不及格",
        "args": (59,),
        "expected_return": "不及格",
    },
]
