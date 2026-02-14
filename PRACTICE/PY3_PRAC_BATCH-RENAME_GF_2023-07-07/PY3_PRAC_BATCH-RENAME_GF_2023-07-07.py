# PY3_PRAC_BATCH-RENAME_GF_2023-07-07.py
# Create by GF 2023-07-07

# ##################################################

import os
import re

# ##################################################

def FuncRecursiveFile(VarSrcPath:str):

    ListFilePath = []
    
    # ..............................................
    # for 循环中的 root 获取路径下的每个目录及子目录路径。
    # for 循环中的 file 获取目录及子目录下每个文件并返回为列表。
    for root, directories, file in os.walk(VarSrcPath):
        # ..........................................
        for filename in file:
            filepath = os.path.join(root, filename)       
            print("Source File : %s" % filepath)      
            ListFilePath.append(filepath)

    # ..............................................
    return ListFilePath

def FuncBatchRename(ListFilePath:list, VarOutPutPath:str):

    ListEndsNum = [i for i in range(0, len(ListFilePath))]

    for FilePath, EndsNum in zip(ListFilePath, ListEndsNum):
        
        # 正则表达式库方法 re.search() 只提取第一个匹配项。
        EndWith = re.search("\.jpg$|\.png$", FilePath).group()
        
        # 格式控制使用 "%03d" 表示宽度为3位，不足两位在前面补0。
        print(r"Export File : %s\%s-%03d%s" % (VarOutPutPath, "图像", EndsNum, EndWith))
        
        # OS库 os.rename(src, dst) 其中 src 为要修改的目录名，dst 为修改后的目录名。
        os.rename(FilePath, (r"%s\%s-%03d%s" % (VarOutPutPath, "图像", EndsNum, EndWith)))

def Running():

    VarSrcPath = str
    print("Please Input Source Path :")
    VarSrcPath = input()
    
    VarExpPath = str
    print("Please Input Export Path :")
    VarExpPath = input()
    
    print("--------------------------------------------------")
    
    ListFilePath = FuncRecursiveFile(VarSrcPath)
    
    print("--------------------------------------------------")
    
    FuncBatchRename(ListFilePath, VarExpPath)

# ##################################################

# 文件作为脚本直接执行，才执行以下条件。
# 将此脚本 import 到其他的 Python 脚本中被调用（模块重用）则不执行以下条件。
if __name__ == '__main__':

    Running()

# ##################################################
# EOF
