# Homework1: Inverted index and Boolean Retrieval Model

- [实验报告](https://github.com/kawehburg/IR/blob/master/ex1/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.pdf)
- [DATA](https://github.com/kawehburg/IR/blob/master/ex1/tweets2.txt)
- Homework1更新的代码封装到了irmodel里

## 实验内容

1. 建立词到文档的索引表：遍历数据集，对每个 text 以空格分词，用 set 建词典， 用 dict 建词到 text id 的映射。同时建立字母到 text 的索引。 
2. 建立词片段到词表的索引：遍历词表，用{作为词的开始结束符，用二维数组建 [a][b]->(word)abc 的映射
3. 布尔原子操作：实现 and，or，not，xor，输入 seq1，seq2(or max_len)，输出操 作后的 seq，复杂度为 O(seq1+seq2)
4. 表达式解析：根据顺序运算的原则遍历表达式，依次通过布尔原子操作完成运算， 对于(…)使用递归处理。函数同时传入表达式和数据源，对于表达式中的符号从数 据源中获得索引的序列
5. 表达式重整：对于用户输入的表达式，重整为用一个空格分开的布尔运算符和查询 索引的重整表达式，对连续的布尔运算基于运算符优先级进行重排以优化查询效率
6. 对表达式中的查询索引通过此片段到词，词到文档的两步查询获得对 text 查询结 果，以 dict 形式存入数据源中 
7. 输出结果：可以通过<…>运算符定义输出次序，对于查询结果使用.count(…)排序，<>可以写在表达式中或者在表达式后定义

## 实验结果

### 1. 建立词到文档的索引表

构建倒排索引生成词到文档的索引表，实验中去除了所有非英文字母的符号， 忽略了重复文本，建立了 53113 个词到 27799 个 text 的索引。

### 2. 建立词片段到词表的索引 

建立27*27的二维数组表示从（a,b)->(word)ab 的映射，用{作为词的开始结束符(因为 {的 ascii 编码在 z 后面便于编程 )

### 3. [布尔原子操作 ](https://github.com/kawehburg/-/blob/master/ex1/boolop.py)
实现 and，or，not，xor，输入 seq1，seq2(or max_len)，输出操 作后的 seq，复杂度为 O(seq1+seq2)

### 4. [表达式解析](https://github.com/kawehburg/IR/blob/master/ex1/op_compile.py)

输入的表达式和数据源 

```
print(cp('a && ( b || ( ! c ) )', {'a': [1, 2, 3], 'b': [3, 4, 5], 'c': [2, 3, 4]}))
```

output：

```
[1, 3]
```

算法可以适应各种组合和长度的合法的表达式，从左向右依次运算，(…)递归处理 ，表达式中的数据存在source中

### 5. 表达式重整 

- 重整为用一个空格分开的布尔运算符和查询索引的重整表达式，对！添加() 


```
$ a&& b ||(! c)
```

output:

```
a && b || ( ( ! C ) )
```

- 对连续的布尔运算基于运算符优先级进行重排以优化查询效率，&&具有高于||的优先级


```
a||b&&(c||!(D&&e)&&F)
```

output:

```
a && ( c && f || ( ! ( d && e ) ) ) || b
```

- 一个更复杂的表达式，重整后去除了<…> ，其中<...>为定义输出次序运算符


```
is{||((!ab ||askm) && < lm>) &&(s{ab && cc)
```

output:

```
is{ && ( s{ab && cc ) || ( ( ( ! ab ) || askm ) && lm )
```

- 如果表达式中两个查询词间无运算符默认为上一运算符，初始运算符为and 


### 6. 从词片段到 text，得到数据源 

对于每个查询词通过索引表获得索引结果 

```
$ hello world
```

output:

```
[optimize] hello world
[source]
hello : [1045, 4015, 5185, ...]
world : [10, 49, 89, ...]
```

其中对于每个词的检索通过词中字母所有字母组合 and 得到 如 wor{ld = wo && or && r{ && {l && ld，查询获得词序列，在通过词检索text id并用or运算得到结果

```
$ {hello{ wor{ld
```

output:

```
[optimize] {hello{ wor{ld
[source]
{hello{ : [1045, 5185, 5550, ...]
wor{ld : []
```

后续表达式和数据源一起进入布尔运算函数 

### 7. [输出结果](https://github.com/kawehburg/IR/blob/master/ex1/agent.py)

- 通过上述步骤获得查询结果，显示 text 和 id 

```
$ {hello{ {world{
```

output:

```
[optimize] {hello{ {world{ 
Find out about 1 results
  15114 Hello World, Cornell scientists 3D print ears with help from rat tails and cow ears:   Science! A t... http://t.co/eRZyjXVkTP Thank You!
Find out about 1 results
```

- <…>中的字符串出现的次数作为排序依据，对检索结果按降序排列

```
$ <love>
```

output:

```
[optimize] love 
Find out about 386 results
  12323 \u266a I, I love you like John loves Sherlock! I, I love you like John loves Sherlock! And I keep hitting re-peat-peat-peat-peat-peat-peat! \u266b
  9916 @kylieminogue #loveisloveislove!!  Equal marriage UK Yes Vote. Oh Happy Day :-)
   ...
Find out about 386 results
```

- <…>可以写在表达式外面 

```
$ weasley && birthday <ron>
```

output:

```
[optimize] weasley && birthday 
Find out about 66 results
  16792 It's Ron Weasley's birthday! The ginger who vomited slugs out from his mouth' happy birthday Ron! #RonWeasleyBirthday
  16819 #HappyBirthdayRonWeasley mumpung lgi ultah ron.. Gimna kalo admin kasih fact ron?
  ...
Find out about 66 results
```

### 8. [交互](https://github.com/kawehburg/IR/blob/master/ex1/agent.py)

在$输入表达式查询直到查询为空退出 

```
$ Hubble oldest star
[optimize] hubble oldest star 
Find out about 5 results
  19231 Hubble telescope dates oldest star, 'Methuselah', at 14.5 billion years old Hubble telescope dates oldest ... http://t.co/dw9KBCcBM1
  19258 Hubble Finds Birth Certificate of Oldest Known Star http://t.co/VPNYz8iMkG
  19388 NASA`s Hubble Telescope finds birth certificate of oldest known star http://t.co/hhb8YwGz6A
  19411 Hubble Finds Birth Certificate of Oldest Known Star http://t.co/LZsevtVRT8
  19715 ''Hubble Finds Birth Certificate of Oldest Known Star'' image: http://t.co/QNvfLVKMwW via #NASA_APP
Find out about 5 results``

$ 
```

## 实验结论



通过实验学习了文档倒排索引和布尔查询，使用 python 实现了一个支持复杂表达式 布尔检索和词片段查询的信息检索系统，经测试对各种查询要求具有较高的查询效率，对用户输入有较好的鲁棒性，并进行了运算次序优化。

```
$ is{||((!ab ||askm) && < lm>) &&(s{ab && cc)

[optimize] is{ && ( s{ab && cc ) || ( ( ( ! ab ) || askm ) && lm ) 
Find out about 758 results
  21393 Download Sherlock Holmes: The Classic BBC Series Starring Douglas Wilmer The Film Online\n\nSherlock Holmes: The http://t.co/z28imzN1oQ
  111 \u2018The King\u2019s Speech\u2019 is top film at producer awards: \u201cThe King\u2019s Speech\u201d claimed the crown for best film at the P... http://bit.ly/eV6RLM
  ...
Find out about 758 results

$ 
```

















