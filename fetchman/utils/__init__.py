#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import os
import time

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

if not os.path.exists("log"):
    os.mkdir("log")

if not os.path.exists("log/error_content"):
    os.mkdir("log/error_content")

class FetchManLogger(object):
    logger = None

    @classmethod
    def init_logger(cls,name):
        name = name.upper()
        date_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        cls.logger = logging.getLogger(name)
        cls.logger.setLevel(logging.DEBUG)
        # 建立一个filehandler来把日志记录在文件里，级别为error以上
        fh_error = logging.FileHandler("log/" + name + "_ERROR_" + date_time + ".log")
        fh_error.setLevel(logging.ERROR)
        # 建立一个filehandler来把日志记录在文件里，级别为error以上
        fh_info = logging.FileHandler("log/" + name + "_INFO_" + date_time + ".log")
        fh_info.setLevel(logging.INFO)
        # 建立一个streamhandler来把日志打在CMD窗口上，级别为info以上
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 设置日志格式
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        fh_error.setFormatter(formatter)
        fh_info.setFormatter(formatter)
        # 将相应的handler添加在logger对象中
        cls.logger.addHandler(ch)
        cls.logger.addHandler(fh_error)
        cls.logger.addHandler(fh_info)
