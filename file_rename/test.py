# _*_coding:utf-8 _*_
# @Time     :2019/8/14   17:27
# @Author   :
# @ File　　:get_webgame_info.py
# @Software :PyCharm
# @Desc     :
"""
root 所指的是当前正在遍历的这个文件夹的本身的地址
dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
"""
import os
def is_all_dir(path):
    os.chdir(path)
    for l in os.listdir(path):
        if os.path.isfile(l):
            return False
    return True
print(is_all_dir(r'C:\Users\Administrator\Desktop\test'))