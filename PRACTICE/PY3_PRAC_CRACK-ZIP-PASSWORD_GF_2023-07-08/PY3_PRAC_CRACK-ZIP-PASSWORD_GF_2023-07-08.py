# PY3_PRAC_CRACK-ZIP-PASSWORD_GF_2023-07-08.py
# Create by GF 2023-07-08 00:18

# ##################################################

import zipfile
import itertools

# ##################################################
# 使用 zipfile.ZipFile() 时，参数为文件的路径与文件名组成的字符串。

# CompressFile = zipfile.ZipFile(r'D:\test.zip')

# ##################################################
# 调用 .namelist 方法可以得到压缩包里面的所有文件名。

# ListCompressFile = CompressFile.namelist()

# ##################################################
# 调用 .extract 方法并配合 for 循环解压文件到指定目录。

# for FileName in ListCompressFile:
#     CompressFile.extract(FileName, r'D:\Dist', pwd="123456".encode("utf-8"))

# ##################################################
# 当使用 zipfile 解压非加密 ZIP 压缩包时，只需修改：
# CompressFile.extract(FileName, r"D:\Dist", pwd="123".encode("utf-8"))
# 为：
# CompressFile.extract(FileName, r"D:\Dist")

# ##################################################
# 不再使用ZIP压缩文件时，关闭文件，释放内存（必须）。
# CompressFile.close()

# ##################################################
# Notice

# 调用 zipfile 对传统加密的 ZIP 文件进行解压可以成功（传统加密 : CRC32 也即 ZIP 2.0）。
# 但是当 ZIP 为非传统加密方式时无法解压（非传统加密 : AES-256）。
# 这里的传统加密指的什么呢？
# 使用版本比较新的 WinRAR 进行 ZIP 加密压缩的时候，下面会有一个“ZIP传统加密”的选项。
# 自带的 zipfile 模块只支持 CRC32 加密的 ZIP 文件，pyzipper 三方库可以读写 AES 加密的 ZIP 文件。

# ##################################################
# 在跳过一些错误的时候，密码本身会导致错误，所以将未尝试过的密码加入到 ListNotAttemptedPassword 列表。

# 使用密码为："2ff0" 会导致 zlib.error: Error -3
# zlib.error: Error -3 while decompressing data: invalid block type

# 使用密码为："2g0e" 会导致 zlib.error: Error -3
# zlib.error: Error -3 while decompressing data: invalid code lengths set

# 使用密码为："eege" 会导致 zlib.error: Error -3
# zlib.error: Error -3 while decompressing data: invalid stored block lengths

ListNotAttemptedPassword = []

# ##################################################

ListPasswordDict = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

ListCartesian = list(itertools.product(ListPasswordDict, ListPasswordDict,
                                       ListPasswordDict, ListPasswordDict)
                     )

def FuncOpenZip(VarZipPath:str):

    CompressFile = zipfile.ZipFile(VarZipPath, 'r')    
    # ..............................................
    return CompressFile
    
def FuncListZipContents(VarZipPath:str):

    CompressFile = FuncOpenZip(VarZipPath)
    # ..............................................
    ListCompressFile = CompressFile.namelist()
    # ..............................................
    return ListCompressFile

def FuncUnZip(VarZipPath:str):

    CompressFile = FuncOpenZip(VarZipPath)
    # ..............................................
    ListCompressFile = FuncListZipContents(VarZipPath)
    # ..............................................
    for FileName in ListCompressFile:
        CompressFile.extract(FileName, r'D:\Dist')
        # ..........................................
        print("Extract File : %s" % FileName)
    
def FuncUnEncryptedZip(VarZipPath:str, VarPassword:str):

    try:
        CompressFile = zipfile.ZipFile(VarZipPath, 'r')
        # ..........................................
        ListCompressFile = CompressFile.namelist()
        # ..........................................
        CompressFile.extract(ListCompressFile[0], r'D:\dist', pwd=VarPassword.encode("utf-8"))
    except RuntimeError as e:
        #print(e.args)
        # ..........................................
        CompressFile.close()
        # ..........................................
        # 如果尝试使用密码解压失败，则返回 False。
        return False
    except Exception:
        CompressFile.close()
        # ..........................................
        # 出现其它错误 (非值错误)，则返回 False。
        ListNotAttemptedPassword.append(VarPassword)
        # ..........................................
        return "Non Value Error"
    else:
        CompressFile.close()
        # ..........................................
        # 如果尝试使用密码解压成功，则返回 True。
        return True
    # ..............................................
    # End

def FuncCrackZip(VarZipPath:str):

    Index = 0
    # ..............................................
    while 0 < len(ListCartesian):
        TryPassword = str().join(ListCartesian[Index])
        # ..........................................
        TryPasswordResult = FuncUnEncryptedZip(VarZipPath, TryPassword)
        # ..........................................
        if TryPasswordResult == True:
            print("Password Attempt Successful, Correct Password is %s" % TryPassword)
            # ------------------------------------------
            break
        elif TryPasswordResult == "Non Value Error":
            print("Unable to Try The %sth Password (Non Value Error)..." % Index)
            # ------------------------------------------
            Index += 1
        else:
            print("Attempting %sth Password..." % Index)
            # ------------------------------------------
            Index += 1
    # ..............................................
    # End
   
def Running():

    VarZipPath = r"D:\\PY3-CRACK-EXAMPLE-ZIP-4-DIGIT-CRC32.zip"

    #FuncOpenZip(VarZipPath)

    #FuncListZipContents(VarZipPath)

    #FuncUnZip(VarZipPath)
    
    FuncCrackZip(VarZipPath)
    
if __name__ == "__main__":

    Running()
    
# ##################################################
# EOF
