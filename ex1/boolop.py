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


if __name__ == '__main__':
    print(_and([1, 3, 4], [3, 4, 5, 6, 7, 8]))
    print(_or([1, 3, 4, 8], [3, 4, 5, 6, 7, 8]))
    print(_not([1, 3, 4, 8], 10))
    print(_xor([1, 3, 4, 8], [3, 4, 5, 6, 7, 8]))
