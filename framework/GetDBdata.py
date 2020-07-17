#!/user/bin/env python3
# -*- coding: utf-8 -*-
import pymysql,re
from framework.logger import Logger
logger = Logger(logger="GetDBdata").getlog()



import configparser,os
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath,encoding="utf-8-sig")

host=cf.get("DATABASE", "host")
user=cf.get("DATABASE", "user")
password=cf.get("DATABASE", "password")
DB='test'
port=cf.get("DATABASE", "port")

class GetDBdata():
    def query_db_all(self, sql):  # 查询表中所有数据
        lists = []
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # cursor = db.cursor(MySQLdb.cursors.DictCursor)
        try:
            # 执行SQL语句
            # sql = "SELECT * FROM %s"%table_name
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            desc = cursor.description  # 提取数据库表头字段
            key_list = (",".join([item[0] for item in desc]))  # 提取数据库表头字段
            Key_list = key_list.split(',')  # 数据库表头字段转化为列表
            for row in results:
                dic = dict(zip(Key_list, row))
                lists.append((dic))
        except Exception as e:
            logger.error(str(e))
        # 关闭数据库连接
        db.close()
        return lists
    def get_db_data(self,dic_rc):

        try:
            sql = "SELECT * FROM `sheet1` WHERE 文物编号= %s and 图片名称='%s'" % (dic_rc['Code'], dic_rc['Test_Chart'])
            data = GetDBdata().query_db_all(sql)[0]
            dic_cc = {
                'top1': data['top1'],
                'top2': data['top2'],
                'top3': data['top3'],
            }

            return {"code": 2000, "message": "识别成功！", "topdata": dic_cc}
        except:

            dic_cc ={"code": 4000, "message": "异常出错", "topdata": {'top1': -99, 'top2': -99, 'top3': -99}}

            return(dic_cc)
