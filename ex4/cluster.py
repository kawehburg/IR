import sklearn
from sklearn.cluster import (
    KMeans,
    AffinityPropagation,
    MeanShift, estimate_bandwidth,
    SpectralClustering,
    AgglomerativeClustering,
    DBSCAN)
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_digits, make_blobs, fetch_20newsgroups
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)


def unique(_data):
    return len(np.unique(_data))


def metric(labels_true, labels_pred):
    m1 = metrics.normalized_mutual_info_score(labels_true, labels_pred)
    m2 = metrics.homogeneity_score(labels_true, labels_pred)
    m3 = metrics.completeness_score(labels_true, labels_pred)
    return m1, m2, m3


def cluster(x, y, n_class):
    plt.figure()

    plt.subplot(241)
    plt.title('RAW')
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=y)

    kmeans_pre = KMeans(n_clusters=n_class, random_state=9).fit_predict(x)
    plt.subplot(242)
    plt.title('K-Means')
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=kmeans_pre)

    aff_pre = AffinityPropagation(preference=-50).fit(x)
    cluster_centers_indices = aff_pre.cluster_centers_indices_
    labels = aff_pre.labels_
    n_clusters_ = len(cluster_centers_indices)
    plt.subplot(243)
    plt.title('AffinityPropagation@{}'.format(unique(labels)))
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=labels)

    bandwidth = estimate_bandwidth(x, quantile=0.2, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth / 2)
    ms.fit(x)
    labels1 = ms.labels_
    cluster_centers = ms.cluster_centers_
    plt.subplot(244)
    plt.title('MeanShift@{}'.format(unique(labels1)))
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=labels1)

    sc_pre = SpectralClustering(n_clusters=n_class).fit_predict(x)
    plt.subplot(245)
    plt.title('SpectralClustering')
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=sc_pre)

    clustering = AgglomerativeClustering(n_clusters=n_class).fit(x)
    labels2 = clustering.labels_
    plt.subplot(246)
    plt.title('AgglomerativeClustering')
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=labels2)

    labels3 = DBSCAN(eps=abs(np.max(x) - np.min(x)) / n_class / 2, min_samples=1).fit_predict(x)
    plt.subplot(247)
    plt.title('DBSCAN@{}'.format(unique(labels3)))
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=labels3)

    gmm = GaussianMixture(n_components=n_class)
    gmm.fit(x)
    labels4 = gmm.predict(x)
    plt.subplot(248)
    plt.title('GaussianMixture')
    plt.axis('off')
    plt.scatter(x[:, 0], x[:, 1], c=labels4)

    plt.show()

    preds = [kmeans_pre, labels, labels1, sc_pre, labels2, labels3, labels4]
    names = ['K-Means',
             'AffinityPropagation@{}'.format(unique(labels)),
             'MeanShift@{}'.format(unique(labels1)),
             'SpectralClustering',
             'AgglomerativeClustering',
             'DBSCAN@{}'.format(unique(labels3)),
             'GaussianMixture']
    print('Method:', 'NMI', 'Homogeneity', 'Completeness')
    for name, pred in zip(names, preds):
        m1, m2, m3 = metric(y, pred)
        print(name + ':', m1, m2, m3)


def blobs(n_class=10):
    return make_blobs(n_samples=500, n_features=2, centers=n_class, cluster_std=[0.5] * n_class, random_state=0)


def digits():
    x = load_digits()

    print(x.data.shape)
    y = x.target
    x = x.data
    # plt.imshow(x.images[120], cmap='gray')
    # plt.show()

    tsne = TSNE(n_components=2, init='pca', random_state=0)
    x = tsne.fit_transform(x)

    # pca = PCA(n_components=2)
    # pca.fit(x, y)
    # x = pca.transform(x)

    x = x[:100]
    y = y[:100]
    print('TSNE DONE')
    return x, y


def newsgroups():
    x = fetch_20newsgroups()
    print(x.target)


if __name__ == '__main__':
    # cluster(*blobs(n_class=10), 10)
    cluster(*digits(), 10)
    # newsgroups()
