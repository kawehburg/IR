from ex2.agent import Agent
from ex3.evaluation import evaluation as eval_func
import re
import tqdm
import os


class Eval(Agent):

    @staticmethod
    def get_id(file='tweets2.txt'):
        set_text = set()
        tweet_id = []
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                ss = re.sub(' +', ' ', re.sub('[^a-zA-Z]', ' ', line.split('"')[9])).lower().strip()
                if len(ss) < 1:
                    continue
                if ss in set_text:
                    continue
                set_text.add(ss)
                for idx, item in enumerate(line.split('"')):
                    if item == 'tweetId':
                        tweet_id.append(line.split('"')[idx + 2])
        return tweet_id

    @staticmethod
    def read_query(file):
        query = []
        with open(file, 'r') as f:
            for line in f:
                if line[:7] == '<query>':
                    query.append(' '.join(line.split(' ')[1:-1]))
        return query

    def org(self, seq):
        return self.vocab_index.get(seq, [])

    def query_org(self, q):
        for item in q:
            if not item.isalpha() and item not in self.OPERATOR:
                q = q.replace(item, ' ')
        q = ' || '.join(self.reg(q.strip()))
        return '< ' + q + ' >'

    def retrieve(self, query, smart='lnc.ltc', k=100):
        smart = smart.split('.')
        try:
            self.smart = (self.smart_notation(smart[0].strip()), self.smart_notation(smart[1].strip()))
        except KeyError:
            print('unsolved format:', smart)
        self.k = k
        m = []
        for q in query:
            s = self.match(self.query_org(q), report=lambda x, *args, **kwargs: None)
            m.append(s)
        return m


def evaluation(smart='lnc.ltc', file=None, agent=None, source=None, k=100, cache=True, output=None):
    print('[TASK]', smart, file=output)
    if file is None:
        file = 'tmp/' + smart + '.' + str(k) + '.txt'
    if os.path.exists(file) and cache:
        print('[exists file]', file, file=output)
    else:
        while os.path.exists(file):
            file = file[:-4] + 'f' + '.txt'
        print('[build file]', file, file=output)
        if not isinstance(agent, Eval):
            agent = Eval('../ex1/tweets2.txt')
        if source is None:
            source = {'q_list': agent.read_query('q.txt'),
                      'id_list': agent.get_id('../ex1/tweets2.txt')}
        q_list = source['q_list']
        id_list = source['id_list']
        r_list = agent.retrieve(q_list, smart=smart, k=k)
        index = 171
        with open(file, 'a+') as f:
            for qs, res in zip(q_list, r_list):
                lines = [id_list[mm] for mm in res]
                for item in lines:
                    f.writelines(str(index) + ' ' + item)
                    f.writelines("\n")
                index += 1
    eval_func(file=file, target='evaluation/qrels.txt', k=k, output=output)
    return {'agent': agent, 'source': source}


def batch(value, cache=True, k=100, output=None):
    tmp = {'agent': None, 'source': None}
    for form in tqdm.tqdm(value):
        tmp = evaluation(form, cache=cache, k=k, output=output, **tmp)


if __name__ == '__main__':
    # agent = Eval('../ex1/tweets2.txt')
    # agent.agent()
    collect1 = 'nabLl'
    collect2 = 'tpn'
    collect3 = 'nc'
    collect = [x + y + z for x in collect1 for y in collect2 for z in collect3]
    batch_list = [x + '.' + y for x in collect for y in collect]
    print(batch_list)
    print(len(batch_list))
    f = open(r'log.txt', 'w')
    batch(batch_list, cache=True, k=20, output=f)
    f.close()
