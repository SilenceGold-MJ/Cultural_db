#!/user/bin/env python3
# -*- coding: utf-8 -*-

from framework.Query_DB import Query_DB
import time,json,os
import base64

from framework.InsertDB import InsertDB

from framework.logger import Logger

logger = Logger(logger="CulturalAPI").getlog()

class CulturalAPI():
    def get_summary_data(self,test_version, test_batch):#获取汇总的结果
        table_name='summary'
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % (table_name, test_version, test_batch)
        list_all = Query_DB().query_db_all(sql_all)
        logger.info(list_all)

        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return json.dumps(dic)

    def del_summary_data(self,dics):#删除一个汇总结果
        dic_values=list(dics.values())
        dic_keys = list(dics.keys())

        #sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % (table_name, test_version, test_batch)
        sql_all="UPDATE %s SET deletes=1 WHERE %s='%s' and %s='%s';" % (dic_values[0],dic_keys[1],dic_values[1],dic_keys[2],dic_values[2])
        list_all = Query_DB().db_all_No_return(sql_all)
        logger.info(list_all)
        #del list_all[0]['deletes']
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                # "counts": len(list_all),
                # "datalist":list_all ,
            }
        return json.dumps(dic)


    def get_results_summary_data(self,test_version, test_batch):#获取汇总页的数据
        table_name = 'results_summary'
        sql_all = "select * from  %s WHERE test_version='%s' AND test_batch='%s';" % ( table_name, test_version, test_batch)
        list_all = Query_DB().query_db_all(sql_all)
        # del list_all[0]['deletes']
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
    def get_start_recording(self):#获取版本和批次号

        sql= "select * from  %s WHERE deletes=0;" % ('algorithm_version')
        sql_batch = "select * from  %s WHERE deletes=0;" % ('sample_batch')

        list_row_version=Query_DB().query_db_all(sql )
        list_row_batch = Query_DB().query_db_all(sql_batch)
        Test_Batch=[]
        Test_Version=[]
        dicdata={}
        Test_Version.sort()
        Test_Version.sort()
        for i in list_row_batch:

            Test_Batch.append(i['batch'])
            dicdata.update({i['batch']:i})

        for i in list_row_version:
            Test_Version.append(i['version'])

        dic = {
                "message": "操作成功",
                "result_code": "0000",
                #"counts": len(list_row),
                'Test_Batch':list(set(Test_Batch)),
                'Test_Version':list(set(Test_Version)),
                #"datalist":list_row ,
                'dicdata':dicdata
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
        version,Test_Time,developer,deletes= dic_value
        Test_Time=Test_Time.replace('T'," ")
        sql_chachong="select count(*) from   %s WHERE version='%s';"%(table_name,version)
        sql_chachong_0 = "select count(*) from   %s WHERE deletes=0 and version='%s';" % (table_name, version)
        sql_chachong_1 = "select count(*) from   %s WHERE deletes=1 and version='%s';" % (table_name, version)

        if Query_DB().getnum(sql_chachong_0) != 0:#显示的存在，提示已存在
            dic = {
                "message": "该版本号在数据库中已存在，请重新添加！",
                "result_code": "0001",
                "datalist": [],
            }
            return json.dumps(dic)

        elif Query_DB().getnum(sql_chachong_1)!= 0:#不显示的存在，更新它

            sql = "UPDATE  %s SET version='%s',Test_Time='%s',developer='%s',deletes=%s WHERE version='%s';" % (
                table_name, version, Test_Time, developer, deletes,version)

            logger.info(sql)
            InsertDB().insert_all_data(sql)
            dic = {
                "message": "操作成功",
                "result_code": "0000",
                "datalist": [],
            }
            return json.dumps(dic)

        elif Query_DB().getnum(sql_chachong)==0:#均不在的插入

            # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])
            # SQL 插入语句
            sql = "INSERT INTO  %s (version,Test_Time,developer,deletes) \
                       VALUES ('%s','%s','%s',%s)" % \
                  (table_name, version, Test_Time, developer, deletes)
            logger.info(sql)
            InsertDB().insert_all_data(sql)
            dic = {
                "message": "操作成功",
                "result_code": "0000",
                "datalist": [],
            }
            return json.dumps(dic)


    def SampleBatch(self,dicdata):#添加样本
        table_name='sample_batch'
        dic_value = list(dicdata.values())
        batch,types_num,total_num,Test_Time,deletes,batch_path= dic_value

        Test_Time=Test_Time.replace('T'," ")


        sql_chachong_0="select count(*) from   %s WHERE deletes=0 and batch='%s';"%(table_name,batch)
        sql_chachong_1="select count(*) from   %s WHERE deletes=1 and batch='%s';"%(table_name,batch)
        sql_chachong = "select count(*) from   %s WHERE  batch='%s';" % (table_name, batch)
        if Query_DB().getnum(sql_chachong_0) != 0:
            dic = {
                "message": "该批次样本在数据库中已存在，请重新添加！",
                "result_code": "0001",
                "datalist": [],
            }
            return json.dumps(dic)

        elif Query_DB().getnum(sql_chachong_1)!= 0:
            # sql = "UPDATE  %s SET (batch,types_num,total_num,Test_Time,deletes,batch_path) \
            #            VALUES ('%s',%s,%s,'%s',%s,'%s') WHERE batch=%s;" % \
            #       (table_name, batch,types_num,total_num,Test_Time,deletes,batch_path,batch)
            sql = "UPDATE  %s SET batch='%s',types_num=%s,total_num=%s,Test_Time='%s',deletes=%s,batch_path='%s' WHERE batch='%s';" % (
            table_name, batch, types_num, total_num, Test_Time, deletes, batch_path, batch)
            InsertDB().insert_all_data(sql)
            dic = {
                "message": "操作成功",
                "result_code": "0000",
                "datalist": [],
            }
            return json.dumps(dic)


        elif Query_DB().getnum(sql_chachong)== 0:
            # logger.info([test_batch, test_version, test_time, template, test_chart, expected_range, test_type, test_value, Timeconsuming, result, Color, Template_path, TestChart_path])
            # SQL 插入语句
            sql = "INSERT INTO  %s (batch,types_num,total_num,Test_Time,deletes,batch_path)  VALUES ('%s',%s,%s,'%s',%s,'%s')" % \
                  (table_name, batch, types_num, total_num, Test_Time, deletes, batch_path)
            InsertDB().insert_all_data(sql)
            dic = {
                "message": "操作成功",
                "result_code": "0000",
                "datalist": [],
            }
            return json.dumps(dic)



    def download_excle(self,dic):#获取结果页数据
        from framework.Statistics import Statistics

        dic_value = list(dic.values())
        filenames, Test_Version, Test_Batch = dic_value
        filename = '%s_%s.xlsx' % (Test_Batch, Test_Version)
        filepath=os.getcwd() + '\\excle\\'+ filename
        logger.info(filepath)
        try:
            if os.path.exists(filepath)==True:
                logger.info('excle存在，不需要后台导出excle')
                pass
            else:
                logger.info('excle不存在，需要后台导出excle')
                Statistics().download(filename, Test_Version, Test_Batch)  # 下载测试数据及汇总结果数据到Excel
            with open(filepath, "rb") as f:
                # b64encode是编码，b64decode是解码
                base64_data = base64.b64encode(f.read())
                str_base64 = str(base64_data, 'utf-8')
                dic = {
                    "message": "操作成功",
                    "result_code": "0000",
                    "datalist": {'filename':filename,
                                 'filebase64':str_base64,
                                 }
                }
                logger.info(dic)
                return json.dumps(dic)


        except Exception as e:
            dic = {
                "message": "操作异常%s" % e,
                "result_code": "4000",
                "datalist": [],
            }
            return json.dumps(dic)

    def getform(self,dic):#获取数据

        sql_all = "select * from  %s WHERE deletes=0  ORDER BY  %s  DESC;" % ( dic['table_name'],dic['Latest_name'])
        list_all = Query_DB().query_db_all(sql_all)
        dic = {
                "message": "操作成功",
                "result_code": "0000",
                "counts": len(list_all),
                "datalist":list_all ,
            }
        return json.dumps(dic)
