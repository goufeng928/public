# 文章_机器学习_PySpark-3.0.3随机森林回归(RandomForestRegressor)实例_GF_2023-12-30

随机森林回归 (Random Forest Regression):

**任务类型**: 随机森林回归主要用于回归任务。在回归任务中, 算法试图预测一个连续的数值输出, 而不是一个离散的类别。

**输出**: 随机森林回归的输出是一个连续的数值, 表示输入数据的预测结果。

**算法原理**: 随机森林回归同样基于决策树, 但在回归任务中, 每个决策树的输出是一个实数值。最终的预测结果是多个决策树输出的平均值或加权平均值。

在 PySpark-3.x.x 中构建随机森林回归主要使用 pyspark.ml 模块中的 RandomForestRegressor。

下面是一个简单的示例, 演示如何使用 PySpark-3.x.x 构建和训练随机森林回归模型。

## 实例数据

本实例是于 2023年12月30日 截取了 "Iris_Dataset (鸢尾花数据集)" 中的120条样本数据。

**字段说明**: SepalLength(花萼长度), SepalWidth(花萼宽度), PetalLength(花瓣长度), PetalWidth(花瓣宽度), Species(品种).

**品种说明**: Setosa(山鸢尾), Versicolor(变色鸢尾), Virginical(维吉尼亚鸢尾).

Iris_Dataset_120_2023-12-30.csv

