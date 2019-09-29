import re
from collections import defaultdict

__all__ = ['IR']


class IR:

    @staticmethod
    def _and(seq1, seq2):
        flag1 = 0
        flag2 = 0
        seq = []
        while flag1 < len(seq1) and flag2 < len(seq2):
            if seq1[flag1] == seq2[flag2]:
                seq.append(seq1[flag1])
                flag1 += 1
                flag2 += 1
            elif seq1[flag1] < seq2[flag2]:
                flag1 += 1
            else:
                flag2 += 1
        return seq

    @staticmethod
    def _or(seq1, seq2):
        flag1 = 0
        flag2 = 0
        seq = []
        while flag1 < len(seq1) and flag2 < len(seq2):
            if seq1[flag1] == seq2[flag2]:
                flag1 += 1
            elif seq1[flag1] < seq2[flag2]:
                seq.append(seq1[flag1])
                flag1 += 1
            else:
                seq.append(seq2[flag2])
                flag2 += 1
        if flag1 == len(seq1):
            seq += seq2[flag2:]
        else:
            seq += seq1[flag1:]
        return seq

    @staticmethod
    def _not(seq1, max_len):
        seq = []
        seq1.append(max_len + 1)
        flag = 0
        for i in range(max_len):
            if seq1[flag] == i:
                flag += 1
                continue
            seq.append(i)
        return seq

    @staticmethod
    def _xor(seq1, seq2):
        flag1 = 0
        flag2 = 0
        seq = []
        while flag1 < len(seq1) and flag2 < len(seq2):
            if seq1[flag1] == seq2[flag2]:
                flag1 += 1
                flag2 += 1
            elif seq1[flag1] < seq2[flag2]:
                seq.append(seq1[flag1])
                flag1 += 1
            else:
                seq.append(seq2[flag2])
                flag2 += 1
        if flag1 == len(seq1):
            seq += seq2[flag2:]
        else:
            seq += seq1[flag1:]
        return seq

    @staticmethod
    def get_data(file='tweets2.txt'):
        text = []
        set_text = set()
        raw_text = []
        letter0 = defaultdict(set)
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                ss = re.sub(' +', ' ', re.sub('[^a-zA-Z]', ' ', line.split('"')[9])).lower().strip()
                if len(ss) < 1:
                    pass
                if ss in set_text:
                    pass
                set_text.add(ss)
                text.append(ss)
                raw_text.append(line.split('"')[9])
                for item in ss:
                    letter0[item].add(i)

        letter = {}
        for key in letter0:
            letter[key] = sorted(list(letter0[key]))
        vocab = set()
        vocab_index = defaultdict(set)

        for i, line in enumerate(text):
            for item in line.split(' '):
                if i not in vocab_index[item]:
                    vocab_index[item].add(i)
                if item not in vocab:
                    vocab.add(item)
        vocab = list(vocab)
        for key in vocab_index:
            vocab_index[key] = sorted(list(vocab_index[key]))
        index0 = [[set() for _ in range(27)] for _ in range(27)]

        for i, item in enumerate(vocab):
            s = '{' + item + '{'
            for sp in range(len(s) - 1):
                if i not in index0[ord(s[sp]) - 97][ord(s[sp + 1]) - 97]:
                    index0[ord(s[sp]) - 97][ord(s[sp + 1]) - 97].add(i)
        index = [[[] for _ in range(27)] for _ in range(27)]
        for i in range(27):
            for j in range(27):
                index[i][j] = sorted(list(index0[i][j]))
        return text, raw_text, vocab, vocab_index, index, letter

    @staticmethod
    def reg(seq):
        seg = []
        for item in seq.split(' '):
            if item != '':
                seg.append(item)
        return seg

    def __init__(self, file):
        self.text, self.raw_text, self.vocab, self.vocab_index, self.index, self.letter = self.get_data(file=file)
        self.OPERATOR = {'(', ')', '&&', '||', '!', '^', '<', '>'}
        self.RANK = {'&&': 1, '||': 2, '!': 0, '^': 1, '_': -1}

    def cp(self, exp, source, max_len=27799):
        if not isinstance(exp, list):
            exp = self.reg(exp)
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
                cur = self.ana(cur, self.cp(exp[i + 1:j - 1], source), op, max_len)
                i = j - 1
            if exp[i] in source:
                cur = self.ana(cur, source[exp[i]], op, max_len)
            else:
                op = exp[i]
            i += 1
        return cur

    def ana(self, seq1, seq2, op, max_len=27799):
        if op == '&&':
            return self._and(seq1, seq2)
        if op == '||':
            return self._or(seq1, seq2)
        if op == '!':
            return self._not(seq2, max_len)
        if op == '^':
            return self._xor(seq1, seq2)
        return seq1

    def org(self, seq):
        cur = [i for i in range(len(self.vocab))]
        if len(seq) == 1:
            return self.letter.get(seq, [])
        for sp in range(len(seq) - 1):
            cur = self.ana(cur, self.index[ord(seq[sp]) - 97][ord(seq[sp + 1]) - 97], '&&')
        text_list = []
        for item in cur:
            text_list = self.ana(text_list, self.vocab_index[self.vocab[item]], '||')
        return text_list

    def optimize(self, exp):
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
                cur.append((operator, '( ' + self.optimize(exp[i + 1:j - 1]) + ')'))
                i = j - 1
            if exp[i] not in self.OPERATOR:
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
                    if exp[j] in self.OPERATOR and exp[j] != ')':
                        f = False
                cur.append((operator, '( ! ' + self.optimize(exp[i + 1:j]) + ')'))
                i = j - 1
            if exp[i] in self.OPERATOR:
                operator = exp[i]
            i += 1
        cur.sort(key=lambda x: self.RANK[x[0]])
        res = ''
        for seq in cur:
            if seq[0] == '_':
                res += seq[1] + ' '
            else:
                res += seq[0] + ' ' + seq[1] + ' '
        return res

    def add_space(self, seq):
        for item in self.OPERATOR:
            seq = seq.replace(item, ' ' + item + ' ')
        seq = seq.lower().strip()
        return seq

    def match(self, exp):
        exp = self.add_space(exp)
        exp = self.reg(exp)
        exp, regular = self.get_regular(exp)
        exp = self.optimize(exp)
        print('[optimize]', exp)
        if regular is not None and len(regular) != 0:
            print('[rank]', regular)
        exp = self.reg(exp)
        source = {}
        for item in exp:
            if item not in self.OPERATOR:
                source[item] = self.org(item)
        res = self.cp(exp, source, max_len=len(self.text))
        res = self.count(res, regular)
        return res

    def get_regular(self, exp):
        regular = None
        if '<' in exp:
            seg = exp.index('<')
            regular = exp[seg + 1]
            if seg == 0 or (exp[seg - 1] in self.OPERATOR and exp[seg - 1] != ')'):
                exp.pop(seg)
                exp.pop(seg + 1)
            else:
                exp = exp[:seg]
        return exp, regular

    def count(self, res, regular):
        if regular is not None:
            res.sort(key=lambda x: self.text[x].count(regular), reverse=True)
        return res

    def agent(self):
        signal = {'', 'quit', 'q'}
        while True:
            s = input('\n$ ')
            if s in signal:
                break
            s = self.match(s)
            print('Find out about {} results'.format(len(s)))
            for tex_id in s:
                print(' ', tex_id, self.raw_text[tex_id])
            print('Find out about {} results'.format(len(s)))

if __name__ == '__main__':
    agent = IR('tweets2.txt')
    agent.agent()
