# Homework2: Ranked retrieval model

## 实验内容

1. 在Homework1.1的基础上实现最基本的Ranked retrieval model 
   - Input：a query (like Ron Weasley birthday) 
   - Output: Return the top K (e.g., K = 10) relevant tweets. 
2. Use SMART notation: lnc.ltc 
   - Document: logarithmic tf (l as first character), no idf and cosine normalization 
   - Query: logarithmic tf (l in leftmost column), idf (t in second column), no normalization 
3. 改进Inverted index 
   - 在Dictionary中存储每个term的DF 
   - 在posting list中存储term在每个doc中的TF with pairs (docID, tf) 
4. 选做 
   - 支持所有的SMART Notations 

## 实验结果

### 1.  在Homework1.1的基础上实现最基本的Ranked retrieval model 

将Homework1封装成类作为ir基础类，在Homework2中继承，添加了

- 构建tf df方法
- 解析SMART notation方法（支持所有的SMART Notations）
- cache机制
- 交互层加入SMART notation

修改了

- 获得排名元素的方法
- 排名算法

### 2. 构建tf df方法

在读入数据的时候记录每个doc中的TF with pairs (docID, tf) ，记录每个term的DF 

### 3. 解析SMART notation方法

对于[列表](https://nlp.stanford.edu/IR-book/html/htmledition/document-and-query-weighting-schemes-1.html)中的各种计算weight方法，对应python代码：

```
def smart_notation(name):
    collect1 = {'n': lambda x, y: x,
                'a': lambda x, y: 0.5 + 0.5 * x / max(y),
                'b': lambda x, y: 1 if x > 0 else 0,
                'L': lambda x, y: (1 + np.log(x)) / (1 + np.log(np.average(y))) if x != 0 else 0,
                'l': lambda x, y: 1 + np.log(x) if x != 0 else 0}
    collect2 = {'t': lambda x, y: np.log(y / x) if x != 0 else 0,
                'p': lambda x, y: max(0, np.log((y - x) / x)) if x != 0 else 0,
                'n': lambda x, y: 1}
    collect3 = {'n': lambda x: 1,
                'c': lambda x: 1 / sum([i ** 2 for i in x] + [0.001]) ** 0.5}
```

### 4. 获得排名元素的方法

沿用Homework1中的表示，用<...>里的元素作为排名依据，<...>可以写在表达式外，在Homework2中支持多个<...>和一个<...>中有多个元素
```
$ <ron> && <birthday happy>
[optimize] ron && birthday && happy 
[rank] ['ron', 'birthday', 'happy']
```

### 5. 排名算法

使用SMART notation解析得到的函数对query和document完成以下运算：

``tf -> tf-wght	   df -> idf    tf-wght,idf -> weight -> n'lized``

再计算出product得到关联度，使用heap优化排序过程，获得最高k个text

对应代码中的函数 ``def text_score(self, x, regular, use_cache=False)``和``def count(self, res, regular) ``

### 6. cache机制

实验中发现doc的tf大部分相同，具有相同的weight，且query的weight对于所有text一样，因此对tf做hash，``hash(tf) = sum(100^i*tf[i])``；创建cache(dict)，在cache中记录出现过的tf，记录为hash(tf) -> weight映射，优先查询cache可以提高查询效率

### 7. 交互层加入SMART notation
直接输入SMART notation切换计算逻辑，默认为lnc.ltc
```
$ lnc.ltc
SMART notation: lnc.ltc                                   
```

指定k的大小，默认为10

```
$ k=20
```

输入查询表达式，获得查询结果

```
$ <Ron Weasley birthday>
[optimize] ron weasley birthday 
[rank] ['ron', 'weasley', 'birthday']
Find out about 10 results
  17168 Happy birthday Ronald Billius Weasley #HappyBirthday #HarryPotter #RonaldWeasley #Ron #RupertGrint http://t.co/sncjxTn2pu
  17142 Happy belated birthday, Ron Weasley.
  17132 A very happy birthday to Ron Weasley! #NerdyTweet
  17037 Happy Birthday Ron Weasley! \ud83c\udf89\ud83c\udf88 #WeasleyIsOurKing
  17023 Happy Birthday Ron Weasley!!
  17011 Happy birthday ron weasley
  16995 Let's not forget that today is also Ron Weasley's birthday
  16980 Happy birthday to my second boyfriend Ron Weasley \ud83d\ude0d\u2764\ud83c\udf81\ud83c\udf89\ud83c\udf88
  16973 Happy Birthday Ron Weasley.  :'3. Mi pelirrojo favorito.
  16971 Ahhhh Happy Birthday to Mr. Ron Weasley, he's such an old man now :P
Find out about 10 results
```

查询的切换：

```
$ lnc.ltc
SMART notation: lnc.ltc
Find out about 0 results
Find out about 0 results

$ <just do it>
[optimize] just do it 
[rank] ['just', 'do', 'it']
Find out about 10 results
  29966 @IanMcKellen just saw #MrHolmes - it was great!! By chance do you know the type of fountain pen that you used in the film?
  22212 \u201c@ComedyAndTruth: do you ever just look at clothes online and cry\u201d \ud83d\ude02\ud83d\ude02 it be that serious sometimes
  4954 Texting While Driving: Just DON'T Do It (You Too Mom!) http://t.co/83384nZ via @huffingtonpost
  18123 Just read a report about a CHILD CURED OF HIV! I cannot wait to get in there and do my part #HIV#medicine#stillhope
  21783 Label GMOs. Not because they are untested potential health risks. Do it because I don't want to give $$ to Monsanto supporters. #justlabelit
  26629 Don't Count on El Ni\u00f1o Alone to End California's Drought: Drought isn\u2019t just about supply\u2014it\u2019s also about demand. http://t.co/ueKWQoT7Gi
  22959 @DomsWildThings @PaolaZajac If you were on BBC's Sherlock it would just be too much for me!! xD
  22178 Cats Don't Dance is what you get if Mr. Rogers was a movie. It's just so sincere and loving in an age of irony and sarcasm.
  18510 look for the 'non gmo project' label on carton and bottled goods... just because it's labeled 'organic ' doesn't... http://t.co/N3d0AbK2fi
  16439 I hope the snow blower works wonders for this snow clean up, its great to have, I so just don't feel up to it, being sick and all.
Find out about 10 results

$ nnn.nnn
SMART notation: nnn.nnn
Find out about 0 results
Find out about 0 results

$ <just do it>
[optimize] just do it 
[rank] ['just', 'do', 'it']
Find out about 10 results
  29966 @IanMcKellen just saw #MrHolmes - it was great!! By chance do you know the type of fountain pen that you used in the film?
  22212 \u201c@ComedyAndTruth: do you ever just look at clothes online and cry\u201d \ud83d\ude02\ud83d\ude02 it be that serious sometimes
  8283 I am #Erdogan. I just bombed the American embssy in Ankara to blame it on the PKK.So it seems as if PKK is against peace talks #TwitterKurds
  7683 Just had the worst fries from McDonald's. It tasted like I just ate a small bowl of mashed potatoes.
  4954 Texting While Driving: Just DON'T Do It (You Too Mom!) http://t.co/83384nZ via @huffingtonpost
  4270 i just found out theres a @FL_McDonalds on twitter, i hate you, not the person behind it just that bastard Ronald
  26629 Don't Count on El Ni\u00f1o Alone to End California's Drought: Drought isn\u2019t just about supply\u2014it\u2019s also about demand. http://t.co/ueKWQoT7Gi
  25242 Greek bank curbs hit children's charities just as needs soar: Donors entitled to withdraw just\u2026 http://t.co/Dvj1WpK5iZ #til_now #news #DNA
  23756 .@Justin_M_Craig\u2014 RT @nprmonkeysee: What do Gone Girl and 50 Shades Of Grey have to do with each other? What? WHAT? http://t.co/PKNLcyalZX
  22959 @DomsWildThings @PaolaZajac If you were on BBC's Sherlock it would just be too much for me!! xD
Find out about 10 results

$ k=3
Find out about 0 results
Find out about 0 results

$ <just do it>
[optimize] just do it 
[rank] ['just', 'do', 'it']
Find out about 3 results
  29966 @IanMcKellen just saw #MrHolmes - it was great!! By chance do you know the type of fountain pen that you used in the film?
  22212 \u201c@ComedyAndTruth: do you ever just look at clothes online and cry\u201d \ud83d\ude02\ud83d\ude02 it be that serious sometimes
  8283 I am #Erdogan. I just bombed the American embssy in Ankara to blame it on the PKK.So it seems as if PKK is against peace talks #TwitterKurds
Find out about 3 results

$ 
```