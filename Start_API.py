#!/user/bin/env python3
# -*- coding: utf-8 -*-

import flask, json,os
from framework.CulturalAPI import CulturalAPI
from flask import request

from framework.logger import Logger
logger = Logger(logger="API").getlog()

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
if __name__ == '__main__':
    server.run(debug=True, port=8408, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