```csv
SepalLength,SepalWidth,PetalLength,PetalWidth,Species
6.4,2.8,5.6,2.2,Virginical
5.0,2.3,3.3,1.0,Versicolor
4.9,2.5,4.5,1.7,Virginical
4.9,3.1,1.5,0.1,Setosa
5.7,3.8,1.7,0.3,Setosa
4.4,3.2,1.3,0.2,Setosa
5.4,3.4,1.5,0.4,Setosa
6.9,3.1,5.1,2.3,Virginical
6.7,3.1,4.4,1.4,Versicolor
5.1,3.7,1.5,0.4,Setosa
5.2,2.7,3.9,1.4,Versicolor
6.9,3.1,4.9,1.5,Versicolor
5.8,4.0,1.2,0.2,Setosa
5.4,3.9,1.7,0.4,Setosa
7.7,3.8,6.7,2.2,Virginical
6.3,3.3,4.7,1.6,Versicolor
6.8,3.2,5.9,2.3,Virginical
7.6,3.0,6.6,2.1,Virginical
6.4,3.2,5.3,2.3,Virginical
5.7,4.4,1.5,0.4,Setosa
6.7,3.3,5.7,2.1,Virginical
6.4,2.8,5.6,2.1,Virginical
5.4,3.9,1.3,0.4,Setosa
6.1,2.6,5.6,1.4,Virginical
7.2,3.0,5.8,1.6,Virginical
5.2,3.5,1.5,0.2,Setosa
5.8,2.6,4.0,1.2,Versicolor
5.9,3.0,5.1,1.8,Virginical
5.4,3.0,4.5,1.5,Versicolor
6.7,3.0,5.0,1.7,Versicolor
6.3,2.3,4.4,1.3,Versicolor
5.1,2.5,3.0,1.1,Versicolor
6.4,3.2,4.5,1.5,Versicolor
6.8,3.0,5.5,2.1,Virginical
6.2,2.8,4.8,1.8,Virginical
6.9,3.2,5.7,2.3,Virginical
6.5,3.2,5.1,2.0,Virginical
5.8,2.8,5.1,2.4,Virginical
5.1,3.8,1.5,0.3,Setosa
4.8,3.0,1.4,0.3,Setosa
7.9,3.8,6.4,2.0,Virginical
5.8,2.7,5.1,1.9,Virginical
6.7,3.0,5.2,2.3,Virginical
5.1,3.8,1.9,0.4,Setosa
4.7,3.2,1.6,0.2,Setosa
6.0,2.2,5.0,1.5,Virginical
4.8,3.4,1.6,0.2,Setosa
7.7,2.6,6.9,2.3,Virginical
4.6,3.6,1.0,0.2,Setosa
7.2,3.2,6.0,1.8,Virginical
5.0,3.3,1.4,0.2,Setosa
6.6,3.0,4.4,1.4,Versicolor
6.1,2.8,4.0,1.3,Versicolor
5.0,3.2,1.2,0.2,Setosa
7.0,3.2,4.7,1.4,Versicolor
6.0,3.0,4.8,1.8,Virginical
7.4,2.8,6.1,1.9,Virginical
5.8,2.7,5.1,1.9,Virginical
6.2,3.4,5.4,2.3,Virginical
5.0,2.0,3.5,1.0,Versicolor
5.6,2.5,3.9,1.1,Versicolor
6.7,3.1,5.6,2.4,Virginical
6.3,2.5,5.0,1.9,Virginical
6.4,3.1,5.5,1.8,Virginical
6.2,2.2,4.5,1.5,Versicolor
7.3,2.9,6.3,1.8,Virginical
4.4,3.0,1.3,0.2,Setosa
7.2,3.6,6.1,2.5,Virginical
6.5,3.0,5.5,1.8,Virginical
5.0,3.4,1.5,0.2,Setosa
4.7,3.2,1.3,0.2,Setosa
6.6,2.9,4.6,1.3,Versicolor
5.5,3.5,1.3,0.2,Setosa
7.7,3.0,6.1,2.3,Virginical
6.1,3.0,4.9,1.8,Virginical
4.9,3.1,1.5,0.1,Setosa
5.5,2.4,3.8,1.1,Versicolor
5.7,2.9,4.2,1.3,Versicolor
6.0,2.9,4.5,1.5,Versicolor
6.4,2.7,5.3,1.9,Virginical
5.4,3.7,1.5,0.2,Setosa
6.1,2.9,4.7,1.4,Versicolor
6.5,2.8,4.6,1.5,Versicolor
5.6,2.7,4.2,1.3,Versicolor
6.3,3.4,5.6,2.4,Virginical
4.9,3.1,1.5,0.1,Setosa
6.8,2.8,4.8,1.4,Versicolor
5.7,2.8,4.5,1.3,Versicolor
6.0,2.7,5.1,1.6,Versicolor
5.0,3.5,1.3,0.3,Setosa
6.5,3.0,5.2,2.0,Virginical
6.1,2.8,4.7,1.2,Versicolor
5.1,3.5,1.4,0.3,Setosa
4.6,3.1,1.5,0.2,Setosa
6.5,3.0,5.8,2.2,Virginical
4.6,3.4,1.4,0.3,Setosa
4.6,3.2,1.4,0.2,Setosa
7.7,2.8,6.7,2.0,Virginical
5.9,3.2,4.8,1.8,Versicolor
5.1,3.8,1.6,0.2,Setosa
4.9,3.0,1.4,0.2,Setosa
4.9,2.4,3.3,1.0,Versicolor
4.5,2.3,1.3,0.3,Setosa
5.8,2.7,4.1,1.0,Versicolor
5.0,3.4,1.6,0.4,Setosa
5.2,3.4,1.4,0.2,Setosa
5.3,3.7,1.5,0.2,Setosa
5.0,3.6,1.4,0.2,Setosa
5.6,2.9,3.6,1.3,Versicolor
4.8,3.1,1.6,0.2,Setosa
6.3,2.7,4.9,1.8,Virginical
5.7,2.8,4.1,1.3,Versicolor
5.0,3.0,1.6,0.2,Setosa
6.3,3.3,6.0,2.5,Virginical
5.0,3.5,1.6,0.6,Setosa
5.5,2.6,4.4,1.2,Versicolor
5.7,3.0,4.2,1.2,Versicolor
4.4,2.9,1.4,0.2,Setosa
4.8,3.0,1.4,0.1,Setosa
5.5,2.4,3.7,1.0,Versicolor

```

## 探索思路

这里只是简单示例, 目的在于熟悉 Spark 中的随机森林回归使用方法。

**目标**:

通过 `SepalLength(花萼长度)`, `SepalWidth(花萼宽度)`, `PetalLength(花瓣长度)`, `PetalWidth(花瓣宽度)` 预测 `Iris(鸢尾花)` 的 `Species(品种)`。

**标签**:

