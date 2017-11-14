#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from fetchman.pipeline.base_pipeline import ItemPipeline
from fetchman.utils import FetchManLogger
import traceback

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 保存图片pipeline
class PicPipeline(ItemPipeline):
    def process_item(self, item):
        try:
            if item is not None:
                with open("/data/fahand/images/400x400/" + item['name'], 'wb') as fs:
                    fs.write(item['content'])
                    print("download success!")
        except Exception:
            FetchManLogger.logger.error(traceback.format_exc())
