# 文章_机器学习_PySpark-3.0.3文本特征提取(TF-IDF)流程_GF_2023-12-29

本例中 Tokenizer 是用于分词的模块。

本例中 HashingTF().tranform() 函数把词哈希成特征向量, 返回结果是 Vectors.sparse() 类型的。

本例中 IDF 类用于计算给定文档集合的反文档频率, 是一个词普遍重要性的度量 (即: 一个词存在多少个文档中)。

## 导入 pyspark.sql 相关模块

Spark SQL 是用于结构化数据处理的 Spark 模块。它提供了一种成为 DataFrame 编程抽象, 是由 SchemaRDD 发展而来。

不同于 SchemaRDD 直接继承 RDD, DataFrame 自己实现了 RDD 的绝大多数功能。

```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF
```

## 创建 SparkSession 对象

Spark 2.0 以上版本的 spark-shell 在启动时会自动创建一个名为 spark 的 SparkSession 对象。

当需要手工创建时, SparkSession 可以由其伴生对象的 builder 方法创建出来。

```python
spark = SparkSession.builder.master("local[*]").appName("spark").getOrCreate()
```

## 使用 Spark 构建 DataFrame 数据 (行作为列表中的列表)

当数据量较小时, 可以使用该方法手工构建 DataFrame 数据。

构建数据集 (行作为列表中的列表):

```python
# 创建一个简单的 DataFrame, 每一个句子代表一个文档。
Data_Set = [[0, "I heard about Spark and I love Spark"],
            [0, "I wish Java could use case classes"],
            [1, "Logistic regression models are neat"]]
```

将数据集转化到指定列名的 DataFrame 数据框:

```python
SDF = spark.createDataFrame(Data_Set).toDF("label", "sentence")
```

输出 DataFrame 数据框:

```python
print("[Message] Builded Spark DataFrame:")
SDF.show()
```

输出:

```txt
[Message] Builded Spark DataFrame:
+-----+--------------------+
|label|            sentence|
+-----+--------------------+
|    0|I heard about Spa...|
|    0|I wish Java could...|
|    1|Logistic regressi...|
+-----+--------------------+
```

## 特征提取 Step 1 - 使用 Tokenizer 创建分词器对象

```python
# 特征提取 Step 1 - 创建分词器对象。
MyTokenizer = Tokenizer().setInputCol("sentence").setOutputCol("Words")
Data_for_Words = MyTokenizer.transform(SDF)

# 输出 Tokenizer 的转换效果。
print("[Message] The Effect of Tokenizer:")
Data_for_Words.select(["label", "sentence", "Words"]).show()
```

输出:

```txt
[Message] The Effect of Tokenizer:
+-----+--------------------+--------------------+
|label|            sentence|               Words|
+-----+--------------------+--------------------+
|    0|I heard about Spa...|[i, heard, about,...|
|    0|I wish Java could...|[i, wish, java, c...|
|    1|Logistic regressi...|[logistic, regres...|
+-----+--------------------+--------------------+
```

## 特征提取 Step 2 - 使用 HashingTF 创建词频映射

`HashingTF().tranform()` 函数把词哈希成特征向量, 返回结果是 `Vectors.sparse()` 类型的。

这里设置哈希表的桶数 `setNumFeatures` 为1000 (注意: 该值设置太小会造成哈希冲突)。

```python
# 特征提取 Step 2 - 使用 HashingTF 创建词频映射, 计算某个词在文件中出现的频率。
MyHashingTF = HashingTF().setInputCol("Words").setOutputCol("Features(Raw)").setNumFeatures(1000) # -> 返回一个 Transformers。
Featurized_for_Words = MyHashingTF.transform(Data_for_Words)

# 输出 HashingTF 的转换效果。
print("[Message] The Effect of HashingTF:")
Featurized_for_Words.select(["label", "Words", "Features(Raw)"]).show()
```

输出:

