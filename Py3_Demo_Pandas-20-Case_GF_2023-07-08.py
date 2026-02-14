#! /usr/bin/env python3

# Create By GF 2023-07-08

# Py3_Demo_Pandas-20-Case_GF_2023-07-08.py

# Pandas 1.4.1

# ----------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np

# ----------------------------------------------------------------------------------------------------
# 建立数据集。

df = pd.DataFrame({"name"          : ["John", "Jane", "Emily", "Lisa", "Matt"],
                   "note"          : [92, 94, 87, 82, 90],
                   "profession"    : ["Electrical engineer", "Mechanical engineer", "Data scientist", "Accountant", "Athlete"],
                   "date_of_birth" : ["1998-11-01", "2002-08-14", "1996-01-12", "2002-10-24", "2004-04-05"],
                   "group"         : ["A","B","B","A","C"]}
                  )

# Output:

#>>> df
#    name  note           profession date_of_birth group
#0   John    92  Electrical engineer    1998-11-01     A
#1   Jane    94  Mechanical engineer    2002-08-14     B
#2  Emily    87       Data scientist    1996-01-12     B
#3   Lisa    82           Accountant    2002-10-24     A
#4   Matt    90              Athlete    2004-04-05     C

# ----------------------------------------------------------------------------------------------------
# 1. 筛选表格中的若干列。

df[["name", "note"]]

# Output:

#>>> df[["name", "note"]]
#    name  note
#0   John    92
#1   Jane    94
#2  Emily    87
#3   Lisa    82
#4   Matt    90

# ----------------------------------------------------------------------------------------------------
# 2. 先筛选表格中的若干列，再筛选出若干行。

# 基于筛选列的结果之上，再筛选出若干行。

df.loc[:3, ["name","note"]]

# Output:

#>>> df.loc[:3, ["name","note"]]
#    name  note
#0   John    92
#1   Jane    94
#2  Emily    87
#3   Lisa    82

# ----------------------------------------------------------------------------------------------------
# 3. 根据索引来过滤数据。

# 这里用到的是 .iloc 方法。

df.iloc[:3, 2]

# Output:

#>>> df.iloc[:3, 2]
#0    Electrical engineer
#1    Mechanical engineer
#2         Data scientist
#Name: profession, dtype: object

# ----------------------------------------------------------------------------------------------------
# 4. 通过比较运算符来筛选数据。

df[df.note > 90]

# Output:

#>>> df[df.note > 90]
#   name  note           profession date_of_birth group
#0  John    92  Electrical engineer    1998-11-01     A
#1  Jane    94  Mechanical engineer    2002-08-14     B

# ----------------------------------------------------------------------------------------------------
# 5. dt 属性接口。

# dt 属性接口是用于处理时间类型的数据的。
# 当然首先我们需要将字符串类型的数据，或者其他类型的数据转换成事件类型的数据，再进行数据处理。


df.date_of_birth = df.date_of_birth.astype("datetime64[ns]")


df[df.date_of_birth.dt.month == 11]

# Output:

#>>> df[df.date_of_birth.dt.month == 11]
#   name  note           profession date_of_birth group
#0  John    92  Electrical engineer    1998-11-01     A

# 或者也可以：

df[df.date_of_birth.dt.year > 2000]

# Output:

#>>> df[df.date_of_birth.dt.year > 2000]
#   name  note           profession date_of_birth group
#1  Jane    94  Mechanical engineer    2002-08-14     B
#3  Lisa    82           Accountant    2002-10-24     A
#4  Matt    90              Athlete    2004-04-05     C

# ----------------------------------------------------------------------------------------------------
# 6. 多个条件交集过滤数据。

# 多个条件，并且是交集的情况下过滤数据。


df[(df.date_of_birth.dt.year > 2000) & (df.profession.str.contains("engineer"))]

# Output:

#>>> df[(df.date_of_birth.dt.year > 2000) & (df.profession.str.contains("engineer"))]
#   name  note           profession date_of_birth group
#1  Jane    94  Mechanical engineer    2002-08-14     B

# ----------------------------------------------------------------------------------------------------
# 7. 多个条件并集筛选数据。

# 多个条件，并且是交集的情况下过滤数据。


df[(df.note > 90) | (df.profession=="Data scientist")]

# Output:

#>>> df[(df.note > 90) | (df.profession=="Data scientist")]
#    name  note           profession date_of_birth group
#0   John    92  Electrical engineer    1998-11-01     A
#1   Jane    94  Mechanical engineer    2002-08-14     B
#2  Emily    87       Data scientist    1996-01-12     B

# ----------------------------------------------------------------------------------------------------
# 8. Query 方法过滤数据。

