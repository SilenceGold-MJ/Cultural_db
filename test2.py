# -*- coding: utf-8 -*-
# !/usr/bin/python3

from framework.Sendmail import SendEmail
from framework.Shutdown import Shutdown
from framework.TestValue import *
from framework.Statistics import *
from framework.Query_DB import Query_DB
from framework.CulturalAPI import CulturalAPI
from framework.logger import Logger

logger = Logger(logger="run").getlog()


threshold = 0.95  # 汇总页达标率阈值
filepath = '文物识别算法准确率测试.xlsx'
pathimage = r'E:\小雁塔\8.6日拍摄测试样本照片（批处理）'
proce = 3  # 测试进程数
Test_Batch = '20200713_1'  # 测试批次
Test_Version = 'v1.0_201912181512'  # 测试版本


if __name__ == '__main__':

    data=(CulturalAPI().get_summary_data(Test_Version,Test_Batch))
    data1=(CulturalAPI().get_results_summary_data(Test_Version,Test_Batch))
    print(data)
    print(data1)

    data2=CulturalAPI().get_record_sheet_data(Test_Version,Test_Batch)
    print(data2)

    data3=CulturalAPI().get_start_recording()
    print(data3)


    #TestValue2(pathimage,proce,Test_Batch,Test_Version)  #数据测试写入表格
    #Statistics( threshold,Test_Version,Test_Batch) # 汇总测试数据到数据库
    # download(filepath, Test_Version, Test_Batch)#下载测试数据及汇总结果数据到Excel
    # get_failimage(Test_Version, Test_Batch)#获取失败图片
    # SendEmail().send_attach(filepath)  # 发送测试生成的结果Excel
    # Shutdown(0)                         #  1判断时间为白天不自动关机，晚上执行关机；0执行完成后关机
    # input('Press Enter to exit...')
