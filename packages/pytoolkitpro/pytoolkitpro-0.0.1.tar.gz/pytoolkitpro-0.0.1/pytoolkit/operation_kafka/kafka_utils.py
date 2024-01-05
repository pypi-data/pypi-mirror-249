#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/3 13:23
# @Author:boyizhang
import json

from kafka import KafkaProducer, KafkaConsumer


class KafkaUtils():

    def __init__(self, brokers, topic, username=None, password=None, security_protocol='SASL_PLAINTEXT',
                 sasl_mechanism='SCRAM-SHA-512', enable_auto_commit=False, auto_offset_reset='earliest'):
        self.brokers = brokers

        self.product_config = {
            'security_protocol': security_protocol,
            'sasl_mechanism': sasl_mechanism,
            'bootstrap_servers': brokers
        }
        self.consumer_config = {
            'sasl_mechanism': sasl_mechanism,
            'bootstrap_servers': brokers,
            'security_protocol': security_protocol,
            'auto_offset_reset': auto_offset_reset,
            'enable_auto_commit': enable_auto_commit,
        }
        if username and password:
            self.product_config['sasl_plain_username'] = username
            self.product_config['sasl_plain_password'] = password
            self.consumer_config['sasl_plain_username'] = username
            self.consumer_config['sasl_plain_password'] = password
        self.topic = topic

    def consumer(self, group_id, enable_auto_commit=False, auto_offset_reset='earliest'):
        self.consumer_config['group_id'] = group_id
        self.consumer_config['enable_auto_commit'] = enable_auto_commit
        self.consumer_config['auto_offset_reset'] = auto_offset_reset
        consumer = KafkaConsumer(self.topic, **self.consumer_config)
        for message in consumer:
            print("%s:%d:%d: key=%s value=%s, %s" % (
            message.topic, message.partition, message.offset, message.key, message.value, message))
            # print('Received message: {}'.format(message.value))

    def product(self, data, key=b''):
        if isinstance(data, list):
            for value in data:
                self._product_main(value, key=key)
        if isinstance(data, str) or isinstance(data, bytes):
            self._product_main(data, key=key)

    def _product_main(self, value, key):
        print(f"config:{self.product_config}\nbrokers:{self.brokers}\ntopic:{self.topic}")
        producer = KafkaProducer(**self.product_config)
        value_to_byte = value
        if not isinstance(value, str):
            value = json.dumps(value)
        if not isinstance(value, bytes):
            value_to_byte = bytes(value, encoding="utf8")
        if not isinstance(key, bytes):
            key = bytes(key, encoding="utf8")
        future = producer.send(self.topic, key=key, value=value_to_byte, partition=0)
        result = future.get(timeout=10)
        print(f"result:{result}, value_to_byte:{value_to_byte}")

    def parse_config_file(self):
        pass


if __name__ == '__main__':
    username, password, brokers, topic = 'owner-e721c5', 'qsBhwYXq', [
        "kafka.public_acl_test.ap-sg-1-general-x.test.mq.shopee.io:29133"], "selleroperation-fss-ccb-program-noti-id-test"
    kafka_utils = KafkaUtils(brokers, topic, username, password)
    print('================product================')
    kafka_utils.product('test', b'ttt')
    print('================consumer================')
    kafka_utils.consumer(group_id='marketplace-seller-e721c5')
