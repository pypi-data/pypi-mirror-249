#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/1 11:49
# @Author:boyizhang
import concurrent.futures
import time

import gevent
import pymysql
# from pymysqlpool import ConnectionPool
from PyMysqlPool.pool import Pool
from dbutils.pooled_db import PooledDB
from gevent import monkey
from pymysql import OperationalError
from pymysql.cursors import DictCursor

# 打补丁，使PyMySQL与gevent协作
monkey.patch_all()


class MySQLDataReader:
    def __init__(self, host, port, user, password, database_prefix, table_prefix, num_databases, num_tables):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database_prefix = database_prefix
        self.table_prefix = table_prefix
        self.num_databases = num_databases
        self.num_tables = num_tables
        self.datas = []

        # 创建连接池
        self.connection_pool = PooledDB(
            creator=pymysql,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=None,  # 连接时指定数据库
            cursorclass=DictCursor,
            autocommit=True,
            blocking=True,
            maxconnections=10,  # 连接池中的最大连接数
            mincached=1,  # 初始化连接池中的连接数
        )

        self.connection_pool_2 = Pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=None,  # 连接时指定数据库
            autocommit=True,
            min_size=1,
            max_size=3,
        )

    def read_data_v1(self, database, table):
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=database
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table} limit 10")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def read_data_v2(self, database, table):
        connection = self.connection_pool.connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f"USE {database}")  # 切换到指定数据库
            cursor.execute(f"SELECT sleep(5)")
            # cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            return rows
        except OperationalError as e:
            # 处理数据库连接异常
            print(f"OperationalError: {e}")
        finally:
            cursor.close()
            connection.close()
    # def read_data_v3(self, database, table):
    #     connection = self.connection_pool_2.get_conn()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(f"USE {database}")  # 切换到指定数据库
    #         cursor.execute(f"SELECT * FROM {table}")
    #         rows = cursor.fetchall()
    #         return rows
    #     except OperationalError as e:
    #         # 处理数据库连接异常
    #         print(f"OperationalError: {e}")
    #     finally:
    #         cursor.close()
    #         connection.close()

    def process_data(self, data):
        # 在这里处理数据，可以根据需求进行相应的操作
        print(data)

    def run_by_concurrent(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 提交任务到线程池
            futures = []
            for i in range(num_databases):
                for j in range(num_tables):
                    database_name = f"{database_prefix}_{str(i).zfill(8)}"
                    table_name = f"{table_prefix}_{str(j).zfill(8)}"
                    future = executor.submit(self.read_data_v2, database_name, table_name)
                    futures.append(future)

            # 收集任务的结果
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.datas.extend(result)

    def run(self):
        # 创建协程列表
        greenlets = []

        # 生成协程并发读取数据
        for i in range(self.num_databases):
            for j in range(self.num_tables):
                database_name = f"{self.database_prefix}_{str(i).zfill(8)}"
                table_name = f"{self.table_prefix}_{str(j).zfill(8)}"
                greenlet = gevent.spawn(self.read_data_v2, database_name, table_name)
                greenlets.append(greenlet)

        # 等待所有协程执行完成
        gevent.joinall(greenlets)

        # 收集协程的结果
        for greenlet in greenlets:
            result = greenlet.value
            self.datas.extend(result)

        # 处理数据
        # for data in self.datas:
        #     self.process_data(data)


# 使用示例
# host = 'master.shopee_seller_growth.mysql.cloud.test.shopee.io'
# port = 6606
# user = 'sz_seller_test'
# password = 'k6Dg3A608Knpy_Q1T1Rr'
# database_prefix = 'shopee_seller_growth_metrics_db'
# table_prefix = 'preferred_seller_execute_result_tab'
# num_databases = 10
# num_tables = 10

host = 'localhost'
port = 3306
user = 'root'
password = 'zhangboyi'
database_prefix = 'qa_auto'
table_prefix = 'api_tab'
num_databases = 10
num_tables = 10

# 创建 MySQLDataReader 实例并运行

i = 0
total = 0
while i < 20:
    data_reader = MySQLDataReader(
        host, port, user, password, database_prefix, table_prefix, num_databases, num_tables
    )
    ctime = int(time.time() * 1000)
    # 2.3s
    data_reader.run_by_concurrent()
    # 13.466s
    # data_reader.run()
    mtime = int(time.time() * 1000)
    print(f'loader time:{(mtime - ctime) / 1000}s')
    print(data_reader.datas)
    # time.sleep(1)
    i += 1
    total += (mtime - ctime) / 1000
print(f"result：{total / i}")