# Pandas 当中的 .query 方法也可以对数据进行过滤。


df.query("note > 90")

# Output:

#>>> df.query("note > 90")
#   name  note           profession date_of_birth group
#0  John    92  Electrical engineer    1998-11-01     A
#1  Jane    94  Mechanical engineer    2002-08-14     B

# 或者：

df.query("group=='A' and note > 89")

#>>> df.query("group=='A' and note > 89")
#   name  note           profession date_of_birth group
#0  John    92  Electrical engineer    1998-11-01     A

# ----------------------------------------------------------------------------------------------------
# 9. nsmallest 方法过滤数据。

# Pandas当中的 。nsmallest 以及 .nlargest 方法是用来找到数据集当中最大、最小的若干数据。

df.nsmallest(2, "note")

# Output:

#>>> df.nsmallest(2, "note")
#    name  note      profession date_of_birth group
#3   Lisa    82      Accountant    2002-10-24     A
#2  Emily    87  Data scientist    1996-01-12     B

df.nlargest(2, "note")

# Output:

#>>> df.nlargest(2, "note")
#   name  note           profession date_of_birth group
#1  Jane    94  Mechanical engineer    2002-08-14     B
#0  John    92  Electrical engineer    1998-11-01     A

# ----------------------------------------------------------------------------------------------------
# 10. isna() 方法。

# isna() 方法功能在于过滤出那些是空值的数据

# 首先我们将表格当中的某些数据设置成空值。

df.loc[0, "profession"] = np.nan

df[df.profession.isna()]

# Output:

#>>> df[df.profession.isna()]
#   name  note profession date_of_birth group
#0  John    92        NaN    1998-11-01     A

# ----------------------------------------------------------------------------------------------------
# 11. notna() 方法。

# notna()方法上面的isna()方法正好相反的功能在于过滤出那些不是空值的数据。

df[df.profession.notna()]

# Output:

#>>> df[df.profession.notna()]
#    name  note           profession date_of_birth group
#1   Jane    94  Mechanical engineer    2002-08-14     B
#2  Emily    87       Data scientist    1996-01-12     B
#3   Lisa    82           Accountant    2002-10-24     A
#4   Matt    90              Athlete    2004-04-05     C

# ----------------------------------------------------------------------------------------------------
# 12. assign() 方法。

# Pandas 当中的 .assign() 方法作用是直接向数据集当中来添加一列。

df_1 = df.assign(score=np.random.randint(0, 100, size=5))

# Output:

#>>> df_1 = df.assign(score=np.random.randint(0, 100, size=5))
#>>> df_1
#    name  note           profession date_of_birth group  score
#0   John    92                  NaN    1998-11-01     A     66
#1   Jane    94  Mechanical engineer    2002-08-14     B     98
#2  Emily    87       Data scientist    1996-01-12     B     93
#3   Lisa    82           Accountant    2002-10-24     A     57
#4   Matt    90              Athlete    2004-04-05     C     67

# ----------------------------------------------------------------------------------------------------
# 13. explode() 方法。

# explode() 方法直译的话，是爆炸的意思，我们经常会遇到这样的数据集。

df = pd.DataFrame({"Name"  : ["吕布", "貂蝉", "赵云"],
                   "Hobby" : [["打篮球", "玩游戏", "喝奶茶"], ["敲代码", "看电影"], ["听音乐", "健身"]]}
                  )

# Output:

#>>> df
#  Name            Hobby
#0   吕布  [打篮球, 玩游戏, 喝奶茶]
#1   貂蝉       [敲代码, 看电影]
#2   赵云        [听音乐, 健身]

# Hobby 列当中的每行数据都以列表的形式集中到了一起，而 .explode() 方法则是将这些集中到一起的数据拆开来。

df.explode("Hobby")

# Output:

#>>> df.explode("Hobby")
#  Name Hobby
#0   吕布   打篮球
#0   吕布   玩游戏
#0   吕布   喝奶茶
#1   貂蝉   敲代码
#1   貂蝉   看电影
#2   赵云   听音乐
#2   赵云    健身

# 展开之后，数据会存在重复的情况。

df.explode('Hobby').drop_duplicates().reset_index(drop=True)

# Output:

#>>> df.explode('Hobby').drop_duplicates().reset_index(drop=True)
#  Name Hobby
#0   吕布   打篮球
#1   吕布   玩游戏
#2   吕布   喝奶茶
#3   貂蝉   敲代码
#4   貂蝉   看电影
#5   赵云   听音乐
#6   赵云    健身

# ----------------------------------------------------------------------------------------------------
# EOF
