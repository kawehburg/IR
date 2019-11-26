# Homework4: Clustering with sklearn

## 实验内容

测试sklearn中聚类算法在数据集上的聚类效果。

Dataset：sklearn.datasets.load_digits & sklearn.datasets.fetch_20newsgroups

Method：K-Means, Affinity propagation, Mean-shift, Spectral clustering, Ward hierachical clustering, Agglomerative, DBSCAN, Gaussian mixtures

Metrics：metrics.normalized_mutual_info_score(labels_true, labels_pred), metrics.homogeneity_score(labels_true, labels_pred), metrics.completeness_score(labels_true, labels_pred) 

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



### 3. Digits

```
    x = load_digits()
    y = x.target
    x = x.data
```

聚类结果（PCA）：



聚类结果（t-SNE）：






### 4. Metrics

对聚类结果进行评价

Blobs：

Method: NMI Homogeneity Completeness
K-Means: 1.0 1.0 1.0
AffinityPropagation@10: 1.0 1.0 1.0
MeanShift@7: 0.9051972175176031 0.819382002601611 0.9999999999999999
SpectralClustering: 1.0 1.0 1.0
AgglomerativeClustering: 1.0 1.0 1.0
DBSCAN@8: 0.9378635304426797 0.8795880017344073 1.0
GaussianMixture: 0.9568429975232176 0.9397940008672038 0.9742012835412709

Digits-PCA

Method: NMI Homogeneity Completeness
K-Means: 0.609477490076555 0.5867461941043316 0.6330894254492019
AffinityPropagation@21: 0.6488625513318248 0.7297289735898393 0.5769575085523329
MeanShift@12: 0.6411514095811631 0.6216736184191277 0.661239463648542
SpectralClustering: 0.3923697167600664 0.29278282817696594 0.5258300003076707
AgglomerativeClustering: 0.6662308884106493 0.6457870655497341 0.6873219058585489
DBSCAN@40: 0.630809764815567 0.74627218619495 0.5332115637533911
GaussianMixture: 0.6628311657225646 0.6357667035768301 0.6910477566399335

Digits-t-SNE

Method: NMI Homogeneity Completeness
K-Means: 0.9311482557690978 0.9180683016717409 0.9444145633206336
AffinityPropagation@25: 0.8629329769863701 0.9890862287448055 0.7528699734456492
MeanShift@10: 0.9311482557690978 0.9180683016717409 0.9444145633206336
SpectralClustering: 0.39575837089770977 0.26957732877296814 0.5810009649124276
AgglomerativeClustering: 0.9311482557690978 0.9180683016717409 0.9444145633206336
DBSCAN@20: 0.9112275182715193 0.9874775147653276 0.8408653135282779
GaussianMixture: 0.9311482557690978 0.9180683016717409 0.9444145633206336