#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/5/31 23:24
# @Author:boyizhang
import concurrent.futures
import time

import gevent
from gevent import monkey
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# 打补丁，使SQLAlchemy与gevent协作
monkey.patch_all()


class MySQLDataReader:
    def __init__(self, host, port, user, password, database_prefix, table_prefix, num_databases, num_tables):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_prefix = database_prefix
        self.table_prefix = table_prefix
        self.num_databases = num_databases
        self.num_tables = num_tables
        self.datas = []

        # 创建数据库引擎
        self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/',
                                    poolclass=QueuePool, pool_size=100, max_overflow=0, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def read_data(self, database, table):
        # 创建表对象

        session = self.Session()
        # 创建表对象
        metadata = MetaData(bind=self.engine, schema=database)
        target_table = Table(table, metadata, autoload=True, schema=database)

        # 执行查询
        result = session.query(target_table).all()
        # print(f"result:{result}")
        session.close()
        # # 执行查询
        # with self.engine.connect() as conn:
        #     result = conn.execute(target_table.select()).fetchone()

        return result

    def process_data(self, data):
        # 在这里处理数据，可以根据需求进行相应的操作
        print(data)

    def run(self):
        # 创建协程列表
        greenlets = []

        # 生成协程并发读取数据
        for i in range(self.num_databases):
            database_name = f"{self.database_prefix}_{str(i).zfill(8)}"
            for j in range(self.num_tables):
                table_name = f"{self.table_prefix}_{str(j).zfill(8)}"
                greenlet = gevent.spawn(self.read_data, database_name, table_name)
                greenlets.append(greenlet)

        # 等待所有协程执行完成
        gevent.joinall(greenlets)

        # 收集协程的结果
        for greenlet in greenlets:
            result = greenlet.value
            # print(result)
            self.datas.extend(result)

        # 处理数据
        # print(self.datas)
        # for data in self.datas:
        #     self.process_data(data)

    def run_by_concurrent(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 提交任务到线程池
            futures = []
            for i in range(num_databases):
                for j in range(num_tables):
                    database_name = f"{database_prefix}_{str(i).zfill(8)}"
                    table_name = f"{table_prefix}_{str(j).zfill(8)}"
                    future = executor.submit(self.read_data, database_name, table_name)
                    futures.append(future)

            # 收集任务的结果
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.datas.extend(result)

        # 处理数据
        # for data in self.datas:
        #     self.process_data(data)


# 使用示例
# host = 'master.shopee_seller_growth.mysql.cloud.test.shopee.io'
# port = '6606'
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
data_reader = MySQLDataReader(
    host, port, user, password, database_prefix, table_prefix, num_databases, num_tables
)
while i < 20:
    data_reader.datas=[]
    ctime = int(time.time() * 1000)
    # data_reader.run()
    data_reader.run_by_concurrent()
    mtime = int(time.time() * 1000)
    print(f'loader time:{(mtime - ctime) / 1000}s')
    # print(data_reader.datas)
    i += 1
    total += (mtime - ctime) / 1000
print(f"result：{total / i}")
