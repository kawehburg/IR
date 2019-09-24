import re
from ex1.boolop import ana


def cp(exp, source, max_len=27799):
    if not isinstance(exp, list):
        exp = reg(exp)
    i = 0
    cur = [s for s in range(max_len)]
    op = '&&'
    while i < len(exp):
        if exp[i] == '(':
            j = i + 1
            m = 0
            while m >= 0:
                if exp[j] == '(':
                    m += 1
                if exp[j] == ')':
                    m -= 1
                j += 1
            cur = ana(cur, cp(exp[i + 1:j - 1], source), op, max_len)
            i = j - 1
        if exp[i] in source:
            cur = ana(cur, source[exp[i]], op, max_len)
        else:
            op = exp[i]
        i += 1
    return cur


def reg(seq):
    seg = []
    for item in seq.split(' '):
        if item != '':
            seg.append(item)
    return seg


if __name__ == '__main__':
    print(cp('a && ( b || ( ! c ) )', {'a': [1, 2, 3], 'b': [3, 4, 5], 'c': [2, 3, 4]}))