由于 `Iris(鸢尾花)` 的 `Species(品种)` 是 `字符串(String)` 的形式, 本例将使用 `pyspark.ml` 的 `StringIndexer` 模块将 `Iris(鸢尾花)` 的 `Species(品种)` 索引化。

## 导入 pyspark.sql 相关模块

Spark SQL 是用于结构化数据处理的 Spark 模块。它提供了一种成为 DataFrame 编程抽象, 是由 SchemaRDD 发展而来。

不同于 SchemaRDD 直接继承 RDD, DataFrame 自己实现了 RDD 的绝大多数功能。

```python
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, DoubleType
```

## 导入 pyspark.ml 相关模块

Spark 在核心数据抽象 RDD 的基础上,  支持 4 大组件,  其中机器学习占其一。

进一步的, Spark 中实际上支持两个机器学习模块, MLlib 和 ML, 区别在于前者主要是基于 RDD 数据结构, 当前处于维护状态; 而后者则是 DataFrame 数据结构, 支持更多的算法, 后续将以此为主进行迭代。

所以, 在实际应用中优先使用 ML 子模块。

Spark 的 ML 库与 Python 中的另一大机器学习库 Sklearn 的关系是: Spark 的 ML 库支持大部分机器学习算法和接口功能, 虽远不如 Sklearn 功能全面, 但主要面向分布式训练, 针对大数据。

而 Sklearn 是单点机器学习算法库, 支持几乎所有主流的机器学习算法, 从样例数据, 特征选择, 模型选择和验证, 基础学习算法和集成学习算法, 提供了机器学习一站式解决方案, 但仅支持并行而不支持分布式。

```python
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
```

## 创建 SparkSession 对象

Spark 2.0 以上版本的 spark-shell 在启动时会自动创建一个名为 spark 的 SparkSession 对象。

当需要手工创建时, SparkSession 可以由其伴生对象的 builder 方法创建出来。

```python
spark = SparkSession.builder.master("local[*]").appName("spark").getOrCreate()
```

## 使用 Spark 构建 DataFrame 数据 (Optional)

当数据量较小时, 可以使用该方法手工构建 DataFrame 数据。

构建数据行 Row (以前 5 行为例):

```python
Row(SepalLength=6.4, SepalWidth=2.8, PetalLength=5.6, PetalWidth=2.2, Species="Virginical")
Row(SepalLength=5.0, SepalWidth=2.3, PetalLength=3.3, PetalWidth=1.0, Species="Versicolor")
Row(SepalLength=4.9, SepalWidth=2.5, PetalLength=4.5, PetalWidth=1.7, Species="Virginical")
Row(SepalLength=4.9, SepalWidth=3.1, PetalLength=1.5, PetalWidth=0.1, Species="Setosa")
Row(SepalLength=5.7, SepalWidth=3.8, PetalLength=1.7, PetalWidth=0.3, Species="Setosa")
```

将构建好的数据行 Row 加入列表 (以前 5 行为例):

```python
Data_Rows = [
    Row(SepalLength=6.4, SepalWidth=2.8, PetalLength=5.6, PetalWidth=2.2, Species="Virginical"),
    Row(SepalLength=5.0, SepalWidth=2.3, PetalLength=3.3, PetalWidth=1.0, Species="Versicolor"),
    Row(SepalLength=4.9, SepalWidth=2.5, PetalLength=4.5, PetalWidth=1.7, Species="Virginical"),
    Row(SepalLength=4.9, SepalWidth=3.1, PetalLength=1.5, PetalWidth=0.1, Species="Setosa"),
    Row(SepalLength=5.7, SepalWidth=3.8, PetalLength=1.7, PetalWidth=0.3, Species="Setosa")
]
```

生成 DataFrame 数据框 (以前 5 行为例):

```python
SDF = spark.createDataFrame(data=Data_Rows)
```

输出 DataFrame 数据框 (以前 5 行为例):

```python
print("[Message] Builded Spark DataFrame:")
SDF.show(3)
```

输出:

