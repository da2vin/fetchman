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

# 爬取猪E网解析器
class Zhue_Processor(BaseProcessor):
    spider_id = 'toutiao_spider'
    allowed_domains = ['zhue.com.cn']

    # 推入初始request
    @classmethod
    def init_start_requests(cls):
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/guoneixinwen/35-%s.html' % page, priority=0, meta={'newsCateId': '20171101140728002'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/guojixinwen/36-%s.html' % page, priority=0, meta={'newsCateId': '20171101140728002'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/zimeiti/677-%s.html' % page, priority=0, meta={'newsCateId': '20171101140728002'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/zhongzhu/172-%s.html' % page, priority=0, meta={'newsCateId': '20171101140728002'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://qx.zhue.com.cn/xingyexinwen/list_731_%s.html' % page, priority=0, meta={'newsCateId': '20171101140728002'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/guojijishu/list_673_%s.html' % page, priority=0, meta={'newsCateId': '20171101140728002'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://js.zhue.com.cn/zhuchangjianshe/31-%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://js.zhue.com.cn/zhuqunbaojian/69-%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://js.zhue.com.cn/fangyiguicheng/72-%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://js.zhue.com.cn/yichuanyuzhong/71-%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://js.zhue.com.cn/rengongshoujing/67-%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://js.zhue.com.cn/yibingfangzhi/3-%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://qx.zhue.com.cn/jishuxinwen/list_732_%s.html' % page, priority=0, meta={'newsCateId': '20171101142701004'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/guoneixinwen/yangzhugushi/list_669_%s.html' % page, priority=0, meta={'newsCateId': '20171101142708005'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/renwuxinwen/121-%s.html' % page, priority=0, meta={'newsCateId': '20171101142708005'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://qx.zhue.com.cn/gaoduanfangtan/list_733_%s.html' % page, priority=0, meta={'newsCateId': '20171101142708005'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/zhengcefagui/16-%s.html' % page, priority=0, meta={'newsCateId': '20171101140923003'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/dianzishangwu/list_586_%s.html' % page, priority=0, meta={'newsCateId': '20171101142714006'}) for page in range(1, 11)])
        cls.start_requests.extend([Request(url='http://cj.zhue.com.cn/wangluoyingxiao/list_588_%s.html' % page, priority=0, meta={'newsCateId': '20171101142714006'}) for page in range(1, 11)])


    @check
    def process(self, response):
        if '404 Not Found' not in response.m_response.content:
            soup = bs(response.m_response.content, 'lxml')

            toutiao_div_list = soup.select('div.warp_left dl.channeldl')
            for toutiao_div in toutiao_div_list:
                if toutiao_div.select('a img'):
                    detail_url = toutiao_div.select('a')[0]['href']
                    img_url = toutiao_div.select('a img')[0]['src']
                    name = toutiao_div.select('h3')[0].text.strip()
                    shortDes = toutiao_div.select('dd.shortdd')[0].text

                    md5 = hashlib.md5()
                    rand_name = str(time.time()) + str(random.random())
                    md5.update(rand_name)
                    img_name = md5.hexdigest() + '.jpg'

                    request = Request(url=img_url, priority=1, callback=self.process_pic)
                    request.meta['img_name'] = img_name
                    yield request

                    request = Request(url=detail_url, priority=1, callback=self.process_detail)
                    request.meta['name'] = name
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
        result['newsFromWebUrl'] = response.request.url
        result['newsFrom'] = soup.select('p.writ span')[1].text.replace('来源：', '')
        result['createTime'] = soup.select('p.writ span')[2].text.replace('时间：', '')
        longDes = soup.select('div#art_content')[0]

        # 去除广告
        adv_list = longDes.select('img[src=http://www.zhue.com.cn/images/zhue888.jpg]')
        for adv in adv_list:
            adv.decompose();

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
    SpiderCore(Zhue_Processor()) \
        .set_pipeline(ConsolePipeline(), 'console') \
        .set_pipeline(PicPipeline(), 'pic') \
        .set_pipeline(DataBasePipeline(), 'database') \
        .start()
