import configparser, os,time
from framework.ExportExcle import *
from framework.Query_DB import Query_DB
from framework.InsertDB import InsertDB
from framework.CulturalAPI import CulturalAPI
from framework.logger import Logger

logger = Logger(logger="Statistics").getlog()
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding="utf-8-sig")


def results_summary( threshold,Test_Version,Test_Batch,Time_Stamp):#获取汇总测试数据
    now = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(Time_Stamp))
    table_name1='test_record_sheet'
    Codelist=Query_DB().query_db_rowlist(table_name1, Test_Version, Test_Batch, 8)#获取值列表

    datalist=[]
    for i in range(len(Codelist)):
        sql_pass= "select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' AND Code=%s AND Result='PASS';" % (table_name1, Test_Version,Test_Batch,Codelist[i])
        sql_num ="select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' AND Code=%s ;" % (table_name1, Test_Version,Test_Batch,Codelist[i])
        sql_fial="select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' AND Code=%s AND Result='FAIL';" % (table_name1, Test_Version,Test_Batch,Codelist[i])
        sql_error ="select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' AND Code=%s AND Result='ERROR';" % (table_name1, Test_Version,Test_Batch,Codelist[i])

        Test_Number= Query_DB().getnum(sql_num)
        PASS=Query_DB().getnum(sql_pass)
        FAIL=Query_DB().getnum(sql_fial)
        ERROR=Query_DB().getnum(sql_error)
        Accuracy =PASS/ Test_Number
        if Accuracy >= threshold:
            Accuracylist =[Accuracy,'c6efce_006100']   # ["%.2f%%" % (Accuracy * 100), ['c6efce','006100']]
        else:
            Accuracylist = [Accuracy,'ffc7ce_9c0006']    #["%.2f%%" % (Accuracy * 100), ['ffc7ce', '9c0006']]

        dic = {
            'Test_ID': i+1,
            'Test_Batch':Test_Batch,
            'Test_Version': Test_Version,
            'Test_Time':now,
            'Time_Stamp':Time_Stamp,
            'Cultural_Name': cf.get("Data", str(Codelist[i])),
            'Code': Codelist[i],
            'Test_Number': Test_Number,
            'PASS': PASS,
            "FAIL": FAIL,
            'ERROR': ERROR,
            'Accuracy': Accuracylist[0],
            'Color':Accuracylist[1]
        }
        logger.info(dic)
        datalist.append(dic)
        #InsertDB().insert_Result('results_summary', dic)

    return datalist



def summary_hz( threshold,Test_Version,Test_Batch,Time_Stamp):#读写汇总页数据，输出汇总语数据
    now = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(Time_Stamp))
    data=CulturalAPI().get_results_summary_data(Test_Version,Test_Batch)
    datalist=data['datalist'][data['time'][-1]]
    SumNumbers = []
    SumPass = []
    SumFail = []
    Standard = []
    UnStandard = []
    for i in datalist:
        SumNumbers.append(i['Test_Number'])
        SumPass .append(i['PASS'])
        SumFail.append(i['FAIL'])
        if i['Accuracy']>=threshold:
            Standard .append(i['Accuracy'])
        else:
            UnStandard .append(i['Accuracy'])
    dic_hz = {
        'Test_Batch': Test_Batch,
        'Test_Version': Test_Version,
        'Test_Time': now,
        'Time_Stamp':Time_Stamp,
        'Total_Type':len(SumNumbers),
        'Sum_Numbers': sum(SumNumbers),
        'Sum_Pass': sum(SumPass),
        'Sum_Fail':  sum(SumFail),
        'Standard':  len(Standard),
        'UnStandard': len(UnStandard),
        'threshold': threshold,
        'StandardRate': len(Standard) / len(SumNumbers),
    }
    InsertDB().insert_summary( 'summary', dic_hz)

def Statistics( threshold,Test_Version,Test_Batch):
    Time_Stamp = int(time.time())
    sql =  "select * from  %s WHERE test_version='%s' AND test_batch='%s' ;" % ('start_recording', Test_Version, Test_Batch)
    Total_Type=Query_DB().query_db_all( sql)[-1]['Total_Type']#查测试类型数
    sql = "select count(*) from  %s WHERE test_version='%s' AND test_batch='%s' ;" % ('results_summary',Test_Version,Test_Batch)
    A = Query_DB().getnum(sql)#查询汇总进度
    if  Total_Type>A:
        datalist = results_summary(threshold, Test_Version, Test_Batch, Time_Stamp)
        Total = len(datalist)
        logger.info('写入数据中……')
        for i in range(A, Total):
            InsertDB().insert_Result('results_summary', datalist[i])
    elif Total_Type==A:
        logger.info('结果汇总页已经汇总完成，无需再次汇总！')
    else:
        logger.error('未知错误：预期总数%s,实际生成数%s'%(Total_Type,A))


    sql =  "select * from  %s WHERE test_version='%s' AND test_batch='%s' ;" % ('summary', Test_Version, Test_Batch)
    datalist = Query_DB().query_db_all(sql)#查询
    if len(datalist)==0:
        logger.info('写入数据中……')
        summary_hz(threshold, Test_Version, Test_Batch, Time_Stamp)
    elif len(datalist)==1:
        logger.info('汇总语页数据，已经写入完成，无需再次汇总！')
    else:
        logger.error('未知错误,计数：%s ,数据：%s'% (len(datalist), datalist))



def download(addr,Test_Version,Test_Batch):#下载数据到表格
    logger.info('开始获取导出数据……')
    data=(CulturalAPI().get_summary_data(Test_Version,Test_Batch))
    data1=(CulturalAPI().get_results_summary_data(Test_Version,Test_Batch))
    sql="select * from  %s WHERE test_version='%s' AND test_batch='%s' ;" % ('test_record_sheet', Test_Version,Test_Batch)
    summary=data['datalist'][data['time'][-1]]
    results_summary=data1['datalist'][data1['time'][-1]]
    record_sheet=Query_DB().query_db_all(sql)
    logger.info('开始写入数据！')
    ExportExcle(addr,record_sheet)
    SummaryExcle(addr, results_summary)
    VerticalExcle(addr, summary)
    logger.info('导出数据完成！')


