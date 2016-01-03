# -*- coding: utf-8 -*-
#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from db_conf import DB_USER, DB_PWD, DB_HOST, DB_NAME

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                   (DB_USER, DB_PWD, DB_HOST, DB_NAME),
                    encoding='utf-8', echo=False,
                    pool_size=100, pool_recycle=10)