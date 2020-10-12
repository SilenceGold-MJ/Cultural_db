# -*- coding: utf-8 -*-
# !/usr/bin/python3

from framework.Sendmail import SendEmail
from framework.Shutdown import Shutdown
from framework.TestValue import *
from framework.CulturalAPI import CulturalAPI
from framework.Statistics import Statistics
from framework.logger import Logger

logger = Logger(logger="run").getlog()

data=json.loads(CulturalAPI().get_start_recording())

Test_Batch ='20200713_1'  # 测试批次
Test_Version = 'v1.0_201812181345'

pathimage = data['dicdata'][Test_Batch]['batch_path']  #pathimage =r'E:\小雁塔\test'
Batchinfo=data['dicdata'][Test_Batch]#样本信息
threshold = 0.95  # 汇总页达标率阈值
filename = '%s_%s.xlsx'%(Test_Batch,Test_Version)
proce = 1  # 测试进程数



if __name__ == '__main__':
    TestValue2(pathimage,proce,Test_Batch,Test_Version,Batchinfo)  #数据测试写入表格
    Statistics().Statistics( threshold,Test_Version,Test_Batch) # 汇总测试数据到数据库
    Statistics().download(filename, Test_Version, Test_Batch)#下载测试数据及汇总结果数据到Excel
    #get_failimage(Test_Version, Test_Batch)#获取失败图片
    SendEmail().send_attach(filename)  # 发送测试生成的结果Excel
    Shutdown(2)                         #  1判断时间为白天不自动关机，晚上执行关机；0执行完成后关机；2执行完成后不会自动关机
    input('Press Enter to exit...')
