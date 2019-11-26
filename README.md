### 信息检索与数据挖掘

## [Homework1: Inverted index and Boolean Retrieval Model](https://github.com/kawehburg/IR/tree/master/ex1)

### 任务： 

- 使用我们介绍的方法，在tweets数据集上构建inverted index; 
- 实现Boolean Retrieval Model，使用TREC 2014 test topics进行测试； 
- Boolean Retrieval Model： 
  - Input：a query (like Ron and Weasley) 
  - Output: print the qualified tweets. 
  - 支持and, or ,not；查询优化可以选做； 

### 注意：

- 对于tweets与queries使用相同的预处理

## [Homework2: Ranked retrieval model](https://github.com/kawehburg/IR/tree/master/ex2)

### 任务：

- 在Homework1.1的基础上实现最基本的Ranked retrieval model 
  - Input：a query (like Ron Weasley birthday) 
  - Output: Return the top K (e.g., K = 10) relevant tweets. 
- Use SMART notation: lnc.ltc 
  - Document: logarithmic tf (l as first character), no idf and cosine normalization 
  - Query: logarithmic tf (l in leftmost column), idf (t in second column), no normalization 
- 改进Inverted index 
  - 在Dictionary中存储每个term的DF 
  - 在posting list中存储term在每个doc中的TF with pairs (docID, tf) 
- 选做 • 支持所有的SMART Notations 

## [Homework3: IR Evaluation](https://github.com/kawehburg/IR/tree/master/ex3)

### 任务：

实现以下指标评价，并对HW2检索结果进行评价

- Mean Average Precision (MAP)
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (NDCG)

## [Homework4: Clustering with sklearn]( https://github.com/kawehburg/IR/tree/master/ex4 )

### 任务：

测试sklearn中聚类算法在数据集上的聚类效果。

**Dataset**：sklearn.datasets.load_digits & sklearn.datasets.fetch_20newsgroups

**Method**：K-Means, Affinity propagation, Mean-shift, Spectral clustering, Ward hierachical clustering, Agglomerative, DBSCAN, Gaussian mixtures

**Metrics**：metrics.normalized_mutual_info_score(labels_true, labels_pred), metrics.homogeneity_score(labels_true, labels_pred), metrics.completeness_score(labels_true, labels_pred)