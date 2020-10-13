#!/user/bin/env python3
# -*- coding: utf-8 -*-
import pymysql,re
from framework.logger import Logger
logger = Logger(logger="Query_DB").getlog()



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
class Query_DB():#查询个数
    def getnum(self,sql):
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句

            cursor.execute(sql)
            # 获取所有记录列表
            results = str(cursor.fetchall())

            # logger.info(re.findall(r'\d+', results)[0])
            return (int(re.findall(r'\d+', results)[0]))

        except:
            logger.info("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()

    def query_db_all(self,sql ):  # 查询表中所有数据
        lists = []

        # 打开数据库连接

        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        #cursor = db.cursor(MySQLdb.cursors.DictCursor)

        try:
            # 执行SQL语句
            # sql = "SELECT * FROM %s"%table_name

            cursor.execute(sql)
            # 获取所有记录列表
            logger.info(sql)
            results = cursor.fetchall()
            desc = cursor.description#提取数据库表头字段
            key_list=( ",".join([item[0] for item in desc]))#提取数据库表头字段
            Key_list =key_list.split(',')#数据库表头字段转化为列表
            id=1
            for row in results:
                dic = dict(zip(Key_list, row))
                del_list = ['deletes', 'Time_Stamp', 'Test_ID', 'Color']
                for i in del_list:
                    if i in dic:
                        del dic[i]
                if 'id' in dic:
                    dic.update({"id":id})
                elif 'ID' in dic:
                    dic.update({"ID": id})
                lists.append((dic))
                id=id+1
        except Exception as e:
            logger.error(str(e))
        # 关闭数据库连接
        db.close()

        return lists

    def query_db_rowlist(self,table_name, test_version, test_batch,row):  # 查询表中某一个行数据列表+除重
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        #cursor = db.cursor(MySQLdb.cursors.DictCursor)

        try:
            # 执行SQL语句
            # sql = "SELECT * FROM %s"%table_name
            sql = "select * from  %s WHERE test_version='%s' AND test_batch='%s' ;" % (
            table_name, test_version, test_batch)
            cursor.execute(sql)
            # 获取所有记录列表

            results = cursor.fetchall()
            key_list=(set ([item[row] for item in results]))
            return list(key_list)
        except Exception as e:
            logger.error(str(e))

        # 关闭数据库连接
        db.close()

    def db_all_No_return(self,sql ):  #执行sql语句无返回值
        lists = []
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        #cursor = db.cursor(MySQLdb.cursors.DictCursor)
        try:
            # 执行SQL语句
            # sql = "SELECT * FROM %s"%table_name
            cursor.execute(sql)
            # 获取所有记录列表
            # 执行sql语句
            db.commit()
            logger.info('执行(%s)'%str(sql))
            # results = cursor.fetchall()
            # desc = cursor.description#提取数据库表头字段
            # key_list=( ",".join([item[0] for item in desc]))#提取数据库表头字段
            # Key_list =key_list.split(',')#数据库表头字段转化为列表
            # for row in results:
            #     dic = dict(zip(Key_list, row))
            #     lists.append((dic))
        except Exception as e:
            logger.error(str(e))
        # 关闭数据库连接
        db.close()

        return lists
