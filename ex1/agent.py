import ex1.load_data as data
import ex1.op_compile as op
from ex1.boolop import _and, _or

OPERATOR = {'(', ')', '&&', '||', '!', '^', '<', '>'}
RANK = {'&&': 1, '||': 2, '!': 0, '^': 1, '_': -1}


def org(seq):
    cur = [i for i in range(len(vocab))]
    if len(seq) == 1:
        return letter.get(seq, [])
    for sp in range(len(seq) - 1):
        cur = _and(cur, index[ord(seq[sp]) - 97][ord(seq[sp + 1]) - 97])
    text_list = []
    for item in cur:
        text_list = _or(text_list, vocab_index[vocab[item]])
    return text_list


def optimize(exp):
    i = 0
    cur = []
    operator = '_'
    while i < len(exp):
        if exp[i] == '(':
            j = i + 1
            m = 0
            while m >= 0:
                if exp[j] == '(':
                    m += 1
                if exp[j] == ')':
                    m -= 1
                if j == len(exp):
                    break
                j += 1
            cur.append((operator, '( ' + optimize(exp[i + 1:j - 1]) + ')'))
            i = j - 1
        if exp[i] not in OPERATOR:
            cur.append((operator, exp[i]))
        if exp[i] == '!':
            j = i
            m = 0
            f = True
            while m > 0 or f:
                j += 1
                f = True
                if j == len(exp):
                    break
                if exp[j] == '(':
                    m += 1
                if exp[j] == ')':
                    m -= 1
                if exp[j] in OPERATOR and exp[j] != ')':
                    f = False
            cur.append((operator, '( ! ' + optimize(exp[i + 1:j]) + ')'))
            i = j - 1
        if exp[i] in OPERATOR:
            operator = exp[i]
        i += 1
    cur.sort(key=lambda x: RANK[x[0]])
    res = ''
    for seq in cur:
        if seq[0] == '_':
            res += seq[1] + ' '
        else:
            res += seq[0] + ' ' + seq[1] + ' '
    return res

def add_space(seq):
    for item in OPERATOR:
        seq = seq.replace(item, ' '+item+' ')
    seq = seq.lower().strip()
    return seq

def match(exp):
    regular = None
    exp = add_space(exp)
    exp = op.reg(exp)
    if '<' in exp:
        seg = exp.index('<')
        regular = exp[seg + 1]
        if seg == 0 or exp[seg - 1] in OPERATOR:
            exp.pop(seg)
            exp.pop(seg + 1)
        else:
            exp = exp[:seg]
    exp = optimize(exp)
    print('[optimize]', exp)
    exp = op.reg(exp)
    source = {}
    for item in exp:
        if item not in OPERATOR:
            source[item] = org(item)
    res = op.cp(exp, source, max_len=len(text))
    if regular is not None:
        res.sort(key=lambda x: text[x].count(regular), reverse=True)
    return res


if __name__ == '__main__':
    text, raw_text, vocab, vocab_index, index, letter = data.get_data(file='tweets2.txt')

    m1 = 'ron && weasley && birthday'
    m0 = 'is{||((!ab ||askm) && < lm>) &&(s{ab && cc)'
    while True:
        s = input('\n$ ')
        if s == '':
            break
        s = match(s)
        print('Find out about {} results'.format(len(s)))
        for tex_id in s:
            print(' ', tex_id, raw_text[tex_id])
        print('Find out about {} results'.format(len(s)))
