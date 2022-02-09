def check_brackets(s: str):
    """检查括号匹配"""
    stack = list()
    bracket_map = {
        '[': ']',
        '{': '}',
        '(': ')',
    }
    bracket_types = list(bracket_map.keys()) + list(bracket_map.values())
    for i in s:
        if i not in bracket_types:
            continue
        if not stack:
            stack.append(i)
            continue
        b = stack.pop()
        if b not in bracket_map or bracket_map[b] != i:
            stack.append(b)
            stack.append(i)
    if stack:
        print(stack)
        return False
    else:
        return True


def calculate_math(math_exp: str):
    """计算数学表达式"""
    key_char = ['*', '/', '+', '-']
    print(key_char)


if __name__ == '__main__':
    # 测试括号匹配
    test_1 = '{][124]fa}'
    print(check_brackets(test_1))
