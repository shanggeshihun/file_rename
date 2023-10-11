# _*_coding:utf-8 _*_
# @Time     :2019/8/14   11:04
# @Author   :
# @ File　　:rename.py
# @Software :PyCharm
# @Desc     :重命名图片并归类值所属镇
import os
import pandas as pd

def del_children_files(path):
    """
    :递归删除该文件夹下所有文件及文件夹
    :param path: 目录
    :return: 无
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def is_all_dir(path):
    """
    :param path:
    :return: 文件夹下是否全部是文件下
    """
    os.chdir(path)
    for l in os.listdir(path):
        if os.path.isfile(l):
            return False
    return True

def pict_saveas_to(excel_path, desti_pict_dir_path, origi_pict_dir_path, error_dir_path):
    """
    excel_path:网格.xls路径
    desti_pict_dir_path:图片重命名后存放的最外层文件夹路径
    origi_pict_dir_path:原图片所在的文件夹路径
    error_dir_path:重命名失败图片存放文件夹路径
    """
    xls = pd.read_excel(excel_path)
    df = xls[['OID', 'zhenjie', 'name']]
    dir_zhenjie_list = df.drop_duplicates('zhenjie').zhenjie

    # 根据 OID 建立 zhenjie name 映射关系
    id_zhenjie_mapping = {}
    id_name_mapping = {}
    for i, row in df.iterrows():
        id = row['OID']
        zhenjie = row['zhenjie']
        name = row['name']
        id_zhenjie_mapping[id] = zhenjie
        id_name_mapping[id] = name

    # 切至重命名图片所在的父目录 并 清空
    os.chdir(desti_pict_dir_path)
    if is_all_dir(desti_pict_dir_path):
        del_children_files(desti_pict_dir_path)
    else:
        print('desti_pict_dir_path输入路径可能有无')
        os._exit(0)
    # 按照镇 新建 父目录下的子目录
    for zhen in dir_zhenjie_list:
        os.mkdir(zhen)
    import shutil
    # 图片重命名前 所在文件夹
    error_path_pair = []
    for path in os.listdir(origi_pict_dir_path):
        id, extension = os.path.splitext(path)
        # 只针对图片形式的拓展名进行处理
        if extension == '.png' or extension == '.jpg':
            to_dir = id_zhenjie_mapping[int(id)]
            to_name = id_name_mapping[int(id)]
            # 图片原路径
            pict_dir_name_path = os.path.join(origi_pict_dir_path, path)
            # 图片处理后路径
            to_dir_name_path = os.path.join(desti_pict_dir_path, to_dir, to_name + '.jpg')
            # 复制另存为
            try:
                shutil.copy(pict_dir_name_path, to_dir_name_path)
            except:
                error_path_pair.append((pict_dir_name_path, to_dir_name_path))
    path_pair_df = pd.DataFrame(error_path_pair)
    # 写入异常记录表 文件夹
    error_basename = r"error_path_pair.xls"
    error_path = os.path.join(error_dir_path, error_basename)
    path_pair_df.to_excel(error_path)

if __name__ == '__main__':
    excel_path = input("输入《网格.xls》路径，如: E:\\网格.xls >>>")
    desti_pict_dir_path = input("输入 图片重命名后存放的最外层文件夹路径，如: D:\\500_1 >>>")
    origi_pict_dir_path = input("输入 原图片所在的文件夹路径，如: E:\\500_1 >>>")
    error_dir_path = input("输入 重命名失败图片存放文件夹路径，如:C:\\Users\\Administrator\\Desktop >>>")
    pict_saveas_to(excel_path, desti_pict_dir_path, origi_pict_dir_path, error_dir_path)
	
	
def file_info(path):
    """
    :param path:
    :return:文件信息字典
    """
    info_dict={}
    tmp={}
    path_info=os.stat(path)
    modified_time=path_info.st_mtime # 最后一次修改的时间
    mtime_array=time.localtime(modified_time)
    modified_time_=time.strftime('%Y-%m-%d %H:%M:%S',mtime_array)

    create_time=path_info.st_ctime # 最后一次修改的时间
    ctime_array=time.localtime(create_time)
    create_time_=time.strftime('%Y-%m-%d %H:%M:%S',ctime_array)

    base_name=os.path.basename(path) # 文件名+拓展名
    file_name=base_name.split('.')[0] # 文件名
    tmp['base_name']=base_name
    tmp['file_name']=file_name
    tmp['modified_time']=modified_time_
    tmp['create_time']=create_time_
    info_dict[path]=tmp
    return info_dict