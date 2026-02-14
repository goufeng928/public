#! /usr/bin/env python3

# Create By GF 2023-07-10 23:05

# Py3_Demo_字符串(String)_Explain_GF_2023-07-10.py

# ----------------------------------------------------------------------------------------------------
# 0. 什么是 Python 字符串。

# 字符串是 Python 中最常用的数据类型。

# ----------------------------------------------------------------------------------------------------
# 1. 如何表示一个字符串。

# Python 中的字符串字面量由单引号或双引号括起。

myString1='abcdef'

myString2="hijklm"

# 也可使用三对单引号来表示一个长字符串。

myString3='''you need to clam down, you need to clam down, you need to clam down, 
you need to cam down'''

# 只要在引号范围内就是有效内容。

# ----------------------------------------------------------------------------------------------------
# 2. 字符串的访问。

    # ------------------------------------------------------------------------------------------------
    # 2.1 print() 方法。
    
    # 直接使用 print() 打印字符串。
    
    myString1='abcdef'
     
    print(myString1)

    # Output:

    #>>> print(myString1)
    #abcdef
    
    print("myString 1 is "+myString1)
    
    # Output:

    #>>> print("myString 1 is "+myString1)
    #myString 1 is abcdef

    # ------------------------------------------------------------------------------------------------
    # 2.2 索引。
    
    # 类似数组。
    
    # ------------------------------------------------------------------------------------------------
    # 2.3 for 循环。

    for letter in myString1:
        print(letter)
     
    # Output:

    #>>> for letter in myString1:
    #    print(letter)
    #
    #a
    #b
    #c
    #d
    #e
    #f
    
    # 把字符串中每个字符切片成 “字符” + “\n" 打印出来。
    
    # 但是我们有些情况下不想打印成这种形式，想要一个完整的句子。
    
    # 这时就要使用 end() 函数了。
    
    # ------------------------------------------------------------------------------------------------
    # 2.4 打印字符 end()。
    
    # 将字符末端的 '\n' 替换为 end() 函数中括号里的内容。
    
    # 最普遍的是
    
    for letter in myString1:
        print(letter,end='')
    
    # Output:
    
    #>>> for letter in myString1:
    #    print(letter,end='')
    #    
    #abcdef
    
    # 比较个性的：
    
    for letter in myString1:
        print(letter,end='*&*')
    
    # Output:
    
    #>>> for letter in myString1:
    #    print(letter,end='*&*')
    #  
    #a*&*b*&*c*&*d*&*e*&*f*&*
    
    # 当然一切以实际需求为准。
    
    # ------------------------------------------------------------------------------------------------
    # 2.5 范围选择符 [n:m]。
    
    # 可以说字符串和数组十分相似，数组可以使用的方法同样适用于字符串。
    
    # 在此强调一点 split() 方法是对原字符串的拷贝，并不改变原来的字符串。
    
    myString3='a-good-boy-a-good-boy'
    
    myString4=myString3[2:10]
    
    print(myString3)
    
    # Output:
    
    #>>> print(myString3)
    #a-good-boy-a-good-boy
    
    print(myString4)
    
    # Output:
    
    #>>> print(myString4)
    #good-boy
    
    # 结合 for 循环：
    
    for letter in myString3[2:10]:
        print(letter,end='')
    
    # Output:
    
    #>>> for letter in myString3[2:10]:
    #    print(letter,end='')
    #
    #good-boy

# ----------------------------------------------------------------------------------------------------
# 3. 字符串的拆分（字符串拆分为列表）。
    
    # ------------------------------------------------------------------------------------------------
    # split() 方法。
    
    # 将字符串拆分成列表。
    
    # 可以不对分隔符作出限制。
    
    str1=myString1.split()
    
    print(str1)
    
    # Output:
    
    #>>> print(str1)
    #['abcdef']
    
    # 一个参数:
    
    # 也可在 split() 方法中添加限制，分隔符不被写入列表。
    
    myString2='abcabcabc'
    
    str2=myString2.split('b')
    
    print(str2)
    
    # Output:
    
    #>>> print(str2)
    #['a', 'ca', 'ca', 'c']
    
    # 常见的分隔：
    
    myString3='a-good-boy'
    
    str3=myString3.split('-')
    
    print(str3)
    # Output:
    
    #>>> print(str3)
    #['a', 'good', 'boy']
    
    # 两个参数：
    
    # 第一个是分隔符，第二个是检测几次分隔符。默认为 -1（即全部分隔符）。
    
    myString3='a-good-boy-a-good-boy'
    
    str3=myString3.split('-',3)
    
    print(str3)
    
    # Output:
    
    #>>> print(str3)
    #['a', 'good', 'boy', 'a-good-boy']
   