```txt
[Message] The Effect of HashingTF:
+-----+--------------------+--------------------+
|label|               Words|       Features(Raw)|
+-----+--------------------+--------------------+
|    0|[i, heard, about,...|(1000,[240,286,67...|
|    0|[i, wish, java, c...|(1000,[80,133,307...|
|    1|[logistic, regres...|(1000,[59,286,604...|
+-----+--------------------+--------------------+
```

## 特征提取 Step 3 - 创建 IDF 类并计算 IDF 度量值

**IDF 类**: 计算给定文档集合的反文档频率, 是一个词普遍重要性的度量 (即: 一个词存在多少个文档中)。

某一特定词语的 IDF, 可以由总文件数目除以包含该词语之文件的数目, 再将得到的商取对数得到。

```python
# 特征提取 Step 3 - 创建 IDF 类。
MyIDF = IDF().setInputCol("Features(Raw)").setOutputCol("Features(IDF)") # -> 返回一个 Estimator。

IDFModel_for_Words = MyIDF.fit(Featurized_for_Words)

# 计算每一个单词对应的 IDF 度量值。
Rescaled_for_Words = IDFModel_for_Words.transform(Featurized_for_Words)

# 输出 IDF 的计算结果的 DataFrame。
print("[Message] The Calculation Result DataFrame of IDF:")
Rescaled_for_Words.select(["label", "Words", "Features(Raw)", "Features(IDF)"]).show()

# 输出 IDF 的计算结果的 RDD。
print("[Message] The Calculation Result RDD of IDF:")
pprint.pprint(Rescaled_for_Words.rdd.take(3))
```

输出:

```txt
[Message] The Calculation Result DataFrame of IDF:
+-----+--------------------+--------------------+--------------------+
|label|               Words|       Features(Raw)|       Features(IDF)|
+-----+--------------------+--------------------+--------------------+
|    0|[i, heard, about,...|(1000,[240,286,67...|(1000,[240,286,67...|
|    0|[i, wish, java, c...|(1000,[80,133,307...|(1000,[80,133,307...|
|    1|[logistic, regres...|(1000,[59,286,604...|(1000,[59,286,604...|
+-----+--------------------+--------------------+--------------------+
[Message] The Calculation Result RDD of IDF:
[Row(label=0, sentence='I heard about Spark and I love Spark', Words=['i', 'heard', 'about', 'spark', 'and', 'i', 'love', 'spark'], Features(Raw)=SparseVector(1000, {240: 1.0, 286: 2.0, 673: 1.0, 756: 2.0, 891: 1.0, 956: 1.0}), Features(IDF)=SparseVector(1000, {240: 0.6931, 286: 0.5754, 673: 0.6931, 756: 0.5754, 891: 0.6931, 956: 0.6931})),
 Row(label=0, sentence='I wish Java could use case classes', Words=['i', 'wish', 'java', 'could', 'use', 'case', 'classes'], Features(Raw)=SparseVector(1000, {80: 1.0, 133: 1.0, 307: 1.0, 342: 1.0, 495: 1.0, 756: 1.0, 967: 1.0}), Features(IDF)=SparseVector(1000, {80: 0.6931, 133: 0.6931, 307: 0.6931, 342: 0.6931, 495: 0.6931, 756: 0.2877, 967: 0.6931})),
 Row(label=1, sentence='Logistic regression models are neat', Words=['logistic', 'regression', 'models', 'are', 'neat'], Features(Raw)=SparseVector(1000, {59: 1.0, 286: 1.0, 604: 1.0, 763: 1.0, 871: 1.0}), Features(IDF)=SparseVector(1000, {59: 0.6931, 286: 0.2877, 604: 0.6931, 763: 0.6931, 871: 0.6931}))]
```

## 结果解读

输出对象为 SparseVector, 这种 Vector 在保存数据的时候保存三个信息: 向量长度, 向量非零值的索引以及索引处的值。

输出的结果中, `240`, `286` 分别代表 "i", "heard" 的哈希值。

`0.6931`, `0.5754` 是 "i", "heard" 对应的 IDF 值, 出现的次数越多, 值越小。

## 完整代码

