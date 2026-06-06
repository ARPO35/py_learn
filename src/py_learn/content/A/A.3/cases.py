# 验证用例文件：A.3 数字运算

RUN_CASES = [
    {
        "name": "冰点",
        "args": (0,),
        "expected_return": 32.0,
    },
    {
        "name": "沸点",
        "args": (100,),
        "expected_return": 212.0,
    },
    {
        "name": "人体体温",
        "args": (37,),
        "expected_return": 98.6,
    },
]

SUBMIT_CASES = [
    {
        "name": "摄氏度零下温度，华氏度也是零下",
        "args": (-40,),
        "expected_return": -40.0,
    },
    {
        "name": "小数输入",
        "args": (36.5,),
        "expected_return": 97.7,
    },
    {
        "name": "绝对零度",
        "args": (-273.15,),
        "expected_return": -459.67,
    },
    {
        "name": "整数 1 度",
        "args": (1,),
        "expected_return": 33.8,
    },
    {
        "name": "整数 200 度",
        "args": (200,),
        "expected_return": 392.0,
    },
]
