# 文章_机器学习_Scikit-Learn随机森林回归(RandomForestRegressor)实例_GF_2023-12-30

随机森林回归(Random Forest Regression): 随机森林是一种集成学习方法, 它通过构建多个决策树来进行预测。

它对于处理大量特征、非线性关系和避免过拟合都有一定的优势。

在 Python 中, 你可以使用 Scikit-learn 库中的 RandomForestRegressor 来实现。

随机森林回归作为一种强大的机器学习方法, 具有以下优点:

```txt
1. 高预测准确性: 随机森林回归在处理复杂、高维、非线性的数据时表现出色, 通常能够取得较高的预测准确性。由于随机森林可以通过集成多棵树的预测结果, 从而降低了过拟合的风险, 提高了模型的泛化能力。
2. 对缺失值和异常值具有较好的鲁棒性: 随机森林回归对于缺失值和异常值有一定的容忍度。在训练过程中, 随机森林可以处理缺失值, 避免数据处理过程中信息的丢失。同时, 由于随机森林采用了多树集成的方式, 对于异常值的影响也相对较小。
3. 可处理大规模数据: 随机森林回归可以处理大规模数据集, 且能够在相对较短的时间内生成预测结果。这使得随机森林在大数据场景下具有较好的应用潜力。
4. 不对数据分布和特征空间做出假设: 随机森林回归不对数据的分布和特征空间做出假设, 对于各种类型的数据都可以进行有效的建模, 包括数值型特征、类别型特征、文本特征等, 具有较强的灵活性和适应性。
5. 可解释性: 虽然随机森林回归是一种黑盒模型, 难以解释其内部的决策过程, 但通过特征重要性的排序, 可以了解不同特征对于预测结果的贡献程度, 从而解释模型的预测结果, 使得模型具有一定的可解释性。
```

随机森林回归也存在一些缺点:

```txt
1. 训练时间较长: 由于随机森林需要构建多棵树并进行集成, 训练时间通常较长, 尤其在处理大规模数据集时可能会耗时较多。
2. 内存消耗较大: 随机森林需要存储多棵树的信息, 因此对内存的消耗较大。在处理大规模数据集时, 可能需要较大的内存空间。
3. 不适用于高维稀疏数据: 由于随机森林采用了多树集成的方式, 对于高维稀疏数据的处理相对较为困难。在这种情况下, 其他特定的算法可能更加适用。
4. 不适用于序列数据和时间序列数据: 随机森林回归是一种基于树结构的模型, 对于序列数据和时间序列数据的建模较为困难, 可能需要其他特定的方法。
```

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

这里只是简单示例, 目的在于熟悉 Scikit-Learn 中的随机森林回归使用方法。

**目标**:

通过 `SepalLength(花萼长度)`, `SepalWidth(花萼宽度)`, `PetalLength(花瓣长度)`, `PetalWidth(花瓣宽度)` 预测 `Iris(鸢尾花)` 的 `Species(品种)`。

**标签**:

由于 `Iris(鸢尾花)` 的 `Species(品种)` 是 `字符串(String)` 的形式, 本例将使用 `pandas` 的 `factorize` 模块将 `Iris(鸢尾花)` 的 `Species(品种)` 索引化。

## 导入 Pandas 相关模块

Pandas 是基于 NumPy 的一种工具, 该工具是为解决数据分析任务而创建的。Pandas 纳入了大量库和一些标准的数据模型, 提供了高效地操作大型数据集所需的工具。

Pandas 提供了大量能使我们快速便捷地处理数据的函数和方法。你很快就会发现, 它是使 Python 成为强大而高效的数据分析环境的重要因素之一。

```python
import pandas as pd
```

## 导入 Scikit-Learn 相关模块

Scikit-Learn (以前称为 scikits.learn, 也称为 sklearn) 是针对 Python 编程语言的免费软件机器学习库。

