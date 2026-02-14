#! /usr/bin/env python3

# Create By GF 2023-07-11 22:31

# Py3_Demo_异常处理(Try-Except)_Explain_GF_2023-07-11.py

# ----------------------------------------------------------------------------------------------------
# 什么是异常。

    # 在执行python程序时，会有出现错误的可能。导致出错的原因有一般两种：
    
        # 1. 语法错误：程序员编写的代码不符合 Python 的规范，比如把 print 写成了 printf，此种错误一旦出现会导致程序无法正常启动，但是此类错误是可以避免的。
        
        # 2. 异常：异常是指在程序运行的过程中由于用户的非法输入，环境的不稳定，突然断网等等不可控的因素导致程序无法正常处理，比如做除法运算时，用户输入了除数为 0 的式子。这些情况需要靠 Python 提供的异常处理机制来解决。
    
    # 代码的健壮性的一方面就体现在：程序是否有完备的异常处理，能够保证在程序运行时遇到非法输入，系统崩溃，突然断网等意外时可以给出对应的错误提示，使程序正常退出。

# ----------------------------------------------------------------------------------------------------
# 执行流程图。

    #                          +- 没有异常 - [Execute Code in "else"] ---+
    #                          |                                         |
    # [Execute Code in "try"] -+                                         +- [Execute Code in "finally"]
    #                          |                                         |
    #                          +- 出现异常 - [Execute Code in "except"] -+

# ----------------------------------------------------------------------------------------------------
# 2. try…excpt 的使用。

    # 2.1 语法介绍
    
        # Python 会捕获到 try 中的异常，并且当 try 中某一行出现异常后，后面的代码将不会再被执行；而是直接调用 except 中的代码。
        
        # try...except 是 python 为程序员提供处理异常的一种措施；语法如下：
        
            # try:
            #     可能出现异常的代码
            # except (Error1, Error2, Error3, ...) as e:
            #     处理异常的代码
            # except [Exception]:
            #     处理异常的代码
            # 
            # -> Error : 异常类型，一个 except 代码块可以同时处理多种异常类型。
            # -> Exception : 表示所有异常类型，一般用在最后一个 except 块中。
        
        # 值的注意的是 except 和 except Exception 的作用是一样的，都是处理所有的异常类型。
        
        # 举个例子：
        
            try:
                print(ss)
            except (ZeroDivisionError, NameError) as e:
                print('出现了除0错误和访问未声明变量错误中的一种')
            except:
                print('其他错误类型')
        
        # 输出结果：
        
            # 出现了除0错误和访问未声明变量错误中的一种
        
        # 此处 Python 在 try 语句中捕获到了异常类型为 NameError，因此执行了第一个 except 代码块中的代码。
    
    # 2.2 执行流程
    
        # try...except 语句的执行流程非常简单，可分为两步：
        
            # 1. 执行 try 语句中的代码，如果出现异常，Python 会得到异常的类型。
            
            # 2. Python 将出现的异常类型和 except 语句中的异常类型做对比，调用对应 except 语句中的代码块。
    
    # 2.3 异常类型的查看
    
        # 比如上面的一段代码：
        
            try:
                print(ss)
            except (ZeroDivisionError, NameError) as e:
                print('出现了除0错误和访问未声明变量错误中的一种')
            except:
                print('其他错误类型')
        
        # 如果想看异常的详细信息，有四种方法：
        
            # 1. e.args : 返回异常信息，元组
            
            # 2. str(e)：返回异常信息，字符串
            
            # 3. repr(e)：返回异常类型，异常信息
            
            # 4. 直接打印e
        
        # 通过上面三种方法都能查看异常的信息，但是稍有区别，详见代码：
        
            try:
                print(ss)
            except Exception as e:
                print(e.args)  # ("name 'ss' is not defined",)
                print(str(e))  # name 'ss' is not defined
                print(repr(e))  # NameError("name 'ss' is not defined")
                print(e)  # name 'ss' is not defined

# ----------------------------------------------------------------------------------------------------
# 3. try…except…else。

    # else 的功能：当 try 中的代码没有异常时，会调用 else 中的代码。
    
    # try...except..else 的使用和 try...except 相同，只不过多了 else 代码，else 中的代码只有当 try 中的代码块没有发现异常的时候才会调用。
    
    # 如下：
    
        a = 1
        while True:
            b = int(input('请输入除数：'))
            try:
                n = a/b
            except Exception:
                print('出现异常')
            else:
                print('程序正常执行')
                print(n)
    
    # 结果如下：
    
        # 请输入除数：0
        # 出现异常
        # 请输入除数：1
        # 程序正常执行
        # 1.0
        # 请输入除数：2
        # 程序正常执行
        # 0.5
    
    # 注意：else 中的代码只有当 try 中的代码没有出现异常时才会被执行；并且 else 要和 try…except 配合使用，如果使用了 else，则代码中不能没有 except，否则会报错。
    
        a = 1
        while True:
            b = int(input('请输入除数：'))
            try:
                n = a/b
            else:
                print('程序正常执行')
                print(n)
    
    # 由于没有 except，因此 Python 会报错：
    
        #   File "e:\code\python\py_study\tt.py", line 6
        #     else:
        #     ^
        # SyntaxError: invalid syntax

# ----------------------------------------------------------------------------------------------------
# 4. try…except…finally。

    # finally 的功能：不管 try 中的代码是否有异常，最终都会调用 finally 中的代码。
    
    # finally 可以结合 try...except，try...except...else 使用，也可以仅有 try 和 finally。
    
    # 如下：
    
        a = 1
        b = 0
        try:
            a/b
        finally:
            print('finally')
    
    # 结果：
    
        # finally
        # Traceback (most recent call last):
        #   File "e:\code\python\py_study\tt.py", line 4, in <module>
        #     a/b
        # ZeroDivisionError: division by zero
    
    # 由于没有 except 处理错误，Python 会抛出异常，但是你会发现，Python 在抛出异常之前先执行 finally 中的代码。
    
    # 同时，还需要注意一点的是，一定要避免在 finally 中编写 return，raise 等会终止函数的语句。否则很容易会产生不符合预期的操作。

# ----------------------------------------------------------------------------------------------------
# EOF
