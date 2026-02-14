# 文章_数据分析_Pandas中的OLAP(类SQL中窗口函数)_GF_2024-01-09

**窗口函数**: 被称为联机分析函数 (OLAP, Online Anallytical Processing) 或者分析函数(Analytic Function)。

窗口函数允许用户根据数据行与所谓窗口 \[so-called window\] 中的当前行之间的某种关系对数据行执行计算, 并对每一行数据返回分析结果, 所以使用窗口函数时, 必须始终记住当前行。

```txt
                          +-------------------+
                          |        Row        |
             +---         +-------------------+         ---+
             |  +---------------------------------------+  |
             |  |         +-------------------+         |  |
             |  |         |        Row        |         |  |
             |  |         +-------------------+         |  |
             |  |      +--|        Row        |         |  |
             |  |      |  +-------------------+        W|  |
             |  | Frame|  |    Current Row    |        i|  |
             |  |      |  +-------------------+        n|  |
Function Over|  |      +--|        Row        |        d|  |
             |  |         +-------------------+        o|  |
             |  |         |        Row        |        w|  |
             |  |         +-------------------+         |  |
             |  |         |        Row        |         |  |
             |  |         +-------------------+         |  |
             |  |         |        Row        |         |  |
             |  |         +-------------------+         |  |
             |  +---------------------------------------+  |
             +---         +-------------------+         ---+
                          |        Row        |
                          +-------------------+
```

## 实例数据

使用 Pandas 的 DataFrame 类构建演示数据。

```python
PDF = pd.DataFrame(
    {"deptName":["研发部", "研发部", "产品部", "产品部", "项目部", "项目部", "研发部", "产品部"],
     "employeeName":["张三", "李四", "王五", "赵六", "李明", "赵亮", "张凯", "赵敏"],
     "salary":[10000, 13000, 12000, 9000, 12500, 8500, 8900, 12000]}
)

print("[Message] Demo Data Based on Pandas DataFrame:")
print(PDF)
```

输出:

```txt
[Message] Demo Data Based on Pandas DataFrame:
   deptName  employeeName  salary
0    研发部          张三   10000
1    研发部          李四   13000
2    产品部          王五   12000
3    产品部          赵六    9000
4    项目部          李明   12500
5    项目部          赵亮    8500
6    研发部          张凯    8900
7    产品部          赵敏   12000
```

## Pandas 类窗口聚合函数 (min, max, avg 等)

支持在 Window 上应用所有的标准聚合函数, 如 min, max, avg 等。

**SQL 等效语句**:

```sql
select deptName, employeeName, salary,
       sum(salary) over(partition by deptName) as sum_salary, 
       avg(salary) over(partition by deptName) as avg_salary, 
       min(salary) over(partition by deptName) as min_salary, 
       max(salary) over(partition by deptName) as max_salary 
from data order by deptName
```

**Pandas 类窗口函数代码**:

```python
NewPDF = PDF.copy()
WindowPDF = NewPDF.groupby('deptName')['salary'];
NewPDF['sum_salary'] = WindowPDF.transform('sum')
NewPDF['min_salary'] = WindowPDF.transform('min')
NewPDF['mean_salary'] = WindowPDF.transform('mean')
NewPDF['max_salary'] = WindowPDF.transform('max')
NewPDF.sort_values('deptName')

print("[Message] Functions Similar to OLAP for Standard Aggregation Based on Pandas DataFrame (Such as min, max, Avg, etc.):")
print(NewPDF.sort_values('deptName'))
```

输出:

```txt
[Message] Functions Similar to OLAP for Standard Aggregation Based on Pandas DataFrame (Such as min, max, Avg, etc.):
   deptName  employeeName  salary  sum_salary  min_salary   mean_salary  max_salary
2    产品部          王五   12000       33000        9000  11000.000000       12000
3    产品部          赵六    9000       33000        9000  11000.000000       12000
7    产品部          赵敏   12000       33000        9000  11000.000000       12000
0    研发部          张三   10000       31900        8900  10633.333333       13000
1    研发部          李四   13000       31900        8900  10633.333333       13000
6    研发部          张凯    8900       31900        8900  10633.333333       13000
4    项目部          李明   12500       21000        8500  10500.000000       12500
5    项目部          赵亮    8500       21000        8500  10500.000000       12500
```

## Pandas 类窗口排序函数

排序函数常用于对分组集或者整体数据进行排名:

* row_number: 对分组內的数据进行 "同分不同级" 方式排序, 不存在序号并列的现象, 即使同分时排序也会不同。

* rank: 对分组內的数据进行 "同分同级且不紧密" 方式排序, 当同分时序号相同, 其它排序按正常排名进行排序, 即 1, 2, 2, 4, 5。

* dense_rank: 对分组內的数据进行 "同分同级且紧密" 方式排序, 当同分时序号相同, 其它排序按下一排名进行排序, 即 1, 2, 2, 3, 4。

**SQL 等效语句**:

```sql
select deptName, employeeName, salary,
       row_number(salary) over(partition by deptName order by salary desc) as row_number,
       rank(salary) over(partition by deptName order by salary desc) as rank,
       dense_rank(salary) over(partition by deptName order by salary desc) as dense_rank
from data order by employeeName,salary
```

**Pandas 类窗口函数代码**:

```python
NewPDF = PDF.copy()
WindowDF = NewPDF.groupby('deptName')['salary'];
NewPDF['row_number'] = WindowPDF.rank(ascending=False,method='first')
NewPDF['rank'] = WindowPDF.rank(ascending=False,method='min')  
NewPDF['dense_rank'] = WindowPDF.rank(ascending=False,method='dense') 
NewPDF.sort_values(['deptName','salary'])

print("[Message] Functions Similar to OLAP for Sorting Based on Pandas DataFrame:")
print(NewPDF.sort_values(['deptName','salary']))
```

输出:

```txt
[Message] Functions Similar to OLAP for Sorting Based on Pandas DataFrame:
   deptName  employeeName  salary  row_number  rank  dense_rank
3    产品部          赵六    9000         3.0   3.0         2.0
2    产品部          王五   12000         1.0   1.0         1.0
7    产品部          赵敏   12000         2.0   1.0         1.0
6    研发部          张凯    8900         3.0   3.0         3.0
0    研发部          张三   10000         2.0   2.0         2.0
1    研发部          李四   13000         1.0   1.0         1.0
5    项目部          赵亮    8500         2.0   2.0         2.0
4    项目部          李明   12500         1.0   1.0         1.0
```

## Pandas 类窗口分布函数

在 SQL 中分布函数主要分为两类: percent_rank() 和 cume_dist(): 

* percent_rank(): 指按照排名计算百分比, 即该排名位于区间[0,1]的位置, 其中区间内第一名为值0, 最后一名值为1。其具体公式为: percent_rank() = (rank - 1) / (rows - 1)

* cume_dist(): 指区间內大于等于当前排名的行数占区间内总函数的比例。多用于判断比当前薪资、得分高的用户比例为多少。

**SQL 等效语句**:

```sql
select deptName, employeeName, salary,
       percent_rank(salary) over(partition by deptName order by salary desc) as percent_rank,
       cume_dist(salary) over(partition by deptName order by salary desc) as cume_dist
from data order by employeeName,salary
```

**Pandas 类窗口函数代码**:

```python
NewPDF = PDF.copy()
WindowPDF = NewPDF.groupby('deptName')['salary'];
NewPDF['rank'] = WindowPDF.rank(ascending=False,method='min')  
NewPDF['count'] = WindowPDF.transform('size')  
NewPDF['percent_rank'] = (WindowPDF.rank(ascending=False,method='min')-1) / (WindowPDF.transform('count')-1)  # -> 如果分组只有一个记录则数据为 na。 
NewPDF['cume_dist'] = WindowPDF.rank(ascending=False,method='first',pct=True)  # -> 可以结合排序函数的方法使用。
NewPDF.sort_values(['deptName','salary'])

print("[Message] Functions Similar to OLAP for Cumulative Distribution Based on Pandas DataFrame:")
print(NewPDF.sort_values(['deptName','salary']))
```

输出:

```txt
[Message] Functions Similar to OLAP for Cumulative Distribution Based on Pandas DataFrame:
   deptName  employeeName  salary  rank  count  percent_rank  cume_dist
3    产品部          赵六    9000   3.0      3           1.0   1.000000
2    产品部          王五   12000   1.0      3           0.0   0.333333
7    产品部          赵敏   12000   1.0      3           0.0   0.666667
6    研发部          张凯    8900   3.0      3           1.0   1.000000
0    研发部          张三   10000   2.0      3           0.5   0.666667
1    研发部          李四   13000   1.0      3           0.0   0.333333
5    项目部          赵亮    8500   2.0      2           1.0   1.000000
4    项目部          李明   12500   1.0      2           0.0   0.500000
```

