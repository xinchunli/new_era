# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from sqlalchemy.orm import aliased

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
def query_all_left_join(cls_left, cls_right, key_left=None, key_right=None):
    """
    左外连接两张表，获取两张表连接后的集合
    :param cls_left:    左表对应的类
    :param cls_right:   右表对应的类
    :param key_left:    左表连接的列名，为空时默认连接id
    :param key_right:   右表连接的列名，为空时默认连接id
    :return:    两个类的对象元组列表，例[(obj_left1, obj_right1), (obj_left2, obj_right2), (...), ...]
    """
    if key_left and key_right:
        query_statement = db_session.query(cls_left, cls_right)\
            .outerjoin(cls_right, getattr(cls_left, key_left) == getattr(cls_right, key_right))\
            .order_by(cls_left.id)
        sql_logger.debug(query_statement)
        return query_statement.all()
    else:
        query_statement = db_session.query(cls_left, cls_right)\
            .outerjoin(cls_right)\
            .order_by(cls_left.id)
        sql_logger.debug(query_statement)
        return query_statement.all()


@error_log([])
def query_all_self_join(cls1, cls2, key1=None, key2=None):
    """
    自连接一张表，获取该表自连接后的集合
    :param cls1:    该表对应的类
    :param cls2:    该表对应的类
    :param key1:    表1连接的列名，为空时默认连接id
    :param key2:    表2连接的列名，为空时默认连接id
    :return:    两个类的对象元组列表，例[(obj1_1, obj2_1), (obj1_2, obj2_2), (...), ...]
    """
    cls1_alias = aliased(cls1)
    cls2_alias = aliased(cls2)
    if key1 and key2:
        query_statement = db_session.query(cls1_alias, cls2_alias)\
            .outerjoin(cls2_alias, getattr(cls1_alias, key1) == getattr(cls2_alias, key2))\
            .order_by(cls1_alias.id)
        sql_logger.debug(query_statement)
        return query_statement.all()
    else:
        query_statement = db_session.query(cls1_alias, cls2_alias)\
            .outerjoin(cls2_alias)\
            .order_by(cls1_alias.id)
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

    # query_list = query_all_left_join(Relation, Member, 'name', 'name')
    # for query in query_list:
    #     print query

    query_list1 = query_all_self_join(Relation, Relation, 'pid', 'id')
    print query_list1

