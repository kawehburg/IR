from ex1.irmodel import IR
from collections import defaultdict
import numpy as np
import heapq


class Agent(IR):

    @staticmethod
    def hash(x):
        w = 1
        h = 0
        for item in x:
            h += w * item
            w *= 100
        return h

    @staticmethod
    def smart_notation(name):
        collect1 = {'n': lambda x, y: x,
                    'a': lambda x, y: 0.5 + 0.5 * x / max(y),
                    'b': lambda x, y: 1 if x > 0 else 0,
                    'L': lambda x, y: (1 + np.log(x)) / (1 + np.log(np.average(y))) if x != 0 else 0,
                    'l': lambda x, y: 1 + np.log(x) if x != 0 else 0}
        collect2 = {'t': lambda x, y: np.log(y / x) if x != 0 else 0,
                    'p': lambda x, y: max(0, np.log((y - x) / x)) if x != 0 else 0,
                    'n': lambda x, y: 1}
        collect3 = {'n': lambda x: 1,
                    'c': lambda x: 1 / sum([i ** 2 for i in x] + [0.001]) ** 0.5}

        return collect1[name[0]], collect2[name[1]], collect3[name[2]]

    def __init__(self, file):
        super().__init__(file)
        self.tf = self.build_score()
        self.smart = (self.smart_notation('lnc'), self.smart_notation('ltc'))
        self.k = 10
        self.cache = {'q': None, 'd': {}}

    def build_score(self):
        tf = []
        for i, line in enumerate(self.text):
            tf.append(defaultdict(int))
            for item in line.split(' '):
                tf[-1][item] += 1
        return tf

    def match(self, exp, report=print):
        if '.' in exp:
            smart = exp.split('.')
            try:
                self.smart = (self.smart_notation(smart[0].strip()), self.smart_notation(smart[1].strip()))
                print('SMART notation:', exp)
            except KeyError:
                print('unsolved format:', exp)
            return []
        elif '=' in exp:
            self.k = int(exp.split('=')[1])
            return []
        else:
            return super().match(exp, report=report)

    def get_regular(self, exp):
        regular = ''
        while '<' in exp:
            seg1 = exp.index('<')
            seg2 = exp.index('>')
            for item in exp[seg1 + 1:seg2]:
                if item not in self.OPERATOR:
                    regular += item + ' '
            if seg1 == 0 or seg2 != len(exp) - 1 or (exp[seg1 - 1] in self.OPERATOR and exp[seg1 - 1] != ')'):
                exp.pop(seg1)
                exp.pop(seg2 - 1)
            else:
                exp = exp[:seg1]
        regular = self.add_space(regular)
        regular = self.reg(regular)
        return exp, regular

    def init_cache(self):
        self.cache = {'q': None, 'd': {}}

    def text_score(self, x, regular, use_cache=False):
        def w(tf, num):
            df = [len(self.vocab_index[i]) for i in regular]
            tf_w = [self.smart[num][0](i, tf) for i in tf]
            df_w = [self.smart[num][1](i, N) for i in df]
            weight = [i * j for i, j in zip(tf_w, df_w)]
            norm = self.smart[num][2](weight)
            weight_n = [i * norm for i in weight]
            return weight_n
        N = len(self.text)
        d_tf = [self.tf[x][i] for i in regular]
        q_tf = [1 for _ in regular]
        if use_cache:
            if self.hash(d_tf) in self.cache['d']:
                d_weight_n = self.cache['d'][self.hash(d_tf)]
            else:
                d_weight_n = w(d_tf, 0)
                self.cache['d'][self.hash(d_tf)] = d_weight_n

            if self.cache['q'] is not None:
                q_weight_n = self.cache['q']
            else:
                q_weight_n = w(q_tf, 1)
                self.cache['q'] = q_weight_n
        else:
            d_weight_n = w(d_tf, 0)
            q_weight_n = w(q_tf, 1)
        product = [i * j for i, j in zip(d_weight_n, q_weight_n)]
        score = sum(product)
        return score

    def count(self, res, regular):
        if len(regular) == 0:
            return res
        self.init_cache()
        heap = []
        if regular != '':
            for text in res:
                heapq.heappush(heap, (self.text_score(text, regular, use_cache=True), text))
                if len(heap) > self.k:
                    heapq.heappop(heap)
        res = []
        while len(heap):
            s = heapq.heappop(heap)
            res.append(s[1])
        res.reverse()
        return res


if __name__ == '__main__':
    agent = Agent('../ex1/tweets2.txt')
    agent.agent()
