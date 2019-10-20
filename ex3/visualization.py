import matplotlib.pyplot as plt
import numpy as np


collect1 = 'nabLl'
collect2 = 'tpn'
collect3 = 'nc'
collect = [x + y + z for x in collect1 for y in collect2 for z in collect3]
for item in collect:
    print(item, end=' ')
print()
idx = {name: i for i, name in enumerate(collect)}
data_map = np.zeros((30, 30))
data_ndcg = np.zeros((30, 30))
data_mrr = np.zeros((30, 30))
batch_list = [x + '.' + y for x in collect for y in collect]

with open('log.txt', 'r', errors='ignore') as f:
    m = iter(f)
    for _ in range(900):
        x = next(m).strip()[7:].split('.')
        _ = next(m)
        data_map[idx[x[0]]][idx[x[1]]] = float(next(m).strip().split(' ')[-1])
        data_ndcg[idx[x[0]]][idx[x[1]]] = float(next(m).strip().split(' ')[-1])
        data_mrr[idx[x[0]]][idx[x[1]]] = float(next(m).strip().split(' ')[-1])

plt.imshow(data_map)
plt.axis('off')
plt.show()
plt.imshow(data_ndcg)
plt.axis('off')
plt.show()
plt.imshow(data_mrr)
plt.axis('off')
plt.show()

plt.figure()
plt.subplot(131)
plt.axis('off')
plt.imshow(data_map)
plt.subplot(132)
plt.imshow(data_ndcg)
plt.subplot(133)
plt.imshow(data_mrr)
plt.show()

