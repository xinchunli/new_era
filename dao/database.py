# coding:utf-8

__author__ = 'xinchun.li'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from common import config
from common import logger
from config import constant


diagnose_logger = logger.get_logger(logger.DIAGNOSE)

db_location = config.get(constant.SQLITE3_DB_LOCATION)
diagnose_logger.info('db_location=' + db_location)
engine = create_engine(db_location, convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))


def init_db():
    metadata.create_all(bind=engine)


def shutdown_session():
    db_session.remove()
