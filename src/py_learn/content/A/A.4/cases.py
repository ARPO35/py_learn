# 验证用例文件：A.4 字符串操作

RUN_CASES = [
    {
        "name": "普通英文单词",
        "args": ("Python",),
        "expected_return": "首尾字母：Pn，长度：6",
    },
    {
        "name": "中文字符串",
        "args": ("你好",),
        "expected_return": "首尾字母：你好，长度：2",
    },
    {
        "name": "单字符字符串",
        "args": ("a",),
        "expected_return": "首尾字母：aa，长度：1",
    },
]

SUBMIT_CASES = [
    {
        "name": "空字符串",
        "args": ("",),
        "expected_return": "首尾字母：，长度：0",
    },
    {
        "name": "长字符串",
        "args": ("supercalifragilisticexpialidocious",),
        "expected_return": "首尾字母：ss，长度：34",
    },
    {
        "name": "数字字符串",
        "args": ("007",),
        "expected_return": "首尾字母：07，长度：3",
    },
    {
        "name": "含空格的字符串",
        "args": ("a b",),
        "expected_return": "首尾字母：ab，长度：3",
    },
    {
        "name": "相同字符重复",
        "args": ("zzz",),
        "expected_return": "首尾字母：zz，长度：3",
    },
    {
        "name": "标点符号字符串",
        "args": ("!?",),
        "expected_return": "首尾字母：!?，长度：2",
    },
]
