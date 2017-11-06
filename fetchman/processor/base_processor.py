#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from bs4 import BeautifulSoup as bs
from fetchman.downloader.http.spider_request import Request
from fetchman.utils.decorator import check
from fetchman.scheduler.queue import PriorityQueue
from fetchman.utils import FetchManLogger

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def identity(x):
    return x


class Rule(object):
    def __init__(self, link_extractor, callback=None, process_request=identity, priority=0, only_first=False):
        self.link_extractor = link_extractor
        self.callback = callback
        self.process_request = process_request
        self.priority = priority
        self.only_first = only_first


class LinkExtractor(object):
    def __init__(self, regex_str=None, css_str=None, process_value=None):
        if regex_str:
            self.regex = re.compile(regex_str)
        else:
            self.regex = None
        self.css_str = css_str
        self.process_value = process_value

    @check
    def extract_links(self, response):
        if self.process_value:
            return [response.nice_join(link) for link in self.process_value(response.m_response.content)]
        elif self.regex:
            return [response.nice_join(link) for link in self.regex.findall(response.m_response.content)]
        elif self.css_str:
            soup = bs(response.m_response.content, 'lxml')
            tags = soup.select(self.css_str)
            return [response.nice_join(tag.attrs["href"]) for tag in tags]


class BaseProcessor(object):
    spider_id = None
    start_requests = []
    rules = ()
    allowed_domains = []

    @check
    def process(self, response):
        if hasattr(self, 'rules'):
            rules = getattr(self, 'rules', None)
        else:
            rules = ()
        for rule in rules:
            links = rule.link_extractor.extract_links(response)
            if links:
                for link in links:
                    request = Request(url=link, callback=rule.callback, priority=rule.priority)
                    request = rule.process_request(request)
                    yield request
                    if rule.only_first:
                        break

    @classmethod
    def init_start_requests(cls):
        pass

    @classmethod
    def push_start_request(cls):
        queue = PriorityQueue(cls)
        for start_request in cls.start_requests:
            start_request.duplicate_remove = False
            queue.push(start_request)
            FetchManLogger.logger.info("push start request to queue :" + str(start_request))

    @classmethod
    def push_request(cls, requests):
        if isinstance(requests, list):
            queue = PriorityQueue(cls)
            for request in requests:
                if isinstance(request,Request):
                    request.duplicate_remove = False
                    queue.push(request)
                    FetchManLogger.logger.info("push request to queue :" + str(request))
                else:
                    FetchManLogger.logger.info("param is not Request!")
        elif isinstance(requests, Request):
            queue = PriorityQueue(cls)
            requests.duplicate_remove = False
            queue.push(requests)
            FetchManLogger.logger.info("push request to queue :" + str(requests))
        else:
            FetchManLogger.logger.info("param is not Request!")