## Pandas 类窗口平移函数

在 SQL 中平移函数主要分为两类: lead(列名, n) 和 lag(列名, n), 此函数多用于计算指标同比、环比:

* lead(列名, n): 获取分区內向下平移n行数据。

* lag(列名, n): 获取分区內向上平移n行数据。

**SQL 等效语句**:

```sql
select deptName, employeeName, salary,
       lead(salary,1) over(partition by deptName order by salary desc ) as lead,
       lag(salary,1) over(partition by deptName order by salary desc) as lag
from data order by deptName,salary desc
```

**Pandas 类窗口函数代码**:

```python
NewPDF = PDF.copy()
NewPDF['lead'] = NewPDF.sort_values(['deptName','salary'],ascending=False).groupby('deptName')['salary'].shift(-1) # 分区內向下平移一个单位。
NewPDF['lag'] = NewPDF.sort_values(['deptName','salary'],ascending=False).groupby('deptName')['salary'].shift(1)  # 分区內向上平移一个单位。
NewPDF.sort_values(['deptName','salary'],ascending=False)

print("[Message] Functions Similar to OLAP for Parallel Movement Based on Pandas DataFrame:")
print(NewPDF.sort_values(['deptName','salary'],ascending=False))
```

输出:

```txt
[Message] Functions Similar to OLAP for Parallel Movement Based on Pandas DataFrame:
   deptName  employeeName  salary     lead      lag
4    项目部          李明   12500   8500.0      NaN
5    项目部          赵亮    8500      NaN  12500.0
1    研发部          李四   13000  10000.0      NaN
0    研发部          张三   10000   8900.0  13000.0
6    研发部          张凯    8900      NaN  10000.0
2    产品部          王五   12000  12000.0      NaN
7    产品部          赵敏   12000   9000.0  12000.0
3    产品部          赵六    9000      NaN  12000.0
```

## Pandas 类窗口首尾函数

在 SQL 中首尾函数主要分为两类: first_val() 和 last_val():

* first_val(): 获取分区內第一行数据。

* last_val(): 获取分区內最后一行数据。

**SQL 等效语句**:

```sql
select deptName, employeeName, salary,
       first_val(salary) over(partition by deptName order by salary desc ) as first_val,
       -- 由于窗口函数默认的是第一行至当前行, 所以在使用last_val()函数时, 会出现分区内最后一行和当前行大小一致的情况, 因此我们需要将分区偏移量改为第一行至最后一行。       
       last_val(salary) over(partition by deptName order by salary desc rows between UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING) as last_val
from data order by deptName,salary
```

**Pandas 类窗口函数代码**:

```python
NewPDF = PDF.copy()
NewPDF['first_val'] = NewPDF.groupby('deptName')['salary'].transform('min')
NewPDF['last_val'] = NewPDF.groupby('deptName')['salary'].transform('max')
NewPDF.sort_values(['deptName','salary'],ascending=True)

print("[Message] Functions Similar to OLAP for Head and Tail Based on Pandas DataFrame:")
print(NewPDF.sort_values(['deptName','salary'],ascending=True))
```

输出:

```txt
[Message] Functions Similar to OLAP for Head and Tail Based on Pandas DataFrame:
   deptName  employeeName  salary  first_val  last_val
3    产品部          赵六    9000       9000     12000
2    产品部          王五   12000       9000     12000
7    产品部          赵敏   12000       9000     12000
6    研发部          张凯    8900       8900     13000
0    研发部          张三   10000       8900     13000
1    研发部          李四   13000       8900     13000
5    项目部          赵亮    8500       8500     12500
4    项目部          李明   12500       8500     12500
```

## Pandas 类窗口 Top N 函数

Top n rows per group 每组取 top N。

如果 tips.csv 没有下载到本地, 可以使用如下语句远程读取数据:

```python
url = ("https://raw.github.com/pandas-dev/pandas/main/pandas/tests/io/data/csv/tips.csv")
tips = pd.read_csv(url)
```

或者点击 [CSV数据-Pandas-Tests-IO-Data-CSV-Tips-2024-01-09.zip](./CSV数据_Pandas_Tests_IO_Data_CSV_Tips_2024-01-09.zip) 下载数据。

### 按天统计给小费最高的 2 笔记录 (基于餐厅消费数据)

**SQL 等效语句**:

