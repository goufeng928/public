# 文章_大数据分析_PySpark中类Pandas的df.loc操作(行列定位)_GF_2024-01-06

在 PySpark 3.0.3 中, 虽然没有直接类似于 Pandas 中 df.loc 的函数, 但可以通过使用 PySpark 的 select 和 filter 操作来达到类似的功能。

select 用于选择列, 而 filter 用于按条件筛选行。

下面是一个简单的例子, 演示如何使用 PySpark 实现类似于 Pandas 中 df.loc 的功能。

## 导入 pyspark.sql 相关模块

Spark SQL 是用于结构化数据处理的 Spark 模块。它提供了一种成为 DataFrame 编程抽象, 是由 SchemaRDD 发展而来。

不同于 SchemaRDD 直接继承 RDD, DataFrame 自己实现了 RDD 的绝大多数功能。

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
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

## 使用 Spark 的 filter 和 select 操作实现类似 Pandas 的 df.loc 的功能

* SDF.filter(): 筛选名为 "SDF" 数据框中的 行(Row)。

* SDF.select(): 筛选名为 "SDF" 数据框中的 列(Col)。

```python
Selected_Rows = SDF.filter((col("Age") > 25) & (col("Gender") == "Male")).select(["Name", "Age"])

print("[Message] Rows and Cols of Filtered Spark DataFrame:")
Selected_Rows.show()
```

输出:

```txt
[Message] Rows and Cols of Filtered Spark DataFrame:
+-------+---+
|   Name|Age|
+-------+---+
|    Bob| 30|
|Charlie| 35|
+-------+---+
```

## 完整代码

```python
#!/usr/bin/python3
# Create By GF 2024-01-06

# 在这个例子中, SDF.filter 用于筛选符合条件的行, 然后通过 select 选择特定的列。
# 你可以根据具体的条件和列名来定制这两个操作, 以达到类似于 Pandas 中 df.loc 的效果。
# 请注意, 与 Pandas 不同, PySpark 的 DataFrame 不是按索引定位的, 而是通过列名来选择和筛选数据的。

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

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

# 使用 Spark 的 filter 和 select 操作实现类似 Pandas 的 df.loc 的功能。
# SDF.filter(): 筛选名为 "SDF" 数据框中的 行(Row)。
# SDF.select(): 筛选名为 "SDF" 数据框中的 列(Col)。
Selected_Rows = SDF.filter((col("Age") > 25) & (col("Gender") == "Male")).select(["Name", "Age"])

print("[Message] Rows and Cols of Filtered Spark DataFrame:")
Selected_Rows.show()
```

## 其它

在这个例子中, SDF.filter 用于筛选符合条件的行, 然后通过 select 选择特定的列。

你可以根据具体的条件和列名来定制这两个操作, 以达到类似于 Pandas 中 df.loc 的效果。

请注意, 与 Pandas 不同, PySpark 的 DataFrame 不是按索引定位的, 而是通过列名来选择和筛选数据的。

## 总结

以上就是关于 大数据分析 PySpark中类Pandas的df.loc操作(行列定位) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
