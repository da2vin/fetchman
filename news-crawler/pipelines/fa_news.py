#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class News(Base):
    # 表的名字:
    __tablename__ = 'NewsProduct'

    # 表的结构:
    newsProductId = Column(String(20), primary_key=True)
    newsCateId = Column(String(20))
    name = Column(String(100), primary_key=True)
    newsFrom = Column(String(100))
    status = Column(Integer())
    auditStatus = Column(Integer())
    createTime = Column(DateTime())
    longDes = Column(String(0))
    imageUrl = Column(String(200))
    shortDes = Column(String(300))
    newsFromWebUrl = Column(String(100))


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@127.0.0.1:3306/fa_news')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
