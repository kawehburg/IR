# Homework4: Clustering with sklearn

## 实验内容

测试sklearn中聚类算法在数据集上的聚类效果。

**Dataset**：sklearn.datasets.load_digits & sklearn.datasets.fetch_20newsgroups

**Method**：K-Means, Affinity propagation, Mean-shift, Spectral clustering, Ward hierachical clustering, Agglomerative, DBSCAN, Gaussian mixtures

**Metrics**：metrics.normalized_mutual_info_score(labels_true, labels_pred), metrics.homogeneity_score(labels_true, labels_pred), metrics.completeness_score(labels_true, labels_pred) 

## 实验结果

### 1. 运行聚类算法

```
from sklearn.cluster import (
    KMeans,
    AffinityPropagation,
    MeanShift, estimate_bandwidth,
    SpectralClustering,
    AgglomerativeClustering,
    DBSCAN)
from sklearn.mixture import GaussianMixture
```

通过cluster函数在各个聚类算法上对输入数据进行聚类

### 2. TOY data - Blobs

```
def blobs(n_class=10):
    return make_blobs(n_samples=500, n_features=2, centers=n_class, cluster_std=[0.5] * n_class, random_state=0)
```

聚类结果：

![Blobs]( https://github.com/kawehburg/IR/blob/master/ex4/blobs.png )

实验结果表明聚类算法可以很好完成对TOY Data的聚类，但可能出现对很临近的类的误判

### 3. Digits

```
    x = load_digits()
    y = x.target
    x = x.data
```

聚类结果（PCA）：

![Digits-PCA]( https://github.com/kawehburg/IR/blob/master/ex4/digits-pca.png )

聚类结果（t-SNE）：

![Digits-t-SNE]( https://github.com/kawehburg/IR/blob/master/ex4/digits-tsne.png )

从实验结果来看t-SNE具有更好的降维效果，运算时间更长，聚类算法根据降维效果不同在聚类上结果不同


### 4. Metrics

使用metric函数对聚类标签进行测评

```
def metric(labels_true, labels_pred):
    m1 = metrics.normalized_mutual_info_score(labels_true, labels_pred)
    m2 = metrics.homogeneity_score(labels_true, labels_pred)
    m3 = metrics.completeness_score(labels_true, labels_pred)
    return m1, m2, m3
```

对聚类结果进行评价结果如下

#### Blobs

| Method                  | NMI   | Homogeneity | Completeness |
| ----------------------- | ----- | ----------- | ------------ |
| K-Means                 | 1.0   | 1.0         | 1.0          |
| AffinityPropagation@10  | 1.0   | 1.0         | 1.0          |
| MeanShift@7             | 0.905 | 0.819       | 1.0          |
| SpectralClustering      | 1.0   | 1.0         | 1.0          |
| AgglomerativeClustering | 1.0   | 1.0         | 1.0          |
| DBSCAN@8                | 0.938 | 0.880       | 1.0          |
| GaussianMixture         | 0.957 | 0.940       | 0.974        |

#### Digits-PCA

| Method                  | NMI                    | Homogeneity          | Completeness           |
| :---------------------- | ---------------------- | -------------------- | ---------------------- |
| K-Means                 | 0.609477490076555      | 0.5867461941043316   | 0.6330894254492019     |
| AffinityPropagation@21  | 0.6488625513318248     | 0.7297289735898393   | 0.5769575085523329     |
| MeanShift@12            | 0.6411514095811631     | 0.6216736184191277   | 0.661239463648542      |
| SpectralClustering      | 0.3923697167600664     | 0.29278282817696594  | 0.5258300003076707     |
| AgglomerativeClustering | **0.6662308884106493** | 0.6457870655497341   | 0.6873219058585489     |
| DBSCAN@40               | 0.630809764815567      | **0.74627218619495** | 0.5332115637533911     |
| GaussianMixture         | 0.6628311657225646     | 0.6357667035768301   | **0.6910477566399335** |

#### Digits-t-SNE

| Method                  | NMI                    | Homogeneity            | Completeness           |
| :---------------------- | ---------------------- | ---------------------- | ---------------------- |
| K-Means                 | **0.9311482557690978** | 0.9180683016717409     | **0.9444145633206336** |
| AffinityPropagation@25  | 0.8629329769863701     | **0.9890862287448055** | 0.7528699734456492     |
| MeanShift@10            | **0.9311482557690978** | 0.9180683016717409     | **0.9444145633206336** |
| SpectralClustering      | 0.3957583708977097     | 0.26957732877296814    | 0.5810009649124276     |
| AgglomerativeClustering | **0.9311482557690978** | 0.9180683016717409     | **0.9444145633206336** |
| DBSCAN@20               | 0.9112275182715193     | 0.9874775147653276     | 0.8408653135282779     |
| GaussianMixture         | **0.9311482557690978** | 0.9180683016717409     | **0.9444145633206336** |

从测评结果来看，对于不同指标，模型的排序是不同的，对于简单的聚类指标普遍更高，t-SNE相比PCA指标明显提升。

### 5. 实验结论

通过本次实验学习了一系列聚类算法，对多个数据集进行运行聚类算法，并对高维数据使用PCA和t-SNE进行降维可视化，进行了对不同算法在三个指标上的评测。