import requests
import base64
import json
import os, time, datetime
import configparser
from framework.Getimage import *
from framework.InsertDB import InsertDB
from framework.Query_DB import Query_DB
from framework.ExportExcle import *
from framework.logger import Logger
from multiprocessing import Process, Lock
from multiprocessing import Pool,Lock,Manager
import multiprocessing

logger = Logger(logger="TestValue").getlog()
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding="utf-8-sig")

def API(imagefile_path):  # 给接口图片地址返回top3的值
    with open(imagefile_path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        str_base64 = str(base64_data, 'utf-8')
        try:
            url = "https://kk.huoyanhou.com:8445/image_analysis/basic/hpTest.html"
            payload = {
                "file": str_base64, "fileName": imagefile_path.split('\\')[-1]
            }
            headers = {
                'Content-Type': "application/json",
            }
            payload = json.dumps(payload)  # 将字典类型转换为 JSON 对象，序列化
            r = requests.post(url, data=payload, headers=headers)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            top = r.text.split(',')
            dics = {"code": 2000, "message": "识别成功！", "topdata": {"top1": int(top[0]), "top2": int(top[1]), "top3": int(top[2])}}
            return json.dumps(dics)
        except Exception as e:
            dics = {"code": 4000, "message": "服务可能未开启，" + str(e), "topdata": {'top1': -99, 'top2': -99, 'top3': -99}}
            return json.dumps(dics)


def API2(imagefile_path):
    with open(imagefile_path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        str_base64 = str(base64_data, 'utf-8')
        try:
            url = "http://192.168.1.182:8888/Disc"
            # querystring = {"image_base64":str_base64,"image_name":imagefile_path.split('\\')[-1]}#imagefile_path.split('\\')[-1]#, params=querystring
            payload = {"image_base64": str_base64,
                       "image_name": imagefile_path.split('\\')[-1]}  # imagefile_path.split('\\')[-1]
            response = requests.request("post", url, data=(payload))
            return (response.text)
        except Exception as e:
            return ("服务可能未开启，" + str(e))


def Summary(imagefile_path, i,Test_Batch,Test_Version):
    Time_Stamp = int(time.time())
    now =time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(Time_Stamp))
    code = int(imagefile_path.split('\\')[-2])
    TestChart = imagefile_path.split('\\')[-1]

    try:
        T1 = datetime.datetime.now()
        topdata = json.loads(API2(imagefile_path))['topdata']

        T2 = datetime.datetime.now()
        T = round((T2 - T1).total_seconds(), 3)  # 检索耗时

    except Exception as e:
        logger.error('报错:%s' % str(e))
        topdata = {'top1': -88, 'top2': -88, 'top3': -88}
        T = 0  # 检索耗时

    TestValue1, TestValue2, TestValue3 = topdata['top1'], topdata['top2'], topdata['top3'],
    if TestValue1 == code:
        Result = ["PASS", 'c6efce_006100']
    elif TestValue1 in [-88, -99]:
        Result = ["ERROR", 'ffeb9c_9c6500']
        Failimgae(imagefile_path, code)
    else:
        Result = ["FAIL", 'ffc7ce_9c0006']
        Failimgae(imagefile_path, code)
    dic = {
        'Test_ID': i + 1,
        "Test_Batch":Test_Batch,
        'Test_Version':Test_Version,
        'Test_Time': now,
        'Time_Stamp':Time_Stamp,
        'Cultural_Name': cf.get("Data", str(code)),
        'Test_Chart': TestChart,
        'Code':int( code),
        "Expected_Value": int( code),
        'TimeConsuming': T,
        'top1': TestValue1,
        'top2': TestValue2,
        'top3': TestValue3,
        'Result': Result[0],
        'Color':Result[1],
        'Image_Path': imagefile_path.replace('\\', '/')#dic["TestChartPath"].replace('\\', '/')

    }

    return dic


def TestValue2(rootdir, proce,Test_Batch,Test_Version):#支持多进程
    Time_Stamp = int(time.time())
    now =time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(Time_Stamp))
    manager = Manager()
    lock = manager.Lock()  # 产生钥匙
    datalist=Pathlsit(rootdir)
    listPath = datalist[0]
    Total = (len(listPath))
    sql = "select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' ;" % ('test_record_sheet',Test_Version,Test_Batch)
    A = Query_DB().getnum(sql)#查询测试进度
    start_dic={"RunTime":now,"RunTime_int":Time_Stamp,"Test_Batch":Test_Batch,"Test_Version":Test_Version,"Total_Type":len(datalist[1]),"Sum_Numbers":Total,"Completed":A}
    # logger.info(start_dic)
    InsertDB().insert_Start_recording( 'start_recording', start_dic)#写入启动测试记录
    pool = multiprocessing.Pool(processes=proce)
    for i in range(A , Total):
        pool.apply_async(func=process, args=(listPath[i],Total,i,lock,Test_Batch,Test_Version))
    pool.close()
    pool.join()  # 在join之前一定要调用close，否则报错

def process(imagefile_path,Total,i,lock,Test_Batch,Test_Version):

    dic = Summary(imagefile_path, i,Test_Batch,Test_Version)
    lock.acquire()  ##拿到钥匙进门,其他进程阻塞, acqurie和release之间的代码只能被一个进程执行
    #SummaryExcle(addr, dic, title, 10)
    InsertDB().insert_data('test_record_sheet',  dic)#插入数据库测试记录数据
    lock.release()  # 释放钥匙
    #logger.info(dic)
    logger.info('测试进度：%s/%s；测试图：%s；编号：%s；耗时：%s；top3：%s、%s、%s；测试结果：%s。' % (
        i + 1, Total, dic['Test_Chart'], dic['Code'], dic['TimeConsuming'], dic['top1'], dic['top2'],
        dic['top3'], dic['Result']))