它具有各种分类, 回归和聚类算法, 包括支持向量机, 随机森林, 梯度提升, K均值 和 DBSCAN, 并且旨在与 Python 数值科学库 NumPy 和 SciPy 联合使用。

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
```

## 使用 Pandas 读取 CSV 数据

调用 Pandas 的 .read_csv 方法读取 CSV 数据:

其中 header 参数指定 CSV 文件的表头行, 这里的 header=0 表示表头行在 1 行, 如果 header=None 则表示数据没有列索引, Pandas 则会自动加上索引。

其中 sep 参数指定 CSV 文件的分隔符, 默认情况下都是以 "," 作为分隔符, 这里的 sep="," 表示指定 CSV 文件的分隔符为 ","。

还有 dtype 参数指定 CSV 某些特定列以特定的数据类型进行读取, 例如 dtype={"Close":float, "Volume":int} 表示 "Close" 列以 浮点(float) 类型读取, "Volume" 列以 整数(integer) 类型读取。

```python
PDF = pd.read_csv("D:\\Iris_Dataset_120_2023-12-30.csv", header=0, sep=",")
```

输出 DataFrame 数据框:

```python
print("[Message] Readed CSV File: D:\\Iris_Dataset_120_2023-12-30.csv")
print(PDF)
```

输出:

```txt
[Message] Readed CSV File: D:\Iris_Dataset_120_2023-12-30.csv
     SepalLength  SepalWidth  PetalLength  PetalWidth     Species
0            6.4         2.8          5.6         2.2  Virginical
1            5.0         2.3          3.3         1.0  Versicolor
2            4.9         2.5          4.5         1.7  Virginical
3            4.9         3.1          1.5         0.1      Setosa
4            5.7         3.8          1.7         0.3      Setosa
..           ...         ...          ...         ...         ...
115          5.5         2.6          4.4         1.2  Versicolor
116          5.7         3.0          4.2         1.2  Versicolor
117          4.4         2.9          1.4         0.2      Setosa
118          4.8         3.0          1.4         0.1      Setosa
119          5.5         2.4          3.7         1.0  Versicolor

[120 rows x 5 columns]
```

## 转换 Pandas 中 DateFrame 各列数据类型

通常情况下, 为了避免计算出现数据类型的错误, 都需要重新转换一下数据类型。

```python
# 转换 Pandas 中 DateFrame 数据类型。
PDF["SepalLength"] = PDF["SepalLength"].astype("float64")
PDF["SepalWidth"] =  PDF["SepalWidth"].astype("float64")
PDF["PetalLength"] = PDF["PetalLength"].astype("float64")
PDF["PetalWidth"] =  PDF["PetalWidth"].astype("float64")
PDF["Species"] =     PDF["Species"].astype("string")

# 输出 Pandas 中 DataFrame 字段和数据类型。
print("[Message] Changed Pandas DataFrame Data Type:")
print(PDF.dtypes)
```

输出:

```txt
[Message] Changed Pandas DataFrame Data Type:
SepalLength    float64
SepalWidth     float64
PetalLength    float64
PetalWidth     float64
Species         string
dtype: object
```

## 在 Pandas 的 DataFrame 中将字符标签索引化 / 因子化 (Factorize)

pd.factorize() 是 Pandas 库中的一个函数, 它的作用是将一列数据中的不同取值映射成整数。

具体来说, pd.factorize() 函数会将一个 Series 或者数组中的不同取值转换成从 0 开始的整数, 然后返回两个数组, 第一个数组是整数映射的结果, 第二个数组是整数对应的原始取值。

```python
# 函数示例:
pandas.factorize(values,          # -> 待编码数据。
                 sort=False,      # -> 是否对数据中的唯一值排序。
                 na_sentinel=- 1, # -> 缺失值编码默认为 -1
                 size_hint=None   # -> 哈希表可选大小, 整型。
)

# 返回值:
pandas.factorize 函数的返回值是一个 tuple(元组), 元组中包含两个元素。
第一个元素是一个 array, 其中的元素是标称型元素映射为的数字; 第二个元素是 Index 类型, 其中的元素是所有标称型元素, 没有重复。
```

**转换 Festival 特征列为数值**:

```python
# 将字符串类型的特征列转换为数值 (索引化 / 因子化)。
PDF["Species(Fact)"] = None

Factors, Uniques = pd.factorize(PDF["Species"]) # -> pandas.factorize 函数的返回值是一个 tuple(元组)。

