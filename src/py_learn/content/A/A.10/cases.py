# 验证用例文件：A.10 列表入门

RUN_CASES = [
    {
        "name": "三个元素",
        "args": ([1, 2, 3],),
        "expected_return": "第一个：1，最后一个：3，共3个",
    },
    {
        "name": "单个元素",
        "args": ([100],),
        "expected_return": "第一个：100，最后一个：100，共1个",
    },
    {
        "name": "四个元素",
        "args": ([5, 10, 15, 20],),
        "expected_return": "第一个：5，最后一个：20，共4个",
    },
]

SUBMIT_CASES = [
    {
        "name": "空列表",
        "args": ([],),
        "expected_return": "列表为空",
    },
    {
        "name": "负数列表",
        "args": ([-5, -3, -1],),
        "expected_return": "第一个：-5，最后一个：-1，共3个",
    },
    {
        "name": "大列表",
        "args": ([10, 20, 30, 40, 50],),
        "expected_return": "第一个：10，最后一个：50，共5个",
    },
    {
        "name": "零值列表",
        "args": ([0, 0, 0],),
        "expected_return": "第一个：0，最后一个：0，共3个",
    },
    {
        "name": "两个元素",
        "args": ([7, 14],),
        "expected_return": "第一个：7，最后一个：14，共2个",
    },
]
