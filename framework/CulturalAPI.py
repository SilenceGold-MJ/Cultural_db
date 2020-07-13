#!/user/bin/env python3
# -*- coding: utf-8 -*-
from framework.Query_DB import Query_DB
import time
from framework.logger import Logger
logger = Logger(logger="CulturalAPI").getlog()

class CulturalAPI():
    def get_summary_data(self,test_version, test_batch):#获取汇总的总数据
        table_name='summary'
        list_row=Query_DB().query_db_rowlist(table_name, test_version, test_batch,4)
        list_row.sort()
        timelist=[]
        datalist={}
        for i in list_row:
            Test_Time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(i))
            sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s' and Test_Time='%s';" % (table_name, test_version, test_batch,Test_Time)
            list_all = Query_DB().query_db_all(sql_all)[0]
            if Test_Time not in timelist:
                timelist.append(Test_Time)
                datalist.update({Test_Time:list_all})
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_row),
                'time': timelist,
                "datalist":datalist ,
            }
        return dic



    def get_results_summary_data(self,test_version, test_batch):#获取汇总页的数据
        table_name = 'results_summary'
        list_row=Query_DB().query_db_rowlist(table_name, test_version, test_batch,5)
        list_row.sort()

        timelist=[]
        datalist={}
        for i in list_row:
            Test_Time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(i))
            sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s' and Test_Time='%s';" % (table_name, test_version, test_batch,Test_Time)
            list_all = Query_DB().query_db_all(sql_all)
            if Test_Time not in timelist:
                timelist.append(Test_Time)
                datalist.update({Test_Time:list_all})
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_row),
                'time': timelist,
                "datalist":datalist ,
            }
        return dic
    def get_record_sheet_data(self,test_version, test_batch):#获取测试记录页数据
        table_name = 'test_record_sheet'

        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % ( table_name, test_version, test_batch)

        list_all = Query_DB().query_db_all(sql_all)
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return dic
    def get_start_recording(self):#获取启动记录页数据
        table_name = 'start_recording'
        sql= "select * from  %s ;" % (table_name,)
        list_row=Query_DB().query_db_all(sql )
        Test_Batch=[]
        Test_Version=[]
        for i in list_row:
            Test_Batch.append(i['Test_Batch'])
            Test_Version.append(i['Test_Version'])


        dic = {
                "message": "操作成功",
                "result_code": "0000",
                #"counts": len(list_row),
                'Test_Batch':list(set(Test_Batch)),
                'Test_Version':list(set(Test_Version)),
                #"datalist":list_row ,
            }
        return dic