PDF["Species(Fact)"] = Factors # -> 取 tuple(元组) 的第一个元素, 这个 array 中的元素是标称型元素映射为的数字。

# 输出转换后的 DataFrame 数据框。
print("[Message] DataFrame After Character Label Factorization:")
print(PDF)
```

输出:

```txt
[Message] DataFrame After Character Label Factorization:
     SepalLength  SepalWidth  PetalLength  PetalWidth     Species  Species(Fact)
0            6.4         2.8          5.6         2.2  Virginical              0
1            5.0         2.3          3.3         1.0  Versicolor              1
2            4.9         2.5          4.5         1.7  Virginical              0
3            4.9         3.1          1.5         0.1      Setosa              2
4            5.7         3.8          1.7         0.3      Setosa              2
..           ...         ...          ...         ...         ...            ...
115          5.5         2.6          4.4         1.2  Versicolor              1
116          5.7         3.0          4.2         1.2  Versicolor              1
117          4.4         2.9          1.4         0.2      Setosa              2
118          4.8         3.0          1.4         0.1      Setosa              2
119          5.5         2.4          3.7         1.0  Versicolor              1

[120 rows x 6 columns]
```

## 提取 标签(Label)列 和 特征(Feature)列

**提取 标签(Label) 列 (因变量)**:

```python
# 提取 标签(Label) 列 (因变量)。
Y = PDF["Species(Fact)"]
```

**提取 特征(Feature) 列 (自变量)**:

```python
# 提取 特征(Feature) 列 (自变量)。
X = PDF[["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]]
```

## 划分训练集和测试集(train_test_split)

**划分训练集和测试集(train_test_split)**:

```python
# 数据集划分训练集和测试集(train_test_split)。
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.2, random_state=42)
```

## 训练 随机森林回归(RandomForestRegressor) 模型

**创建 随机森林回归(RandomForestRegressor)**:

```python
# 创建 随机森林回归(RandomForestRegressor)。
RFR = RandomForestRegressor()
```

**训练 随机森林回归(RandomForestRegressor) 模型**:

```python
# 训练 随机森林回归(RandomForestRegressor) 模型。
RFR.fit(X_Train, Y_Train)

# Value of Return:
# +------------------------+
# |▼ RandomForestRegressor |
# +------------------------+
# | RandomForestRegressor()|
# +------------------------+
```

## 使用 随机森林回归(RandomForestRegressor) 模型预测数据

```python
# 在测试集上进行预测。
Y_Pred = RFR.predict(X_Test)

# 对比预测结果。
PredPDF = pd.DataFrame({"实际值": Y_Test,
                        "预测值": Y_Pred})

print("[Message] Prediction Results on The Test Data Set for RandomForestRegressor:")
print(PredPDF)
```

输出:

```txt
[Message] Prediction Results on The Test Data Set for RandomForestRegressor:
     实际值   预测值
44        2     2.00
47        0     0.00
4         2     2.00
55        0     0.49
26        1     1.00
64        1     1.00
73        0     0.00
10        1     0.98
40        0     0.00
107       2     2.00
18        0     0.00
62        0     0.07
11        1     0.76
36        0     0.01
89        2     2.00
91        1     1.00
109       2     2.00
0         0     0.00
88        1     0.35
104       2     2.00
65        0     0.00
45        0     0.67
31        1     0.98
70        2     2.00
```

## 使用 mean_squared_error 均方误差(MSE) 评估模型性能

```python
# 评估模型。
RFRMeanSquaredError = mean_squared_error(Y_Test, Y_Pred)
print("随机森林回归 - 均方误差(MSE): %f" % RFRMeanSquaredError)

# 均方误差 (Mean Squared Error, MSE): 表示预测值与真实值之间的平均差的平方。MSE 越小, 表示模型预测越准确。
# 平均绝对误差 (Mean Absolute Error, MAE): 表示预测值与真实值之间的平均绝对差。MAE 越小, 表示模型预测越准确。
# R平方 (R-squared, R2): 表示模型解释方差的比例, 取值范围在 0 和 1 之间, 越接近 1 表示模型的解释能力越强。
```

输出:

```txt
随机森林回归 - 均方误差(MSE): 0.048954
```

## 完整代码

```python
#!/usr/bin/python3
# Create By GF 2023-12-30

# 在这个示例中, 我们使用 RandomForestRegressor 构建随机森林回归模型。
# 为了处理字符串类型的特征列, 我们使用了 pandas.factorize 进行字符标签因子化。
# 然后, 我们对特征进行标准化, 并使用 train_test_split 将数据集划分为训练集和测试集。
# 最后, 我们训练模型、进行预测, 并评估模型性能。
# 请注意, 这只是一个基本的示例, 实际应用中你可能需要更多的特征工程、调参和模型评估。

import pandas as pd
# --------------------------------------------------
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# ####################################################################################################

PDF = pd.read_csv("D:\\Iris_Dataset_120_2023-12-30.csv", header=0, sep=",")

print("[Message] Readed CSV File: D:\\Iris_Dataset_120_2023-12-30.csv")
print(PDF)

# 转换 Pandas 中 DateFrame 数据类型。
PDF["SepalLength"] = PDF["SepalLength"].astype("float64")
PDF["SepalWidth"] =  PDF["SepalWidth"].astype("float64")
PDF["PetalLength"] = PDF["PetalLength"].astype("float64")
PDF["PetalWidth"] =  PDF["PetalWidth"].astype("float64")
PDF["Species"] =     PDF["Species"].astype("string")

# 输出 Pandas 中 DataFrame 字段和数据类型。
print("[Message] Changed Pandas DataFrame Data Type:")
print(PDF.dtypes)

# 将字符串类型的特征列转换为数值 (索引化 / 因子化)。
PDF["Species(Fact)"] = None

Factors, Uniques = pd.factorize(PDF["Species"]) # -> pandas.factorize 函数的返回值是一个 tuple(元组)。

PDF["Species(Fact)"] = Factors # -> 取 tuple(元组) 的第一个元素, 这个 array 中的元素是标称型元素映射为的数字。

# 输出转换后的 DataFrame 数据框。
print("[Message] DataFrame After Character Label Factorization:")
print(PDF)

# 提取 标签(Label) 列 (因变量)。
Y = PDF["Species(Fact)"]

# 提取 特征(Feature) 列 (自变量)。
X = PDF[["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]]

# 数据集划分训练集和测试集(train_test_split)。
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 创建 随机森林回归(RandomForestRegressor)。
RFR = RandomForestRegressor()

# 训练 随机森林回归(RandomForestRegressor) 模型。
RFR.fit(X_Train, Y_Train)

# Value of Return:
# +------------------------+
# |▼ RandomForestRegressor |
# +------------------------+
# | RandomForestRegressor()|
# +------------------------+

# 在测试集上进行预测。
Y_Pred = RFR.predict(X_Test)

# 对比预测结果。
PredPDF = pd.DataFrame({"实际值": Y_Test,
                        "预测值": Y_Pred})

print("[Message] Prediction Results on The Test Data Set for RandomForestRegressor:")
print(PredPDF)

# 评估模型。
RFRMeanSquaredError = mean_squared_error(Y_Test, Y_Pred)
print("随机森林回归 - 均方误差(MSE): %f" % RFRMeanSquaredError)

# 均方误差 (Mean Squared Error, MSE): 表示预测值与真实值之间的平均差的平方。MSE 越小, 表示模型预测越准确。
# 平均绝对误差 (Mean Absolute Error, MAE): 表示预测值与真实值之间的平均绝对差。MAE 越小, 表示模型预测越准确。
# R平方 (R-squared, R2): 表示模型解释方差的比例, 取值范围在 0 和 1 之间, 越接近 1 表示模型的解释能力越强。

```

## 其它

在这个示例中, 我们使用 RandomForestRegressor 构建随机森林回归模型。

为了处理字符串类型的特征列, 我们使用了 pandas.factorize 进行字符标签因子化。

然后, 我们对特征进行标准化, 并使用 train_test_split 将数据集划分为训练集和测试集。

最后, 我们训练模型、进行预测, 并评估模型性能。

请注意, 这只是一个基本的示例, 实际应用中你可能需要更多的特征工程、调参和模型评估。

## 总结

以上就是关于 机器学习 Scikit-Learn随机森林回归(RandomForestRegressor)实例 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
