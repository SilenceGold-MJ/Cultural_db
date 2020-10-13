#!/user/bin/env python3
# -*- coding: utf-8 -*-

import flask, json,os
from framework.CulturalAPI import CulturalAPI
from framework.Getimage import Getimage
from flask import request

from framework.logger import Logger
logger = Logger(logger="Start_API").getlog()

'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)
@server.route('/GetStart',methods=['post']) #入参为json
def GetStart():#获取测试批次和版本列表
    data = CulturalAPI().get_start_recording()
    logger.info("'/GetStart',methods=['post']：%s" % (str(data)))
    return data
@server.route('/GetSheetData',methods=['post']) #入参为json
def GetSheetData():#获取测试记录也得数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch')
        }
        data = CulturalAPI().get_record_sheet_data(dic['test_version'],dic['test_batch'])
        logger.info("'/GetSheetData',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/GetSheetData',methods=['post']：" + str(data))
        return data
@server.route('/GetResultsData',methods=['post']) #入参为json
def GetResultsData():#获取汇总页数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch')
        }
        data =CulturalAPI().get_results_summary_data(dic['test_version'],dic['test_batch'])
        logger.info("'/GetResultsData',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/GetResultsData',methods=['post']：" + str(data))
        return data

@server.route('/GetSummaryData',methods=['post']) #入参为json
def GetSummaryData():#获取测试汇总结果
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch')
        }
        data =CulturalAPI().get_summary_data(dic['test_version'],dic['test_batch'])
        logger.info("'/GetSummaryData',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/GetSummaryData',methods=['post']：" + str(data))
        return data

@server.route('/GetOnesheet',methods=['post']) #入参为json
def GetOnesheet():  # 获取某一个文物
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch'),
            'Code':params.get('Code')

        }
        data = CulturalAPI().get_one_sheet_data(dic)
        logger.info("'/GetOnesheet',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/GetOnesheet',methods=['post']：" + str(data))
        return data

@server.route('/GetPic', methods=['post'])  # 入参为json
def GetPic():#单个图片信息
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch'),
            'Code':params.get('Code'),
            'Test_Chart': params.get('Test_Chart')

        }
        data = CulturalAPI().get_pic_data(dic)
        logger.info("'/GetPic', methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/GetPic', methods=['post']" + str(data))
        return data
@server.route('/Linechart', methods=['post'])  # 入参为json
def Linechart():#获取折线图基础数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch')
        }
        data =CulturalAPI().Linechart(dic['test_version'],dic['test_batch'])
        logger.info("'/Linechart',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/Linechart',methods=['post']：" + str(data))
        return data
@server.route('/Proportion_zb', methods=['post'])  # 入参为json
def Proportion_zb():#获取饼状图基础数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            'test_version': params.get('test_version'),
            'test_batch': params.get('test_batch')
        }
        data =CulturalAPI().Proportion_zb(dic['test_version'],dic['test_batch'])
        logger.info("'/Proportion_zb',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/Proportion_zb',methods=['post']：" + str(data))
        return data

@server.route('/Addtestinfo', methods=['post'])  # 入参为json
def Addtestinfo():
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            "version":params.get("version"),
            "Test_Time": params.get("Test_Time"),
            "developer": params.get("developer"),
            "deletes": 0
        }
        data =CulturalAPI().Addtestinfo(dic)
        logger.info("'/Addtestinfo',methods=['post']：%s；%s" % (str(dic), str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/Addtestinfo',methods=['post']：" + str(data))
        return data


@server.route('/SampleBatch', methods=['post'])  # 入参为json
def SampleBatch():
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。

    if params:
        try:
            batch_path = params.get("batch_path")
            imageinfo = Getimage(batch_path)
            types_num = len(list(set(imageinfo[1])))
            total_num = len(imageinfo[0])

            dic = {
                "batch": params.get("batch"),
                "types_num": types_num,
                "total_num": total_num,
                "Test_Time": params.get("Test_Time"),
                "delete": 0,
                "batch_path": batch_path.replace('\\', '/'),
            }

            data = CulturalAPI().SampleBatch(dic)
            logger.info("'/SampleBatch',methods=['post']：%s；%s" % (str(dic), str(data)))
            return data
        except Exception as e:
            data = json.dumps({"result_code": 4000, "message": "样本路径不准确，请重新输入（%s）。" % e})
        logger.error("'/SampleBatch',methods=['post']：" + str( json.loads(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "message": "入参必须为json类型。"})
        logger.info("'/SampleBatch',methods=['post']：" + str(data))
        return data






@server.route('/Getform', methods=['post'])  # 入参为json
def getform():#获取列表数据
    # table_name = 'summary'
    # data = CulturalAPI().getform(table_name)
    # logger.info("'/GetSummary',methods=['post']：%s" % (str(data)))
    # return data

    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            "table_name":params.get("table_name"),
            'Latest_name':params.get("Latest_name")
            # "Test_Version": params.get("Test_Version"),
            # "Test_Batch": params.get("Test_Batch"),
        }
         # Latest_name 指导字段最新排序
        logger.info("'/getform',methods=['post']：%s；" % (str(dic)))
        data = CulturalAPI().getform(dic)
        logger.info("'/getform',methods=['post']：%s" % ( str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/DownloadExcle',methods=['post']：" + str(data))
        return data



@server.route('/DownloadExcle', methods=['post'])  # 入参为json
def DownloadExcle():#下载excel

    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            "filename":params.get("filename"),
            "Test_Version": params.get("Test_Version"),
            "Test_Batch": params.get("Test_Batch"),
        }

        logger.info("'/DownloadExcle',methods=['post']：%s；" % (str(dic)))
        data = CulturalAPI().download_excle(dic)
        logger.info("'/DownloadExcle',methods=['post']：%s" % ( str(data)))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/DownloadExcle',methods=['post']：" + str(data))
        return data


@server.route('/del_summary_data', methods=['post'])  # 入参为json
def del_summary_data():#删除一行数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        dic = {
            "dic_data": params.get("dic_data"),
        }
        logger.info("'/del_summary_data',methods=['post']：%s；" % (str(dic["dic_data"])))
        #data = CulturalAPI().del_summary_data(dic["table_name"],dic['Test_Version'],dic['Test_Batch'])
        data = CulturalAPI().del_summary_data(dic["dic_data"])
        logger.info("'/del_summary_data',methods=['post']：%s" % ( str(dic["dic_data"])))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/del_summary_data',methods=['post']：" + str(data))
        return data


if __name__ == '__main__':
    server.run(debug=True, port=8408, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
