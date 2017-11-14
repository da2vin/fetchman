#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from fetchman.pipeline.base_pipeline import ItemPipeline
from fa_news import DBSession, News
from fetchman.utils import FetchManLogger
import traceback

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 存入数据库pipeline
class DataBasePipeline(ItemPipeline):
    def process_item(self, item):
        try:
            session = DBSession()
            news = News(newsProductId=item["newsProductId"],
                        newsCateId=item["newsCateId"],
                        name=item["name"],
                        newsFromWebUrl=item['newsFromWebUrl'],
                        newsFrom=item["newsFrom"],
                        createTime=item["createTime"],
                        longDes=item["longDes"],
                        imageUrl=item["imageUrl"],
                        shortDes=item["shortDes"],
                        status=1,
                        auditStatus=2)
            session.add(news)
            session.commit()
            session.close()
        except Exception:
            FetchManLogger.logger.error(traceback.format_exc())
