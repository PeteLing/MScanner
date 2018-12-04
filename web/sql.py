# coding=utf-8

import sys
import re
import copy

from LogManager import log

from wCurl import wcurl
from hashes.simhash import simhash

from web.http.Request import Request
from web.http.postdata import postdata
from web.util.smart_fill import smart_fill
from web.util.rand_string import rand_char, rand_number, rand_letter

import data.severity as severity
from data.vuln import vuln
from data.vulnmanager import vm


class sql:
    def __init__(self):
        self._true_threshold = 0.85
        self._false_threshlod = 0.90

        # 扫描模式： 0普通模式 1验证模式
        self._scan_mode = 0
        self._sql_verify_value = "(select{watscan watscan}from(SELECT COUNT(*),CONCAT(0x73716C,(SELECT (ELT(" \
                                 "2085=2085,1))),0x5F766572696679,FLOOR(RAND(0)*2))x FROM " \
                                 "INFORMATION_SCHEMA.CHARACTER_SETS GROUP BY x)a) "
        self._sql_verify_key = "sql1_verify1"
        # 白名单参数列表，过滤掉没有必要检测的参数
        self._white_param = ["csrf_token", "captcha", "sign", "_"]

    def check(self, t_request):
        log.info('正在检测目标是否存在SQL注入漏洞...')
        http_request = copy.deepcopy(t_request)
        # param {'id': 'd', 'tp': 'ttt', 'name': ''}
        if http_request.get_method() == 'GET':
            param_dict = http_request.get_get_param()

        if http_request.get_method == 'POST':
            param_dict = http_request.get_post_param()

        sql_payload_list = self._get_payload_list(param_dict)
        error_param_list = []

        for name, poc_true, poc_false, poc_type in sql_payload_list:
            if name.lower() in self._white_param:
                continue
            if http_request.get_method() == 'GET':
                pass

