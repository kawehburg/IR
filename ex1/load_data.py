import re
from collections import defaultdict
import pickle

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

if __name__ == '__main__':
    text, raw_text, vocab, vocab_index, index, letter = get_data()
    print('data loaded')
    print(len(text), len(vocab))
    # 27799 53113