```txt
[Message] Builded Spark DataFrame:
+-----------+----------+-----------+----------+----------+
|SepalLength|SepalWidth|PetalLength|PetalWidth|   Species|
+-----------+----------+-----------+----------+----------+
|        6.4|       2.8|        5.6|       2.2|Virginical|
|        5.0|       2.3|        3.3|       1.0|Versicolor|
|        4.9|       2.5|        4.5|       1.7|Virginical|
|        4.9|       3.1|        1.5|       0.1|    Setosa|
|        5.7|       3.8|        1.7|       0.3|    Setosa|
+-----------+----------+-----------+----------+----------+
only showing top 3 rows
```

## 使用 Spark 读取 CSV 数据

调用 SparkSession 的 .read 方法读取 CSV 数据:

其中 .option 是读取文件时的选项, 左边是 "键(Key)", 右边是 "值(Value)", 例如 .option("header", "true") 与 {header = "true"} 类同。

```python
SDF = spark.read.option("header", "true").option("encoding", "utf-8").csv("file:///D:\\Iris_Dataset_120_2023-12-30.csv")
```

输出 DataFrame 数据框:

```python
print("[Message] Readed CSV File: D:\\Iris_Dataset_120_2023-12-30.csv")
SDF.show()
```

输出:

```txt
[Message] Readed CSV File: D:\Iris_Dataset_120_2023-12-30.csv
+-----------+----------+-----------+----------+----------+
|SepalLength|SepalWidth|PetalLength|PetalWidth|   Species|
+-----------+----------+-----------+----------+----------+
|        6.4|       2.8|        5.6|       2.2|Virginical|
|        5.0|       2.3|        3.3|       1.0|Versicolor|
|        4.9|       2.5|        4.5|       1.7|Virginical|
|        4.9|       3.1|        1.5|       0.1|    Setosa|
|        5.7|       3.8|        1.7|       0.3|    Setosa|
|        4.4|       3.2|        1.3|       0.2|    Setosa|
|        5.4|       3.4|        1.5|       0.4|    Setosa|
|        6.9|       3.1|        5.1|       2.3|Virginical|
|        6.7|       3.1|        4.4|       1.4|Versicolor|
|        5.1|       3.7|        1.5|       0.4|    Setosa|
|        5.2|       2.7|        3.9|       1.4|Versicolor|
|        6.9|       3.1|        4.9|       1.5|Versicolor|
|        5.8|       4.0|        1.2|       0.2|    Setosa|
|        5.4|       3.9|        1.7|       0.4|    Setosa|
|        7.7|       3.8|        6.7|       2.2|Virginical|
|        6.3|       3.3|        4.7|       1.6|Versicolor|
|        6.8|       3.2|        5.9|       2.3|Virginical|
|        7.6|       3.0|        6.6|       2.1|Virginical|
|        6.4|       3.2|        5.3|       2.3|Virginical|
|        5.7|       4.4|        1.5|       0.4|    Setosa|
+-----------+----------+-----------+----------+----------+
only showing top 20 rows
```

## 转换 Spark 中 DateFrame 各列数据类型

通常情况下, 为了避免计算出现数据类型的错误, 都需要重新转换一下数据类型。

```python
# 转换 Spark 中 DateFrame 数据类型。
SDF = SDF.withColumn("SepalLength", col("SepalLength").cast(DoubleType()))
SDF = SDF.withColumn("SepalWidth",  col("SepalWidth").cast(DoubleType()))
SDF = SDF.withColumn("PetalLength", col("PetalLength").cast(DoubleType()))
SDF = SDF.withColumn("PetalWidth",  col("PetalWidth").cast(DoubleType()))
SDF = SDF.withColumn("Species",     col("Species").cast(StringType()))

# 输出 Spark 中 DataFrame 字段和数据类型。
print("[Message] Changed Spark DataFrame Data Type:")
SDF.printSchema()
```

输出:

```txt
[Message] Changed Spark DataFrame Data Type:
root
 |-- SepalLength: double (nullable = true)
 |-- SepalWidth: double (nullable = true)
 |-- PetalLength: double (nullable = true)
 |-- PetalWidth: double (nullable = true)
 |-- Species: string (nullable = true)
```

## 字符串索引化 (StringIndexer) 转换 Species 列

StringIndexer (字符串-索引变换) 是一个估计器, 是将字符串列编码为标签索引列。索引位于 `[0, numLabels)`, 按标签频率排序, 频率最高的排 0, 依次类推, 因此最常见的标签获取索引是 0。

