#!/user/bin/env python3
# -*- coding: utf-8 -*-
import pymysql

from framework.logger import Logger
logger = Logger(logger="InsertDB").getlog()

import configparser,os
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath,encoding="utf-8-sig")

host=cf.get("DATABASE", "host")
user=cf.get("DATABASE", "user")
password=cf.get("DATABASE", "password")
DB=cf.get("DATABASE", "DB")
port=cf.get("DATABASE", "port")
class InsertDB():
    def insert_data(self,table_name,dicdata):#插入测试记录数据
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        dic_value=list(dicdata.values())
        Test_ID,Test_Batch,Test_Version,Test_Time,Time_Stamp,Cultural_Name,Test_Chart,Code,Expected_Value,TimeConsuming,top1,top2,top3,Result,Color,Image_Path = dic_value

        # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])

        # SQL 插入语句
        sql = "INSERT INTO  %s (Test_ID,Test_Batch,Test_Version,Test_Time,Time_Stamp,Cultural_Name,Test_Chart,Code,Expected_Value,TimeConsuming,top1,top2,top3,Result,Color,Image_Path) \
                   VALUES (%s,'%s','%s','%s',%s,'%s', '%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s')" % \
              (table_name, Test_ID,Test_Batch,Test_Version,Test_Time,Time_Stamp,Cultural_Name,Test_Chart,Code,Expected_Value,TimeConsuming,top1,top2,top3,Result,Color,Image_Path)
        try:
            # 执行sql语句
            # print(sql)
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            # cursor.connection.commit()  # 执行commit操作，插入语句才能生效

        except:
            # 发生错误时回滚
            db.rollback()

        # cursor.close()
        # 关闭数据库连接
        db.close()



    def insert_Result(self,table_name,dicdata):#插入汇总页数据
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        dic_value=list(dicdata.values())
        Test_ID,Test_Batch,Test_Version,Test_Time,Time_Stamp,Cultural_Name,Code,Test_Number,PASS,FAIL,ERROR,Accuracy,Color = dic_value

        # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])

        # SQL 插入语句
        sql = "INSERT INTO  %s (Test_ID,Test_Batch,Test_Version,Test_Time,Time_Stamp,Cultural_Name,Code,Test_Number,PASS,FAIL,ERROR,Accuracy,Color) \
                   VALUES (%s,'%s','%s','%s',%s,'%s', %s,%s,%s,%s,%s,%s,'%s')" % \
              (table_name, Test_ID,Test_Batch,Test_Version,Test_Time,Time_Stamp,Cultural_Name,Code,Test_Number,PASS,FAIL,ERROR,Accuracy,Color)
        try:
            # 执行sql语句
            # print(sql)
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            # cursor.connection.commit()  # 执行commit操作，插入语句才能生效

        except:
            # 发生错误时回滚
            db.rollback()

        # cursor.close()
        # 关闭数据库连接
        db.close()

    def insert_summary(self, table_name, dicdata):  # 插入汇总语数据
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        dic_value = list(dicdata.values())
        Test_Batch,Test_Version,Test_Time,Time_Stamp,Total_Type,Sum_Numbers,Sum_Pass,Sum_Fail,Standard,UnStandard,threshold,StandardRate= dic_value
        # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])
        # SQL 插入语句
        sql = "INSERT INTO  %s (Test_Batch,Test_Version,Test_Time,Time_Stamp,Total_Type,Sum_Numbers,Sum_Pass,Sum_Fail,Standard,UnStandard,threshold,StandardRate) \
                   VALUES ('%s','%s','%s',%s,%s,%s, %s,%s,%s,%s,%s,%s)" % \
              (table_name, Test_Batch,Test_Version,Test_Time,Time_Stamp,Total_Type,Sum_Numbers,Sum_Pass,Sum_Fail,Standard,UnStandard,threshold,StandardRate)
        try:
            # 执行sql语句
            #print(sql)
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            # cursor.connection.commit()  # 执行commit操作，插入语句才能生效

        except:
            # 发生错误时回滚
            db.rollback()

        # cursor.close()
        # 关闭数据库连接
        db.close()
    def insert_Start_recording(self, table_name, dicdata):  # 插入启动记录
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        dic_value = list(dicdata.values())
        RunTime,RunTime_int,Test_Batch,Test_Version,Total_Type,Sum_Numbers,Completed= dic_value
        # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])
        # SQL 插入语句
        sql = "INSERT INTO  %s (RunTime,RunTime_int,Test_Batch,Test_Version,Total_Type,Sum_Numbers,Completed) \
                   VALUES ('%s',%s,'%s','%s',%s,%s,%s)" % \
              (table_name, RunTime,RunTime_int,Test_Batch,Test_Version,Total_Type,Sum_Numbers,Completed)
        try:
            # 执行sql语句
            #print(sql)
            cursor.execute(sql)

            # 执行sql语句
            db.commit()
            # cursor.connection.commit()  # 执行commit操作，插入语句才能生效

        except:
            # 发生错误时回滚
            db.rollback()

        # cursor.close()
        # 关闭数据库连接
        db.close()