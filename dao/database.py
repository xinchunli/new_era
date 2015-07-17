# coding:utf-8

__author__ = 'xinchun.li'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:////new_era/test.db', convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))


def init_db():
    metadata.create_all(bind=engine)


def shutdown_session():
    db_session.remove()