```python
# 使用 StringIndexer 转换 Species 列。
MyStringIndexer = StringIndexer(inputCol="Species", outputCol="SpeciesIdx")
# 拟合并转换数据。
IndexedSDF = MyStringIndexer.fit(SDF).transform(SDF)

# 输出 StringIndexer 的转换效果。
print("[Message] The Effect of StringIndexer:")
IndexedSDF.show()
```

输出:

```txt
[Message] The Effect of StringIndexer:
+-----------+----------+-----------+----------+----------+----------+
|SepalLength|SepalWidth|PetalLength|PetalWidth|   Species|SpeciesIdx|
+-----------+----------+-----------+----------+----------+----------+
|        6.4|       2.8|        5.6|       2.2|Virginical|       1.0|
|        5.0|       2.3|        3.3|       1.0|Versicolor|       2.0|
|        4.9|       2.5|        4.5|       1.7|Virginical|       1.0|
|        4.9|       3.1|        1.5|       0.1|    Setosa|       0.0|
|        5.7|       3.8|        1.7|       0.3|    Setosa|       0.0|
|        4.4|       3.2|        1.3|       0.2|    Setosa|       0.0|
|        5.4|       3.4|        1.5|       0.4|    Setosa|       0.0|
|        6.9|       3.1|        5.1|       2.3|Virginical|       1.0|
|        6.7|       3.1|        4.4|       1.4|Versicolor|       2.0|
|        5.1|       3.7|        1.5|       0.4|    Setosa|       0.0|
|        5.2|       2.7|        3.9|       1.4|Versicolor|       2.0|
|        6.9|       3.1|        4.9|       1.5|Versicolor|       2.0|
|        5.8|       4.0|        1.2|       0.2|    Setosa|       0.0|
|        5.4|       3.9|        1.7|       0.4|    Setosa|       0.0|
|        7.7|       3.8|        6.7|       2.2|Virginical|       1.0|
|        6.3|       3.3|        4.7|       1.6|Versicolor|       2.0|
|        6.8|       3.2|        5.9|       2.3|Virginical|       1.0|
|        7.6|       3.0|        6.6|       2.1|Virginical|       1.0|
|        6.4|       3.2|        5.3|       2.3|Virginical|       1.0|
|        5.7|       4.4|        1.5|       0.4|    Setosa|       0.0|
+-----------+----------+-----------+----------+----------+----------+
only showing top 20 rows
```

## 提取 标签(Label)列 和 特征向量(Features)列

在创建特征向量(Features)列时, 将会用到 VectorAssembler 模块, VectorAssembler 将多个特征合并为一个特征向量。

**提取 标签(Label) 列**:

```python
# 将 SpeciesIdx 列复制为 Label 列。
NewSDF = IndexedSDF.withColumn("Label", col("SpeciesIdx"))
```

**创建 特征向量(Features) 列**:

```python
# VectorAssembler 将多个特征合并为一个特征向量。
FeaColsName:list = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]
MyAssembler = VectorAssembler(inputCols=FeaColsName, outputCol="Features")

# 创建 特征向量(Features) 列: 拟合数据 (可选, 如果在模型训练时使用 Pipeline, 则无需在此步骤拟合数据, 当然也就无法在此步骤预览数据)。
AssembledSDF = MyAssembler.transform(NewSDF)
```

**输出预览**:

```python
print("[Message] Assembled Label and Features for RandomForestRegressor:")
AssembledSDF.show()
```

预览:

