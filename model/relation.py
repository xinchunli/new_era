# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper

from dao.database import metadata
from common.decorator import to_string


class Relation:
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid

    @to_string
    def __str__(self):
        pass

    __repr__ = __str__


relation = Table('relation', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String(50), unique=True),
                 Column('pid', Integer))

mapper(Relation, relation)


if __name__ == '__main__':
    relation = Relation(u'Lee', 1)
    print relation