#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/3 10:48
# @Author:boyizhang
import concurrent.futures
import threading

import gevent
import pymysql
from dbutils.pooled_db import PooledDB
from gevent import monkey
from pymysql import OperationalError
from pymysql.cursors import DictCursor

# 打补丁，使PyMySQL与gevent协作
monkey.patch_all()


class SQLUtils:
    pass


class MysqlUtils:
    def __init__(self, db_instance, host, port, user, password):
        self.db_instance = db_instance
        self.host = host
        self.user = user
        self.port = port
        self.password = password
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

    def gen_sql(self, dbn, tbn, database_prefix, table_prefix, sql):
        database = f"{database_prefix}_{str(dbn).zfill(8)}"
        table = f"{table_prefix}_{str(tbn).zfill(8)}"
        sql = sql.format(database=database, table=table)
        return sql

    def read_data(self, sql):
        connection = self.connection_pool.connection()
        cursor = connection.cursor()
        try:
            # cursor.execute(sql)
            # cursor.execute(f"SELECT sleep(5)")
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except OperationalError as e:
            # 处理数据库连接异常
            print(f"OperationalError: {e}")
        finally:
            cursor.close()
            connection.close()

    def read_data_by_concurrent(self, num_databases, num_tables, database_prefix, table_prefix, sql):
        rows = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 提交任务到线程池
            futures = []
            for i in range(num_databases):
                for j in range(num_tables):
                    sql = self.gen_sql(i, j, database_prefix, table_prefix, sql)
                    future = executor.submit(self.read_data, sql)
                    futures.append(future)

            # 收集任务的结果
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                rows.extend(result)
        return rows

    def ready_data_by_threading(self, num_databases, num_tables, database_prefix, table_prefix, sql: str):
        rows = []
        threads = []

        for i in range(num_databases):
            for j in range(num_tables):
                sql = self.gen_sql(i, j, database_prefix, table_prefix, sql)
                thread = threading.Thread(target=self.read_data, args=(sql,))
                threads.append(thread)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for thread in threads:
            rows.extend(thread.result)

    def read_data_by_gevent(self, num_databases, num_tables, database_prefix, table_prefix, sql):
        greenlets = []
        rows = []
        for i in range(num_databases):
            for j in range(num_tables):
                sql = self.gen_sql(i, j, database_prefix, table_prefix, sql)
                greenlet = gevent.spawn(self.read_data, sql)
                greenlets.append(greenlet)

        gevent.joinall(greenlets)
        exceptions = []
        for greenlet in greenlets:
            if not greenlet.successful():
                exceptions.append(greenlet.exception)
            rows.extend(greenlet.value)
        return rows

if __name__ == '__main__':
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'zhangboyi'
    database_prefix = 'qa_auto'
    table_prefix = 'api_tab'
    num_databases = 10
    num_tables = 10
    sql_con = MysqlUtils(db_instance=1, host=host, port=port, user=user, password=password)
    # sql = "SELECT * FROM {database}.{table}"
    sql = "SELECT * FROM {database}.{table}"
    rows = sql_con.read_data_by_gevent(num_databases, num_tables, database_prefix, table_prefix, sql)
    print(f"len: {len(rows)}")