```txt
[Message] Assembled for RandomForestRegressor:
+-----------+----------+-----------+----------+----------+----------+-----+-----------------+
|SepalLength|SepalWidth|PetalLength|PetalWidth|   Species|SpeciesIdx|Label|         Features|
+-----------+----------+-----------+----------+----------+----------+-----+-----------------+
|        6.4|       2.8|        5.6|       2.2|Virginical|       1.0|  1.0|[6.4,2.8,5.6,2.2]|
|        5.0|       2.3|        3.3|       1.0|Versicolor|       2.0|  2.0|[5.0,2.3,3.3,1.0]|
|        4.9|       2.5|        4.5|       1.7|Virginical|       1.0|  1.0|[4.9,2.5,4.5,1.7]|
|        4.9|       3.1|        1.5|       0.1|    Setosa|       0.0|  0.0|[4.9,3.1,1.5,0.1]|
|        5.7|       3.8|        1.7|       0.3|    Setosa|       0.0|  0.0|[5.7,3.8,1.7,0.3]|
|        4.4|       3.2|        1.3|       0.2|    Setosa|       0.0|  0.0|[4.4,3.2,1.3,0.2]|
|        5.4|       3.4|        1.5|       0.4|    Setosa|       0.0|  0.0|[5.4,3.4,1.5,0.4]|
|        6.9|       3.1|        5.1|       2.3|Virginical|       1.0|  1.0|[6.9,3.1,5.1,2.3]|
|        6.7|       3.1|        4.4|       1.4|Versicolor|       2.0|  2.0|[6.7,3.1,4.4,1.4]|
|        5.1|       3.7|        1.5|       0.4|    Setosa|       0.0|  0.0|[5.1,3.7,1.5,0.4]|
|        5.2|       2.7|        3.9|       1.4|Versicolor|       2.0|  2.0|[5.2,2.7,3.9,1.4]|
|        6.9|       3.1|        4.9|       1.5|Versicolor|       2.0|  2.0|[6.9,3.1,4.9,1.5]|
|        5.8|       4.0|        1.2|       0.2|    Setosa|       0.0|  0.0|[5.8,4.0,1.2,0.2]|
|        5.4|       3.9|        1.7|       0.4|    Setosa|       0.0|  0.0|[5.4,3.9,1.7,0.4]|
|        7.7|       3.8|        6.7|       2.2|Virginical|       1.0|  1.0|[7.7,3.8,6.7,2.2]|
|        6.3|       3.3|        4.7|       1.6|Versicolor|       2.0|  2.0|[6.3,3.3,4.7,1.6]|
|        6.8|       3.2|        5.9|       2.3|Virginical|       1.0|  1.0|[6.8,3.2,5.9,2.3]|
|        7.6|       3.0|        6.6|       2.1|Virginical|       1.0|  1.0|[7.6,3.0,6.6,2.1]|
|        6.4|       3.2|        5.3|       2.3|Virginical|       1.0|  1.0|[6.4,3.2,5.3,2.3]|
|        5.7|       4.4|        1.5|       0.4|    Setosa|       0.0|  0.0|[5.7,4.4,1.5,0.4]|
+-----------+----------+-----------+----------+----------+----------+-----+-----------------+
only showing top 20 rows
```

## 训练 随机森林回归(RandomForestRegressor) 模型

**将数据集划分为 "训练集" 和 "测试集"**:

```python
(TrainingData, TestData) = AssembledSDF.randomSplit([0.8, 0.2], seed=42)
```

**创建 随机森林回归(RandomForestRegressor)**:

```python
RFR = RandomForestRegressor(featuresCol="Features", labelCol="Label")
```

**创建 Pipeline (可选)**:

```python
# 创建 Pipeline, 将特征向量转换和随机森林回归模型组合在一起
# 注意: 如果要使用 Pipeline, 则在创建 特征向量(Features)列 的时候不需要拟合数据, 否则会报 "Output column Features already exists." 的错误。
MyPipeline = Pipeline(stages=[MyAssembler, RFR])
```

**训练 随机森林回归(RandomForestRegressor) 模型**:

如果在创建 特征向量(Features)列 的时候已经拟合数据:

```python
# 训练模型 (普通模式)。
Model = RFR.fit(TrainingData)
```

如果在创建 特征向量(Features)列 的时候没有拟合数据:

```python
# 训练模型 (Pipeline 模式)。
Model = MyPipeline.fit(TrainingData)
```

## 使用 随机森林回归(RandomForestRegressor) 模型预测数据

```python
# 在测试集上进行预测。
Predictions = Model.transform(TestData)

print("[Message] Prediction Results on The Test Data Set for RandomForestRegressor:")
Predictions.show()
```

输出:

