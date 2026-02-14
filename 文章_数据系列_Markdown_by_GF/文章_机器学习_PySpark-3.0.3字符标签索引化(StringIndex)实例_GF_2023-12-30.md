# 文章_机器学习_PySpark-3.0.3字符标签索引化(StringIndex)实例_GF_2023-12-30

StringIndexer 是 PySpark-3.0.3 中用于将字符串列转换为数值索引的转换器。

它会根据字符串的出现频率为每个唯一字符串分配一个整数索引。

如果你的字符串类型的日期列是连续的, 频率相同, StringIndexer 会为每个不同的字符串分配一个整数索引, 而不考虑它们的实际顺序。

不考虑它们的实际顺序, 这可能导致模型在处理字符串类型的日期时不会考虑到它们之间的实际顺序关系。

## 导入 pyspark.sql 相关模块

Spark SQL 是用于结构化数据处理的 Spark 模块。它提供了一种成为 DataFrame 编程抽象, 是由 SchemaRDD 发展而来。

不同于 SchemaRDD 直接继承 RDD, DataFrame 自己实现了 RDD 的绝大多数功能。

```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
```

## 创建 SparkSession 对象

Spark 2.0 以上版本的 spark-shell 在启动时会自动创建一个名为 spark 的 SparkSession 对象。

当需要手工创建时, SparkSession 可以由其伴生对象的 builder 方法创建出来。

```python
spark = SparkSession.builder.master("local[*]").appName("spark").getOrCreate()
```

## 使用 Spark 构建 DataFrame 数据 (行作为元组, 列名作为列表)

当数据量较小时, 可以使用该方法手工构建 DataFrame 数据。

构建数据行 Rows (元组的列表):

```python
Data_Rows = [("Alice", 25, "Female"),
             ("Bob", 30, "Male"),
             ("Charlie", 35, "Male")]
```

构建数据列名 Cols (字符串的列表):

```python
Data_Cols = ["Name", "Age", "Gender"]
```

生成 DataFrame 数据框:

```python
SDF = spark.createDataFrame(Data_Rows, Data_Cols)
```

输出 DataFrame 数据框:

```python
print("[Message] Builded Spark DataFrame:")
SDF.show()
```

输出:

```txt
[Message] Builded Spark DataFrame:
+-------+---+------+
|   Name|Age|Gender|
+-------+---+------+
|  Alice| 25|Female|
|    Bob| 30|  Male|
|Charlie| 35|  Male|
+-------+---+------+
```

## 使用 pyspark.ml 的字符标签索引化 (StringIndexer) 模块

**使用 pyspark.ml 的字符标签索引化 (StringIndexer) 模块转换 Name 列**:

```python
# 使用 StringIndexer 转换 Name 列。
MyStringIndexer = StringIndexer(inputCol="Name", outputCol="Name(Idx)")
# 拟合并转换数据。
IndexedSDF = MyStringIndexer.fit(SDF).transform(SDF)

# 输出 StringIndexer 的转换效果。
print("[Message] The Effect of StringIndexer on \"Name\":")
IndexedSDF.show()
```

输出:

```txt
[Message] The Effect of StringIndexer on "Name":
+-------+---+------+---------+
|   Name|Age|Gender|Name(Idx)|
+-------+---+------+---------+
|  Alice| 25|Female|      0.0|
|    Bob| 30|  Male|      1.0|
|Charlie| 35|  Male|      2.0|
+-------+---+------+---------+
```

**使用 pyspark.ml 的字符标签索引化 (StringIndexer) 模块转换 Name 列和 Gender 列**:

```python
# 使用 StringIndexer 转换 Name, Gender 列。
MyStringIndexer = StringIndexer(inputCols=["Name", "Gender"], outputCols=["Name(Idx)", "Gender(Idx)"])
# 拟合并转换数据。
IndexedSDF = MyStringIndexer.fit(SDF).transform(SDF)

# 输出 StringIndexer 的转换效果。
print("[Message] The Effect of StringIndexer on \"Name\" and \"Gender\":")
IndexedSDF.select(["Name", "Name(Idx)", "Gender", "Gender(Idx)"]).show()
```

输出:

```txt
[Message] The Effect of StringIndexer on "Name" and "Gender":
+-------+---------+------+-----------+
|   Name|Name(Idx)|Gender|Gender(Idx)|
+-------+---------+------+-----------+
|  Alice|      0.0|Female|        1.0|
|    Bob|      1.0|  Male|        0.0|
|Charlie|      2.0|  Male|        0.0|
+-------+---------+------+-----------+
```

## 完整代码

```python
#!/usr/bin/python3
# Create By GF 2023-12-30

# 请确保在使用 StringIndexer 之前, 将你的数据集转换为 PySpark 的 DataFrame。
# 在实际应用中, 你可能需要对多个字符串列进行索引, 并使用 VectorAssembler 将它们组合成一个特征向量, 以供机器学习模型使用。

from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer

# Spark 2.0 以上版本的 spark-shell 在启动时会自动创建一个名为 spark 的 SparkSession 对象。
# 当需要手工创建时, SparkSession 可以由其伴生对象的 builder 方法创建出来。
spark = SparkSession.builder.master("local[*]").appName("spark").getOrCreate()

# 使用 Spark 构建 DataFrame 数据 (行作为元组, 列名作为列表)。
# 构建数据行 Rows (元组的列表)。
Data_Rows = [("Alice", 25, "Female"),
             ("Bob", 30, "Male"),
             ("Charlie", 35, "Male")]

# 构建数据列名 Cols (字符串的列表)。
Data_Cols = ["Name", "Age", "Gender"]

# 生成 DataFrame 数据框。
SDF = spark.createDataFrame(Data_Rows, Data_Cols)

print("[Message] Builded Spark DataFrame:")
SDF.show()

# 使用 StringIndexer 转换 Name 列。
MyStringIndexer = StringIndexer(inputCol="Name", outputCol="Name(Idx)")
# 拟合并转换数据。
IndexedSDF = MyStringIndexer.fit(SDF).transform(SDF)

# 输出 StringIndexer 的转换效果。
print("[Message] The Effect of StringIndexer on \"Name\":")
IndexedSDF.show()

# 使用 StringIndexer 转换 Name, Gender 列。
MyStringIndexer = StringIndexer(inputCols=["Name", "Gender"], outputCols=["Name(Idx)", "Gender(Idx)"])
# 拟合并转换数据。
IndexedSDF = MyStringIndexer.fit(SDF).transform(SDF)

# 输出 StringIndexer 的转换效果。
print("[Message] The Effect of StringIndexer on \"Name\" and \"Gender\":")
IndexedSDF.select(["Name", "Name(Idx)", "Gender", "Gender(Idx)"]).show()

```

## 其它

请确保在使用 StringIndexer 之前, 将你的数据集转换为 PySpark 的 DataFrame。

在实际应用中, 你可能需要对多个字符串列进行索引, 并使用 VectorAssembler 将它们组合成一个特征向量, 以供机器学习模型使用。

## 总结

以上就是关于 机器学习 PySpark-3.0.3字符标签索引化(StringIndex)实例 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
