# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from dao.database import db_session, init_db
from common.decorator import error_log
from common import logger


sql_logger = logger.get_logger(logger.SQL)


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


@error_log(False)
def add(obj):
    """
    向数据库中插入一条数据
    :param obj: 要插入的对象
    :return:    成功或失败
    """
    with MyTransaction(db_session) as transaction:
        db_session.add(obj)
    return transaction.status


@error_log(False)
def update(obj):
    """
    将数据库中的一条数据更新为obj对象的属性
    :param obj:
    :return:
    """
    with MyTransaction(db_session) as transaction:
        db_session.merge(obj)
    return transaction.status


@error_log(False)
def add_all(objs):
    """
    向数据库中插入多条数据
    :param objs:要插入的对象列表
    :return:    成功或失败
    """
    with MyTransaction(db_session) as transaction:
        db_session.add_all(objs)
    return transaction.status


@error_log(False)
def delete(obj):
    """
    从数据库中删除一条数据
    :param obj: 要删除的对象
    :return:    成功或失败
    """
    with MyTransaction(db_session) as transaction:
        db_session.delete(obj)
    return transaction.status


@error_log(False)
def delete_all(cls):
    """
    从数据库中删除一张表所有的数据
    :param cls: 数据表对应的类
    :return:    成功或失败
    """
    objs = query_all(cls)
    with MyTransaction(db_session) as transaction:
        for obj in objs:
            db_session.delete(obj)
    return transaction.status


@error_log([])
def query_all(cls):
    """
    从数据库中查询所有数据
    :param cls: 数据表对应的类
    :return:    符合条件的对象列表
    """
    query_statement = db_session.query(cls)
    sql_logger.debug(query_statement)
    return query_statement.all()


@error_log()
def query_by_id(cls, id):
    """
    从数据库中查询id为指定id的数据
    :param cls: 数据表对应的类
    :param id:  数据的id
    :return:    符合条件的对象
    """
    query_statement = db_session.query(cls).filter(cls.id == id)
    sql_logger.debug(query_statement)
    return query_statement.first()


@error_log([])
def query_by_condition(cls, **condition):
    """
    从数据库中查询条件为指定条件的数据
    :param cls: 数据表对应的类
    :param condition:  查询条件字典
    :return:    符合条件的对象列表
    """
    query_statement = db_session.query(cls)
    for key, value in condition.items():
        query_statement = query_statement.filter(getattr(cls, key) == value)
    sql_logger.debug(query_statement)
    return query_statement.all()


@error_log([])
def query_all_left_join(left_cls, right_cls, left_key=None, right_key=None):
    """

    :param left_cls:
    :param right_cls:
    :param left_key:
    :param right_key:
    :return:
    """
    if left_key and right_key:
        query_statement = db_session.query(left_cls, right_cls). \
            outerjoin(right_cls, getattr(left_cls, left_key) == getattr(right_cls, right_key))
        sql_logger.debug(query_statement)
        return query_statement.all()
    else:
        query_statement = db_session.query(left_cls).outerjoin(right_cls)
        sql_logger.debug(query_statement)
        return query_statement.all()


if __name__ == '__main__':
    init_db()

    from model.member import Member
    #
    # member = Member(u'Lee', 12345678901, 'abcdefg', 'kevin@gmail.com')
    # print 'add status: ', add(member)
    #
    # members = query_all(Member)
    # print 'query_all result: ', members
    #
    # member = query_by_id(Member, 1)
    # print 'query_by_id result: ', member
    #
    # members = query_by_condition(Member, name=u'Lee')
    # print 'query_by_condition result: ', members
    # # print 'delete status: ', delete(members[0])
    #
    # member = members[0]
    # member.phone = 11111111111
    # print 'update status: ', update(member)

    from model.relation import Relation
    # relation = Relation(u'Lee', 0)
    # add(relation)
    # print relation.id

    query_list = query_all_left_join(Relation, Member, 'name', 'name')
    for query in query_list:
        print query