```txt
[Message] Prediction Results on The Test Data Set for RandomForestRegressor:
+-----------+----------+-----------+----------+----------+----------+-----+-----------------+------------------+
|SepalLength|SepalWidth|PetalLength|PetalWidth|   Species|SpeciesIdx|Label|         Features|        prediction|
+-----------+----------+-----------+----------+----------+----------+-----+-----------------+------------------+
|        4.4|       3.2|        1.3|       0.2|    Setosa|       0.0|  0.0|[4.4,3.2,1.3,0.2]|               0.0|
|        4.6|       3.4|        1.4|       0.3|    Setosa|       0.0|  0.0|[4.6,3.4,1.4,0.3]|               0.0|
|        4.7|       3.2|        1.3|       0.2|    Setosa|       0.0|  0.0|[4.7,3.2,1.3,0.2]|               0.0|
|        4.8|       3.4|        1.6|       0.2|    Setosa|       0.0|  0.0|[4.8,3.4,1.6,0.2]|               0.0|
|        4.9|       3.1|        1.5|       0.1|    Setosa|       0.0|  0.0|[4.9,3.1,1.5,0.1]|               0.0|
|        5.0|       3.2|        1.2|       0.2|    Setosa|       0.0|  0.0|[5.0,3.2,1.2,0.2]|               0.0|
|        5.0|       3.6|        1.4|       0.2|    Setosa|       0.0|  0.0|[5.0,3.6,1.4,0.2]|               0.0|
|        5.1|       3.8|        1.9|       0.4|    Setosa|       0.0|  0.0|[5.1,3.8,1.9,0.4]|               0.2|
|        5.5|       2.4|        3.7|       1.0|Versicolor|       2.0|  2.0|[5.5,2.4,3.7,1.0]|               2.0|
|        5.5|       2.4|        3.8|       1.1|Versicolor|       2.0|  2.0|[5.5,2.4,3.8,1.1]|               2.0|
|        5.5|       2.6|        4.4|       1.2|Versicolor|       2.0|  2.0|[5.5,2.6,4.4,1.2]|               2.0|
|        5.6|       2.5|        3.9|       1.1|Versicolor|       2.0|  2.0|[5.6,2.5,3.9,1.1]|               2.0|
|        5.6|       2.9|        3.6|       1.3|Versicolor|       2.0|  2.0|[5.6,2.9,3.6,1.3]|               2.0|
|        5.7|       3.0|        4.2|       1.2|Versicolor|       2.0|  2.0|[5.7,3.0,4.2,1.2]|               2.0|
|        5.8|       2.8|        5.1|       2.4|Virginical|       1.0|  1.0|[5.8,2.8,5.1,2.4]|               1.0|
|        6.0|       3.0|        4.8|       1.8|Virginical|       1.0|  1.0|[6.0,3.0,4.8,1.8]|1.3833333333333333|
|        6.2|       3.4|        5.4|       2.3|Virginical|       1.0|  1.0|[6.2,3.4,5.4,2.3]|               1.0|
|        6.7|       3.1|        5.6|       2.4|Virginical|       1.0|  1.0|[6.7,3.1,5.6,2.4]|               1.0|
|        7.3|       2.9|        6.3|       1.8|Virginical|       1.0|  1.0|[7.3,2.9,6.3,1.8]|               1.0|
|        7.7|       2.8|        6.7|       2.0|Virginical|       1.0|  1.0|[7.7,2.8,6.7,2.0]|               1.0|
+-----------+----------+-----------+----------+----------+----------+-----+-----------------+------------------+
only showing top 20 rows
```

## 使用 RegressionEvaluator 评估模型性能

```python
# 使用 RegressionEvaluator 评估模型性能。
MyEvaluator = RegressionEvaluator(labelCol="Label", predictionCol="prediction", metricName="mse")
mse = MyEvaluator.evaluate(Predictions)

print("均方误差(MSE): %f" % mse)
```

输出:

```txt
均方误差(MSE): 0.008497
```

## 完整代码

