#!/user/bin/env python3
# -*- coding: utf-8 -*-
from framework.Query_DB import Query_DB
import time,json
from framework.InsertDB import InsertDB
from framework.logger import Logger
logger = Logger(logger="CulturalAPI").getlog()

class CulturalAPI():
    def get_summary_data(self,test_version, test_batch):#获取汇总的结果
        table_name='summary'
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % (table_name, test_version, test_batch)
        list_all = Query_DB().query_db_all(sql_all)
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return json.dumps(dic)



    def get_results_summary_data(self,test_version, test_batch):#获取汇总页的数据
        table_name = 'results_summary'
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % ( table_name, test_version, test_batch)
        list_all = Query_DB().query_db_all(sql_all)
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return json.dumps(dic)
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
        return json.dumps(dic)
    def get_start_recording(self):#获取启动记录页数据

        sql= "select * from  %s ;" % ('algorithm_version')
        sql_batch = "select * from  %s ;" % ('sample_batch')
        list_row_version=Query_DB().query_db_all(sql )
        list_row_batch = Query_DB().query_db_all(sql_batch)
        Test_Batch=[]
        Test_Version=[]
        for i in list_row_batch:
            logger.info(i)
            Test_Batch.append(i['batch'])
        for i in list_row_version:
            Test_Version.append(i['version'])

        dic = {
                "message": "操作成功",
                "result_code": "0000",
                #"counts": len(list_row),
                'Test_Batch':list(set(Test_Batch)),
                'Test_Version':list(set(Test_Version)),
                #"datalist":list_row ,
            }
        return json.dumps(dic)

    def get_one_sheet_data(self,dicdata):#获取测试记录页数据
        test_version, test_batch, Code=list(dicdata.values())
        table_name = 'test_record_sheet'
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s' AND Code=%s;" % ( table_name, test_version, test_batch,Code)
        list_all = Query_DB().query_db_all(sql_all)
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return json.dumps(dic)
    def get_pic_data(self,dicdata):#获取测试记录页数据

        table_name = 'test_record_sheet'
        test_version, test_batch, Code,Test_Chart=list(dicdata.values())
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s' AND Code=%s AND Test_Chart='%s';" % ( table_name, test_version, test_batch,Code,Test_Chart)
        list_all = Query_DB().query_db_all(sql_all)
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return json.dumps(dic)

    def Linechart(self,test_version, test_batch):
        dicdata={"文物编号":[],
                       "准确率":[],
                       "文物名称":[]}
        table_name = 'results_summary'
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % ( table_name, test_version, test_batch)
        list_all = Query_DB().query_db_all(sql_all)
        for i in list_all:
            dicdata["文物编号"].append(i['Code'])
            dicdata["准确率"].append(i['Accuracy'])
            dicdata["文物名称"].append('')#i['Cultural_Name']


        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "datalist":dicdata ,
            }
        return json.dumps(dic)

    def Proportion_zb(self,test_version, test_batch):
        dic_test={
            '0~10%':'AND Accuracy <=0.1',
            '10%~30%':'And 0.1<Accuracy And Accuracy<=0.3',
            '30%~50%': 'And 0.3<Accuracy And Accuracy<=0.5 ',
            '50%~60%':'And 0.5<Accuracy And Accuracy<=0.6 ',
            '60%~70%': 'And 0.6<Accuracy And Accuracy<=0.7 ',
            '70%~80%': 'And 0.7<Accuracy And Accuracy<=0.8 ',
            '80%~90%': 'And 0.8<Accuracy And Accuracy<=0.9 ',
            '90%~95%': 'And 0.9<Accuracy And Accuracy<=0.95 ',
            '95%~100%': 'And 0.95<Accuracy And Accuracy<=1 ',
        }
        listdata=[]
        for k, v in dic_test.items():
            sql = "select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' %s ;" % ('results_summary', test_version, test_batch,v)
            print(sql)
            num = Query_DB().getnum(sql)  # 查询测试进度
            listdata.append([k, str(num)])
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "datalist":listdata ,
            }
        return json.dumps(dic)

    def Addtestinfo(self,dicdata):#添加算法
        table_name='algorithm_version'
        dic_value = list(dicdata.values())
        version,release_time,developer,deletes= dic_value
        sql_chachong="select count(*) from   %s WHERE version='%s';"%(table_name,version)
        if Query_DB().getnum(sql_chachong)==0:

            # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])
            # SQL 插入语句
            sql = "INSERT INTO  %s (version,release_time,developer,deletes) \
                       VALUES ('%s','%s','%s',%s)" % \
                  (table_name, version, release_time, developer, deletes)
            try:
                logger.info(sql)
                InsertDB().insert_all_data(sql)
                dic = {
                    "message": "操作成功",
                    "result_code": "0000",
                    "datalist": [],
                }
                return json.dumps(dic)
            except Exception as e:
                dic = {
                    "message": "操作异常%s" % e,
                    "result_code": "4000",
                    "datalist": [],
                }
                return json.dumps(dic)
        else:
            dic = {
                "message": "该版本号在数据库中已存在，请重新添加！",
                "result_code": "0001",
                "datalist": [],
            }
            return json.dumps(dic)


    def SampleBatch(self,dicdata):#添加样本
        table_name='sample_batch'
        dic_value = list(dicdata.values())
        batch,types_num,total_num,batch_date,deletes,batch_path= dic_value
        sql_chachong="select count(*) from   %s WHERE batch='%s';"%(table_name,batch)
        print(sql_chachong)
        if Query_DB().getnum(sql_chachong)==0:
            # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])
            # SQL 插入语句
            sql = "INSERT INTO  %s (batch,types_num,total_num,batch_date,deletes,batch_path) \
                       VALUES ('%s',%s,%s,'%s',%s,'%s')" % \
                  (table_name, batch,types_num,total_num,batch_date,deletes,batch_path)
            try:
                logger.info(sql)
                InsertDB().insert_all_data(sql)
                dic = {
                    "message": "操作成功",
                    "result_code": "0000",
                    "datalist": [],
                }
                return json.dumps(dic)
            except Exception as e:
                dic = {
                    "message": "操作异常%s" % e,
                    "result_code": "4000",
                    "datalist": [],
                }
                return json.dumps(dic)
        else:
            dic = {
                "message": "该批次样本在数据库中已存在，请重新添加！",
                "result_code": "0001",
                "datalist": [],
            }
            return json.dumps(dic)