```python
#!/usr/bin/python3
# Create By GF 2023-12-29

# 本例中 Tokenizer 是用于分词的模块。
# 本例中 HashingTF().tranform() 函数把词哈希成特征向量, 返回结果是 Vectors.sparse() 类型的。
# 本例中 IDF 类用于计算给定文档集合的反文档频率, 是一个词普遍重要性的度量 (即: 一个词存在多少个文档中)。

import pprint
# --------------------------------------------------
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer

# Spark 2.0 以上版本的 spark-shell 在启动时会自动创建一个名为 spark 的 SparkSession 对象。
# 当需要手工创建时, SparkSession 可以由其伴生对象的 builder 方法创建出来。
spark = SparkSession.builder.master("local[*]").appName("spark").getOrCreate()

# 创建一个简单的 DataFrame, 每一个句子代表一个文档。
Data_Set = [[0, "I heard about Spark and I love Spark"],
            [0, "I wish Java could use case classes"],
            [1, "Logistic regression models are neat"]]

# 将数据集转化到指定列名的 DataFrame 数据框。
SDF = spark.createDataFrame(Data_Set).toDF("label", "sentence")

print("[Message] Builded Spark DataFrame:")
SDF.show()

# 特征提取 Step 1 - 创建分词器对象。
MyTokenizer = Tokenizer().setInputCol("sentence").setOutputCol("Words")
Data_for_Words = MyTokenizer.transform(SDF)

# 输出 Tokenizer 的转换效果。
print("[Message] The Effect of Tokenizer:")
Data_for_Words.select(["label", "sentence", "Words"]).show()

# 特征提取 Step 2 - 使用 HashingTF 创建词频映射, 计算某个词在文件中出现的频率。
MyHashingTF = HashingTF().setInputCol("Words").setOutputCol("Features(Raw)").setNumFeatures(1000) # -> 返回一个 Transformers。
Featurized_for_Words = MyHashingTF.transform(Data_for_Words)

# 输出 HashingTF 的转换效果。
# - HashingTF().tranform() 函数把词哈希成特征向量, 返回结果是 Vectors.sparse() 类型的。
# - 这里设置哈希表的桶数 setNumFeatures 为1000 (注意: 该值设置太小会造成哈希冲突)。
print("[Message] The Effect of HashingTF:")
Featurized_for_Words.select(["label", "Words", "Features(Raw)"]).show()

# 特征提取 Step 3 - 创建 IDF 类。
# - IDF 类: 计算给定文档集合的反文档频率, 是一个词普遍重要性的度量 (即: 一个词存在多少个文档中)。
# - 某一特定词语的 IDF, 可以由总文件数目除以包含该词语之文件的数目, 再将得到的商取对数得到。
MyIDF = IDF().setInputCol("Features(Raw)").setOutputCol("Features(IDF)") # -> 返回一个 Estimator。

IDFModel_for_Words = MyIDF.fit(Featurized_for_Words)

# 计算每一个单词对应的 IDF 度量值。
Rescaled_for_Words = IDFModel_for_Words.transform(Featurized_for_Words)

# 输出 IDF 的计算结果的 DataFrame。
print("[Message] The Calculation Result DataFrame of IDF:")
Rescaled_for_Words.select(["label", "Words", "Features(Raw)", "Features(IDF)"]).show()

# 输出 IDF 的计算结果的 RDD。
print("[Message] The Calculation Result RDD of IDF:")
pprint.pprint(Rescaled_for_Words.rdd.take(3))

# 结果解读:
# - 输出对象为 SparseVector, 这种 Vector 在保存数据的时候保存三个信息: 向量长度, 向量非零值的索引以及索引处的值。
# - 输出的结果中, 240, 286 分别代表 "i", "heard" 的哈希值。
# - 0.6931, 0.5754 是 "i", "heard" 对应的 IDF 值, 出现的次数越多, 值越小。

```

## 总结

以上就是关于 机器学习 PySpark-3.0.3文本特征提取(TF-IDF)流程 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
