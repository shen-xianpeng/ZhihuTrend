# -*- coding: utf-8 -*-
DB_HOST = '127.0.0.1'
# DB_HOST = '127.0.0.1'
DB_USER = 'root'
# DB_USER = 'root'
DB_PWD = 'Smm'
# DB_PWD = '084358'
DB_NAME = 'zhtrend'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import  scoped_session
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base() #create Base lei
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                   (DB_USER, DB_PWD, DB_HOST, DB_NAME),
                 encoding='utf-8', echo=False,
                   pool_size=100, pool_recycle=10)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()



