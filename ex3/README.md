# Homework3:  IR Evaluation

## 实验内容

实现以下指标评价，并对HW2检索结果进行评价 

- Mean Average Precision (MAP) 
- Mean Reciprocal Rank (MRR) 
- Normalized Discounted Cumulative Gain (NDCG) 

## 实验结果

### 1. 实现指标评价

实验中提供了MAP，NDCG实现，根据提供的代码格式，实现了MRR指标函数 -> 把标准答案在被评价系统给出结果中的排序取倒数作为它的准确度，再对所有的问题取平均

### 2. 在HW2基础上的操作

继承HW2中Agent类，添加了

- 从data序号到tweetID的映射的静态方法 - get_id
- 从qrels2014获得所有query的静态方法 - read_query
- 将query规范化的方法 - query_org
- 检索方法 - retrieve

修改了

- 从word到source的方法 - org
- 将match方法中的print作为参数

### 3. 从data序号到tweetID的映射的静态方法

在之前实验中使用序号作为索引，在HW3中换成tweetID，记录data序号到tweetID的映射关系

### 4. 从qrels2014获得所有query的静态方法

读取qrels2014文件，提取中其中的query，index从171开始顺序定义
### 5. 将query规范化的方法

对于query中所有非字母且不出现在OPERATOR中的字符用空格替代，调用reg方法解析query表达，并用||操作拼接word，将<>接在query左右作为排序依据

### 6. 检索方法

接受smart notation表达式，k的赋值，以及查询query，完成对smart和k的赋值后，调用query_org规范表达式，调用match方法获得检索结果，将match中的print设置为空操作：

`result = self.match(self.query_org(q), report=lambda x, *args, **kwargs: None)`

对于所有query进行操作获得检索结果

### 7. 从word到source的方法
在之前的方法中会将word分解为字母组合的片段，在从字母组合索引到字母，再从字母获得source。

在HW3中word是确定的单词，直接通过word获得source，这样符合题目要求，且避免了极为耗时的从字母组合索引到字母的过程

### 8. 将match方法中的print作为参数

在之前方法中会在match中print当前信息，在HW3中会print大量信息没有必要，因此将print作为参数report传入方法，使用report(info)替代print(info)，在检索时设置为空操作使print失效。

`def match(self, exp, report=print):`

### 9. 对HW2检索结果进行评价的函数

通过evaluation方法完成

`def evaluation(smart='lnc.ltc', file=None, agent=None, source=None, k=100, cache=True, output=None):`

使用agent对qrels2014中query使用检索方法获得结果，存入文件中，调用实现指标评价中的函数对文件进行指标评价，并将结果输出

Parameters：

smart：str，输入smart nota表达式

file：str，检索结果输出文件，如果是None则会以smart和k命名

agent：Eval，HW3中检索类，如果是None则会在函数中构建

source：dict，包括所有query和tweetID映射，如果是None则会在函数中构建

k：int，查询前k个结果

cache：bool，是否使用cache，使用cache时会判断file是否已存在，如果存在直接使用file作指标不在进行检索

output：stream，本次检索的指标的输出流，应用于`print(, file=output)`

Return:

`{'agent': agent, 'source': source}`

并定义batch函数对多个smart notation进行批处理

### 10. 获得smart notation组合的指标

```
collect1 = 'nabLl'
collect2 = 'tpn'
collect3 = 'nc'
collect = [x + y + z for x in collect1 for y in collect2 for z in collect3]
batch_list = [x + '.' + y for x in collect for y in collect]
```
对应HW2中实现的smart notation表达式，在batch_list中包括了30*30=900个不同的表达式组合，这些表达式都可以通过评价方法获得指标。

实验中设置k=20，将所有指标输出到log中，结果如下

```
[TASK] nnc.bnc
[build file] tmp/nnc.bnc.20.txt
MAP = 0.23514020280837972
NDCG = 0.7447655117521886
MRR = 0.0579974098547128
[TASK] nnc.Ltn
[build file] tmp/nnc.Ltn.20.txt
MAP = 0.2460346537632576
NDCG = 0.7349076951742601
MRR = 0.05923067951895832
...
```
总共计算了900个指标

### 11. 结果可视化

使用matplotlib将smart notation组合的指标进行可视化结果如下

![result](https://github.com/kawehburg/IR/blob/master/ex3/result.png)

