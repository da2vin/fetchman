#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')


# seq生成器
class SeqUtil(object):
    tempSeq = ''
    seq = 0

    @classmethod
    def get_seq(cls):
        cls.tempSeq = str(cls.seq)
        while cls.tempSeq.__len__() < 3:
            cls.tempSeq = "0" + cls.tempSeq
        cls.seq += 1
        if cls.seq == 1000:
            cls.seq = 0
        return cls.tempSeq
