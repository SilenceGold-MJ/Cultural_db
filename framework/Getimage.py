import os,imghdr,shutil
from framework.Query_DB import Query_DB
from framework.logger import Logger
logger = Logger(logger="Getimage").getlog()


def Getimage(rootdir):#所有文件列表
    _files = []
    dirs=[]
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])  # 合并路径，将rootdir和list合并
        if os.path.isdir(path):
            _files.extend(Getimage(path)[0]) # 递归调用函数
            dirs.extend(Getimage(path)[1])
        if os.path.isfile(path):
            if imghdr.what(path) in ["bmp", "jpg", "png", "gif", "jpeg"]:
                _files.append(path)
                dirs.append(int(path.split('\\')[-2]))

    return [_files,dirs]


def Pathlsit(rootdir):#排序
    datalist = (Getimage(rootdir))
    testNO = list(set(datalist[1]))
    testNO.sort()
    Pathlist = []
    for i in testNO:
        for n in datalist[0]:
            if i == int(n.split('\\')[-2]):
                Pathlist.append(n)
    return Pathlist

def Failimgae(wide,code):
    newpath=os.getcwd()+"/"+"failimgae"+"/"+str(code)
    if os.path.exists(newpath):
        shutil.copyfile(wide, os.path.join(newpath,wide.split("\\")[-1]))
    else:
        os.makedirs(newpath)
        shutil.copyfile(wide, os.path.join(newpath,wide.split("\\")[-1]))

def get_failimage(test_version, test_batch):

    table_name='test_record_sheet'
    sql="select * from  %s WHERE test_version='%s' AND test_batch='%s' and Result='FAIL';" % (table_name, test_version, test_batch)
    list=Query_DB().query_db_all(sql )
    n=1
    for i in list:
        Image_Path=i['Image_Path'].replace( '/','\\')
        #print(Image_Path)
        code =Image_Path.split("\\")[-2]
        Failimgae(Image_Path,code)
        logger.info('%s/%s,复制《%s》……'%(n,len(list),Image_Path.split('\\')[-1]))
        n+=1