```python
#!/usr/bin/python3
# Create By GF 2023-12-30

# 请确保你的 DataFrame 包含一个名为 Label 的列, 这是 Species(品种) 的列。
# 如果 label 是字符串类型的分类特征, 你可能需要使用 StringIndexer 进行索引。

from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, DoubleType
# --------------------------------------------------
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

# Spark 2.0 以上版本的 spark-shell 在启动时会自动创建一个名为 spark 的 SparkSession 对象。
# 当需要手工创建时, SparkSession 可以由其伴生对象的 builder 方法创建出来。
spark = SparkSession.builder.master("local[*]").appName("spark").getOrCreate()

# 调用 SparkSession 的 .read 方法读取 CSV 数据:
# 其中 .option 是读取文件时的选项, 左边是 "键(Key)", 右边是 "值(Value)", 例如 .option("header", "true") 与 {header = "true"} 类同。
SDF = spark.read.option("header", "true").option("encoding", "utf-8").csv("file:///D:\\Iris_Dataset_120_2023-12-30.csv")

print("[Message] Readed CSV File: D:\\Iris_Dataset_120_2023-12-30.csv")
SDF.show()

# 转换 Spark 中 DateFrame 数据类型。
SDF = SDF.withColumn("SepalLength", col("SepalLength").cast(DoubleType()))
SDF = SDF.withColumn("SepalWidth",  col("SepalWidth").cast(DoubleType()))
SDF = SDF.withColumn("PetalLength", col("PetalLength").cast(DoubleType()))
SDF = SDF.withColumn("PetalWidth",  col("PetalWidth").cast(DoubleType()))
SDF = SDF.withColumn("Species",     col("Species").cast(StringType()))

# 输出 Spark 中 DataFrame 字段和数据类型。
print("[Message] Changed Spark DataFrame Data Type:")
SDF.printSchema()

# 使用 StringIndexer 转换 Species 列。
MyStringIndexer = StringIndexer(inputCol="Species", outputCol="SpeciesIdx")
# 拟合并转换数据。
IndexedSDF = MyStringIndexer.fit(SDF).transform(SDF)

# 输出 StringIndexer 的转换效果。
print("[Message] The Effect of StringIndexer:")
IndexedSDF.show()

# 将 SpeciesIdx 列复制为 Label 列。
NewSDF = IndexedSDF.withColumn("Label", col("SpeciesIdx"))

# VectorAssembler 将多个特征合并为一个特征向量。
FeaColsName:list = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]
MyAssembler = VectorAssembler(inputCols=FeaColsName, outputCol="Features")

# 创建 特征向量(Features) 列: 拟合数据 (可选, 如果在模型训练时使用 Pipeline, 则无需在此步骤拟合数据, 当然也就无法在此步骤预览数据)。
AssembledSDF = MyAssembler.transform(NewSDF)

print("[Message] Assembled Label and Features for RandomForestRegressor:")
AssembledSDF.show()

# 将数据集划分为 "训练集" 和 "测试集"。
(TrainingData, TestData) = AssembledSDF.randomSplit([0.8, 0.2], seed=42)

# 创建 随机森林回归(RandomForestRegressor)。
RFR = RandomForestRegressor(featuresCol="Features", labelCol="Label")

# 创建 Pipeline (可选): 将特征向量转换和随机森林回归模型组合在一起
# 注意: 如果要使用 Pipeline, 则在创建 特征向量(Features)列 的时候不需要拟合数据, 否则会报 "Output column Features already exists." 的错误。
#MyPipeline = Pipeline(stages=[MyAssembler, RFR])

# 训练模型 (普通模式)。
Model = RFR.fit(TrainingData)

# 训练模型 (Pipeline 模式)。
#Model = MyPipeline.fit(TrainingData)

# 在测试集上进行预测。
Predictions = Model.transform(TestData)

print("[Message] Prediction Results on The Test Data Set for RandomForestRegressor:")
Predictions.show()

# 使用 RegressionEvaluator 评估模型性能。
MyEvaluator = RegressionEvaluator(labelCol="Label", predictionCol="prediction", metricName="mse")
mse = MyEvaluator.evaluate(Predictions)

print("均方误差(MSE): %f" % mse)

```

## 其它

请确保你的 DataFrame 包含一个名为 Label 的列, 这是 Species(品种) 的列。

如果 label 是字符串类型的分类特征, 你可能需要使用 StringIndexer 进行索引。

## 总结

以上就是关于 机器学习 PySpark-3.0.3随机森林回归(RandomForestRegressor)实例 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
