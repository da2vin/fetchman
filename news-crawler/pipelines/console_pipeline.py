#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from fetchman.pipeline.base_pipeline import ItemPipeline
from fetchman.utils import FetchManLogger
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


# 输出pipeline
class ConsolePipeline(ItemPipeline):
    def process_item(self, item):
        try:
            print item['name']
        except:
            FetchManLogger.logger.error(traceback.format_exc())