```sql
SELECT * FROM (
  SELECT
    t.*,
    ROW_NUMBER() OVER(PARTITION BY day ORDER BY total_bill DESC) AS rn
  FROM tips t
)
WHERE rn < 3
ORDER BY day, rn;
```

**Pandas 类窗口函数代码**:

```python
tips = pd.read_csv("./tips.csv")

# 方式一。
res = tips.assign(
        rn=tips.sort_values(["total_bill"], ascending=False)
        .groupby(["day"])
        .cumcount()
        + 1
).query("rn < 3").sort_values(["day", "rn"])

# 方式二。
# res = tips.assign(
#         rnk=tips.groupby(["day"])["total_bill"].rank(
#             method="first", ascending=False
#         )
# ).query("rnk < 3").sort_values(["day", "rnk"])

print("[Message] Functions Similar to OLAP for The Top N by Day Based on Pandas DataFrame:")
print(res)
```

输出:

```txt
[Message] Functions Similar to OLAP for The Top N by Day Based on Pandas DataFrame:
     total_bill    tip     sex  smoker   day    time  size  rnk
 95       40.17   4.73    Male     Yes   Fri  Dinner     4  1.0
 90       28.97   3.00    Male     Yes   Fri  Dinner     2  2.0
170       50.81  10.00    Male     Yes   Sat  Dinner     3  1.0
212       48.33   9.00    Male      No   Sat  Dinner     4  2.0
156       48.17   5.00    Male      No   Sun  Dinner     6  1.0
182       45.35   3.50    Male     Yes   Sun  Dinner     3  2.0
197       43.11   5.00  Female     Yes  Thur   Lunch     4  1.0
142       41.19   5.00    Male      No  Thur   Lunch     5  2.0
```

### 按性别统计给小费最高的 2 笔记录 (基于餐厅消费数据)

**SQL 等效语句**:

```sql
SELECT * FROM (
  SELECT
    t.*,
    RANK() OVER(PARTITION BY sex ORDER BY tip desc) AS rnk
  FROM tips t
  WHERE tip < 2
)
WHERE rnk < 3
ORDER BY sex, rnk;
```

**Pandas 类窗口函数代码**:

```python
tips = pd.read_csv("./tips.csv")

print("[Message] Functions Similar to OLAP for The Top N by Sex Based on Pandas DataFrame:")
(
    tips
    .assign(rnk_min=tips.groupby(["sex"])["tip"].rank(method="min",ascending=False))
    .query("rnk_min < 3")
    .sort_values(["sex", "rnk_min"],ascending=True)
)
```

输出:

```txt
[Message] Functions Similar to OLAP for The Top N by Sex Based on Pandas DataFrame:
     total_bill   tip     sex  smoker  day    time  size  rnk_min
214       28.17   6.5  Female     Yes  Sat  Dinner     3      1.0
 52       34.81   5.2  Female      No  Sun  Dinner     4      2.0
170       50.81  10.0    Male     Yes  Sat  Dinner     3      1.0
212       48.33   9.0    Male      No  Sat  Dinner     4      2.0
```

### nlargest 的使用示例 (基于餐厅消费数据)

**SQL 等效语句**:

```sql
SELECT * FROM tips ORDER BY tip DESC LIMIT 10 OFFSET 5;
```

**Pandas 类窗口函数代码**:

```python
tips = pd.read_csv("./tips.csv")

res = tips.nlargest(10 + 5, columns="tip").tail(10)

print("[Message] Functions Similar to OLAP for The Top N by nlargest Based on Pandas DataFrame:")
print(res)
```

输出:

```txt
[Message] Functions Similar to OLAP for The Top N by nlargest Based on Pandas DataFrame:
     total_bill   tip     sex  smoker   day    time  size
183       23.17  6.50    Male     Yes   Sun  Dinner     4
214       28.17  6.50  Female     Yes   Sat  Dinner     3
 47       32.40  6.00    Male      No   Sun  Dinner     4
239       29.03  5.92    Male      No   Sat  Dinner     3
 88       24.71  5.85    Male      No  Thur   Lunch     2
181       23.33  5.65    Male     Yes   Sun  Dinner     2
 44       30.40  5.60    Male      No   Sun  Dinner     4
 52       34.81  5.20  Female      No   Sun  Dinner     4
 85       34.83  5.17  Female      No  Thur   Lunch     4
211       25.89  5.16    Male     Yes   Sat  Dinner     4
```

## 总结

以上就是关于 数据分析 Pandas中的OLAP(类SQL中窗口函数) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
