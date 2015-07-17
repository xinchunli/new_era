# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from dao.database import db_session, init_db
from common.decorator import logger


class MyTransaction:
    def __init__(self, session):
        self.session = session
        self.status = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session is None:
            return

        if exc_type is None:
            try:
                self.session.commit()
                self.status = True
            except Exception, exc_sql:
                self.session.rollback()
                raise exc_sql
        else:
            self.session.rollback()
            raise exc_type


@logger
def add(obj):
    """

    :param obj:
    :return:
    """
    with MyTransaction(db_session) as transaction:
        db_session.add(obj)
    return transaction.status


@logger
def add_all(objs):
    """

    :param objs:
    :return:
    """
    with MyTransaction(db_session) as transaction:
        for obj in objs:
            db_session(obj)
    return transaction.status


@logger
def delete(obj):
    """

    :param obj:
    :return
    """
    with MyTransaction(db_session) as transaction:
        db_session.delete(obj)
    return transaction.status


@logger
def query_all(cls):
    """

    :param cls:
    :return:
    """
    return db_session.query(cls).all()


if __name__ == '__main__':
    from model.member import Member

    init_db()
    member = Member(u'Lee', 12345678901, 'abcdefg', 'kevin@gmail.com')
    print 'add status: ', add(member)

    members = query_all(Member)
    print members
    print 'delete status: ', delete(members[0])