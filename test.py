# -*- coding: utf-8 -*-
# !/usr/bin/python3

from framework.Sendmail import SendEmail
from framework.Shutdown import Shutdown
from framework.TestValue import *
from framework.Statistics import *
from framework.logger import Logger

logger = Logger(logger="run").getlog()


threshold = 0.95  # 汇总页达标率阈值
filepath = '文物识别算法准确率测试.xlsx'
pathimage = r'D:\Python\python3\文物识别批量测试\8.6日拍摄测试样本照片（批处理）'
proce = 3  # 测试进程数
Test_Batch = '20200619_1'  # 测试批次
Test_Version = 'v1.0_201912181512'  # 测试版本


if __name__ == '__main__':
    TestValue2(pathimage,proce,Test_Batch,Test_Version)  #数据测试写入表格
    Statistics( threshold,Test_Version,Test_Batch) # 汇总测试数据到数据库
    download(filepath, Test_Version, Test_Batch)#下载测试数据及汇总结果数据到Excel
    SendEmail().send_attach(filepath)  # 发送测试生成的结果Excel
    Shutdown(1)                         #  1判断时间为白天不自动关机，晚上执行关机；0执行完成后关机
    # input('Press Enter to exit...')
