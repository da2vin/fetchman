#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class pipeItem(object):
    def __init__(self, pipenames=[], result=None):
        self.pipenames = pipenames
        self.result = result
