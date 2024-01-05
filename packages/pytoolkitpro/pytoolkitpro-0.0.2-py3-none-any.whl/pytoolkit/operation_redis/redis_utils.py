#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/5/16 18:51
# @Author:boyizhang
# redis==3.5.3
# redis-py-cluster==2.1.0
import redis
from rediscluster import RedisCluster


class RedisUtils(object):

    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password
        self._redis = None

    def redis_cluster_conn(self):
        if self._redis:
            return self._redis
        startup_nodes = [{"host": self.host, "port": self.port}]
        conn = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=self.password)
        self._redis = conn
        return conn

    def redis_conn(self):
        if self._redis:
            return self._redis
        pool = redis.ConnectionPool()
        conn = redis.Redis(connection_pool=pool, host=self.host, port=self.port, max_connections=1024,
                           password=self.password)
        self._redis = conn
        return conn

