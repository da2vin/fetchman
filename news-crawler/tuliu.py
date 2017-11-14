#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import hashlib
import random
import sys
import time

from bs4 import BeautifulSoup as bs
from util.seq_util import SeqUtil

from fetchman.downloader.http.spider_request import Request
from fetchman.pipeline.pipe_item import pipeItem
from fetchman.processor.base_processor import BaseProcessor
from fetchman.spider.spider_core import SpiderCore
from fetchman.utils.decorator import check
from pipelines.console_pipeline import ConsolePipeline
from pipelines.database_pipeline import DataBasePipeline
from pipelines.pic_pipeline import PicPipeline

reload(sys)
sys.setdefaultencoding('utf-8')

# 爬取土流网解析器
class Tuliu_Processor(BaseProcessor):
    spider_id = 'tuliu_spider'
    allowed_domains = ['tuliu.com']

    # 推入初始request
    @classmethod
    def init_start_requests(cls):
        cls.start_requests.extend([Request(url='http://www.tuliu.com/news/list-c165/%s.html' % page, priority=0, meta={'newsCateId': '20171102111907007'}) for page in range(1, 9)])
        cls.start_requests.extend([Request(url='http://www.tuliu.com/news/list-c163/%s.html' % page, priority=0, meta={'newsCateId': '20171102111907007'}) for page in range(1, 30)])

    @check
    def process(self, response):
        if '404错误' not in response.m_response.content:
            soup = bs(response.m_response.content, 'lxml')

            tuliu_div_list = soup.select('div.news_list_list ul li.list_box')
            for tuliu_div in tuliu_div_list:
                if tuliu_div.select('a img'):
                    detail_url = tuliu_div.select('a')[0]['href']
                    img_url = tuliu_div.select('a img')[0]['src']
                    name = tuliu_div.select('h1.category_title nobr.l')[0].text.strip()
                    createTime = tuliu_div.select('h1.category_title nobr.r')[0].text.replace('发布时间 ', '').strip()
                    shortDes = tuliu_div.select('div')[0].text.replace('[查看全文]', '')

                    md5 = hashlib.md5()
                    rand_name = str(time.time()) + str(random.random())
                    md5.update(rand_name)
                    img_name = md5.hexdigest() + '.jpg'

                    request = Request(url=img_url, priority=1, callback=self.process_pic)
                    request.meta['img_name'] = img_name
                    yield request

                    request = Request(url=detail_url, priority=1, callback=self.process_detail)
                    request.meta['name'] = name
                    request.meta['createTime'] = createTime
                    request.meta['shortDes'] = shortDes
                    request.meta['img_name'] = img_name
                    request.meta['newsCateId'] = response.request.meta['newsCateId']
                    yield request

    # 获取图片内容并丢入PicPipeline
    @check
    def process_pic(self, response):
        item = dict()
        item['content'] = response.m_response.content
        item['name'] = response.request.meta['img_name']
        yield pipeItem(['pic'], item)

    # 获取新闻详情并丢入DataBasePipeline
    @check
    def process_detail(self, response):
        soup = bs(response.m_response.content, 'lxml')
        result = dict()
        result['newsProductId'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + SeqUtil.get_seq()
        result['newsCateId'] = response.request.meta['newsCateId']
        result['name'] = response.request.meta['name']
        result['imageUrl'] = response.request.meta['img_name']
        result['newsCateId'] = response.request.meta['newsCateId']
        result['shortDes'] = response.request.meta['shortDes']
        result['createTime'] = response.request.meta['createTime']
        result['newsFromWebUrl'] = response.request.url
        span_list = soup.select('div.article-header p.text-gray-9 span')
        for span in span_list:
            if '来源：' in span.text:
                result['newsFrom'] = span.text.replace('来源：', '').strip()
                break
            else:
                result['newsFrom'] = '互联网'
        longDes = soup.select('div.article-content')[0]

        tag_list = longDes.find_all()
        # 去除样式
        for tag in tag_list:
            attrs = copy.copy(tag.attrs)
            for key in attrs.iterkeys():
                if key != 'src':
                    del tag.attrs[key]

        result['longDes'] = str(longDes)

        yield pipeItem(['database', 'console'], result)


if __name__ == '__main__':
    # 生成爬虫对象，设置pipeline，启动爬虫
    SpiderCore(Tuliu_Processor(),time_sleep=1) \
        .set_pipeline(ConsolePipeline(), 'console') \
        .set_pipeline(PicPipeline(), 'pic') \
        .set_pipeline(DataBasePipeline(), 'database') \
        .start()