# ----------------------------------------------------------------------------------------------------
# 4. 字符串的连接 / 复制 / 合并：

    # ------------------------------------------------------------------------------------------------
    # 4.1 字符串相加相乘。
    
    # 运算符号系列。
    
    # " + " 链接两个字符串：
    
    myString6 = '123456'
    
    myString7 = 'abcd'
    
    str5 = myString6 + myString7
    
    print(str5)
    
    # Output:
    
    #>>> print(str5)
    #123456abcd
    
    # " * " 重复字符串中的内容：
    
    myString7 = 'abcd'
    
    str6 = myString7 * 4
    
    print(str6)
    
    # Output:
    
    #>>> print(str6)
    #abcdabcdabcdabcd
    
    # ------------------------------------------------------------------------------------------------
    # 4.2 join() 方法（列表合并为字符串）。

    # 使用 join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。

    # 下面代码中的 * 充当链接符，当然也可以是其它任何字符。
    
    myString3='a-good-boy-a-good-boy'
    
    str3=myString3.split('-')
    
    print(str3)
    
    # Output:
    
    #>>> print(str3)
    #['a', 'good', 'boy', 'a', 'good', 'boy']
    
    str4='*'.join(str3)
    
    print(str4)
    
    # Output:
    
    #>>> print(str4)
    #a*good*boy*a*good*boy

# ----------------------------------------------------------------------------------------------------
# 5. 字符串的替换。

    # ------------------------------------------------------------------------------------------------
    # replace() 方法（用另一段字符串来替换现有的字符串）。

    # 至少要有两个参数，第一个参数是旧的字符串，第二个是替换后的字符串。

    myString1='abcdefabcdefabcdef'
    
    str4=myString1.replace('a','A')
    
    print(myString1)
    
    # Output:
    
    #>>> print(myString1)
    #abcdefabcdefabcdef
    
    print(str4)
    
    # Output:
    
    #>>> print(str4)
    #AbcdefAbcdefAbcdef
    
    # 第三个参数是设定替换次数的，默认为全部的。
    
    myString1='abcdefabcdefabcdef'
    
    str4=myString1.replace('a','A',1)
    
    print(myString1)
    
    # Output:
    
    #>>> print(myString1)
    #abcdefabcdefabcdef
    
    print(str4)
    
    # Output:
    
    #>>> print(str4)
    #Abcdefabcdefabcdef
    
    # 经典力扣题《替换空格》，用 Python 一下就出来了：
    
    # return s.replace(' ', '%20')

# ----------------------------------------------------------------------------------------------------
# 6. 使用 len() 函数获取字符串长度。

myString1='abcdef'

lengthOfStr1=len(myString1)

print('lengthOfStr1 is '+str(lengthOfStr1))
 
# Output:

#>>> print('lengthOfStr1 is '+str(lengthOfStr1))
#lengthOfStr1 is 6

# ----------------------------------------------------------------------------------------------------
# 7. 检查字符串 in / not in。

myString5='You need to calm down'

x='cal' in myString5

y='ooo' in myString5

z='ooo' not in myString5

print(type(x))

# Output:

#>>> print(type(x))
#<class 'bool'>

print(x)

# Output:

#>>> print(x)
#True

print(y)

# Output:

#>>> print(y)
#False

print(z)

# Output:

#>>> print(z)
#True

# ----------------------------------------------------------------------------------------------------
# 8. 字符串内容判断。

# 判断字符内容，返回布尔值。

# +------------+---------------------+
# |isalnum()   |字符是否为字符或数字 |
# |isalpha()   |字符是否为字母       |
# |isdigit()   |字符是否为数字       |
# |isdecimal() |字符是否为小数       |
# +------------+---------------------+

# 判断字符串中的数字的两种方法：

count=0
cnt=0

str='at 9 o\'clock to reach work at 10 am.'

for m in str:
    #方法一
    if(m>='0'and(m<='9')):
        cnt+=1
    #方法二
    if(m.isdigit()):
        count+=1
        
print(count)

# Output:

#>>> print(count)
#3

print(cnt)

# Output:

#>>> print(cnt)
#3

# ----------------------------------------------------------------------------------------------------
# 9. 字符串内容搜索。

# +--------+-------------------------------------------+
# |count() |返回指定值在字符串中出现的次数             |
# |find()  |在字符串中搜索指定的值并返回它被找到的位置 |
# |index() |在字符串中搜索指定的值并返回它被找到的位置 |
# +--------+-------------------------------------------+

str='at 9 o\'clock to reach work at 10 am.'

n=str.count('a')

print(n)

# Output:

#>>> print(n)
#4

# ----------------------------------------------------------------------------------------------------
# 10. 字符串内容格式化。

# +----------------------+---------------------------------------+
# |capotalize()          |首字符为大写                           |
# |casefold()            |把字符串转化成小写                     |
# |upper()               |把字符串转化成大写                     |
# |swapcase()            |切换大小写                             |
# |tittle()              |把每个单词的首字符转换成大写           |
# |startwith()/endwith() |以指定值开头、结尾的字符串，返回布尔值 |
# +----------------------+---------------------------------------+

test=open('para1.txt','r')

for line in test:
    if(line.startswith('The') or line.startswith('You')or
        line.startswith('Please')):
        print(line.upper())
    if(line.endswith('unit\n') or line.endswith('document\n')):
        print(line.lower())
    if (line == ''):
        break

test.close()

# ----------------------------------------------------------------------------------------------------
# EOF
