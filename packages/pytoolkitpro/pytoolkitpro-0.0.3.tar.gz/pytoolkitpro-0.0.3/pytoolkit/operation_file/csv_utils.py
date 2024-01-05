#!/usr/bin/metrics_db_name python
# -*- coding: utf-8 -*-
# @Time:2021/12/21 5:53 下午
# @Author:boyizhang
import csv
import logging
import os
import random


class CsvTools(object):
    @staticmethod
    def write_to_file(sheet_data_list, headers: list, file_name=None, is_single_row=True):
        """
        :param sheet_data_dict: defaultdict 每个key对应一个sheet的值。sheet值的key的写入数据与headers元素顺序一致
        :param headers: list 标题头
        :param filename: 保存的文件地址+文件名
        :param type:
        :return:
        """
        with open(f'{file_name}.csv', mode='a') as f:
            # 追加
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if f.tell() == 0:
                writer.writerow(headers)
            if is_single_row:
                writer.writerow(sheet_data_list)
            else:
                writer.writerows(sheet_data_list)

    @staticmethod
    def read_data_from_mutil_file(file_path='.', match='source.csv'):
        files = os.listdir(file_path)
        rows = []
        logging.debug(f"files:{files}")
        for file in files:
            if file.endswith(match):

                with open(file, 'r') as f:
                    reader = csv.reader(f)
                    line_count = 0
                    for row in reader:
                        if line_count != 0:
                            rows.append(int(row[0]))
                            line_count += 1
                        else:
                            line_count += 1
                            continue

        logging.debug(f"rows:{rows}")
        return rows

    @staticmethod
    def read_data_from_single_file(file_name):
        rows = []
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            line_count = 0
            for row in reader:
                if line_count != 0:
                    rows.append(int(row[0]))
                    line_count += 1
                else:
                    line_count += 1
                    continue

        logging.debug(f"rows:{rows}")
        return rows

if __name__ == '__main__':
    shop_ids = []
    for i in range(30000):
        a=random.randint(10000,99999999)
        print(a)
        shop_ids.append([a])
    print(len(shop_ids))

    CsvTools.write_to_file(shop_ids,['To-be-onboarded Shopid'], 'boyi onboard 30k test',False)
