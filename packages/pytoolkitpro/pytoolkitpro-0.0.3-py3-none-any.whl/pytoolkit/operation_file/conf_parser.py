#!/usr/bin/metrics_db_name python
# -*- coding: utf-8 -*-
# @Time:2021/2/5 6:12 下午
# @Author:boyizhang
import json
import os
# import ConfigParser
import logging
import configparser

import toml

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 脚本所在绝对目录

def parse_conf_toml(conf_file):
    with open(conf_file, 'r') as f:
        data = toml.load(f)
        print(json.dumps(data))


def parse_conf(conf_file):
    # conf_file = SCRIPT_DIR+'/log/ah_tools.log'
    conf_file = SCRIPT_DIR+'/conf/config.ini'
    """解析conf.ini，得到conf_dict"""
    conf_dict = dict()
    if not os.path.isfile(conf_file):
        raise IOError('conf file[%s] is not exsit' % conf_file)
    cf = configparser.ConfigParser()
    cf.read(conf_file)
    cf.items('lumos')

    # # alert_email
    # conf_dict['email_alert'] = int(cf.get('alert_email', 'email_alert'))
    # conf_dict['email_creator'] = cf.get('alert_email', 'email_creator')
    # email_notifyEmails = cf.get('alert_email', 'email_notifyEmails').split(',')
    # conf_dict['email_notifyEmails'] = list()
    # for notifyEmail in email_notifyEmails:
    #     conf_dict['email_notifyEmails'].append(notifyEmail)

    # lumos

    conf_dict['lumos_url'] = cf.get('lumos', 'lumos_url')
    conf_dict['lumos_session'] = cf.get('lumos', 'lumos_session')
    conf_dict['sql_editor_id'] = cf.get('lumos', 'sql_editor_id')
    conf_dict['database_id'] = cf.get('lumos', 'database_id')
    conf_dict['schema'] = cf.get('lumos', 'schema')

    # hive
    conf_dict['hive_host'] = cf.get('hive', 'hive_host')
    conf_dict['hive_port'] = cf.get('hive', 'hive_port')
    conf_dict['hive_auth'] = cf.get('hive', 'hive_auth')
    conf_dict['hive_username'] = cf.get('hive', 'hive_username')
    conf_dict['hive_password'] = cf.get('hive', 'hive_password')

    # hive_telin
    conf_dict['hive_host_telin'] = cf.get('hive_telin', 'hive_host')
    conf_dict['hive_port_telin'] = cf.get('hive_telin', 'hive_port')
    conf_dict['hive_auth_telin'] = cf.get('hive_telin', 'hive_auth')
    conf_dict['hive_username_telin'] = cf.get('hive_telin', 'hive_username')
    conf_dict['hive_password_telin'] = cf.get('hive_telin', 'hive_password')

    # hive_uat
    conf_dict['hive_host_uat'] = cf.get('hive_uat', 'hive_host')
    conf_dict['hive_port_uat'] = cf.get('hive_uat', 'hive_port')
    conf_dict['hive_auth_uat'] = cf.get('hive_uat', 'hive_auth')
    conf_dict['hive_username_uat'] = cf.get('hive_uat', 'hive_username')
    conf_dict['hive_password_uat'] = cf.get('hive_uat', 'hive_password')

    # lumos_uat
    conf_dict['lumos_url_uat'] = cf.get('lumos_uat', 'lumos_url')
    conf_dict['lumos_session_uat'] = cf.get('lumos_uat', 'lumos_session')
    conf_dict['sql_editor_id_uat'] = cf.get('lumos_uat', 'sql_editor_id')
    conf_dict['database_id_uat'] = cf.get('lumos_uat', 'database_id')
    conf_dict['schema_uat'] = cf.get('lumos_uat', 'schema')

    return conf_dict




if __name__ == "__main__":
    """for test"""
    # conf_file = SCRIPT_DIR + '/conf/config.ini'
    # conf_dict = parse_conf(conf_file)
    # print(conf_dict)

    parse_conf_toml('schema.toml')
