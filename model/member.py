# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper

from dao.database import metadata
from common.decorator import to_string


class Member:
    def __init__(self, name=None, id_no=None, phone=None, card=None, email=None):
        self.name = name
        self.id_no = id_no
        self.phone = phone
        self.card = card
        self.email = email

    @to_string
    def __str__(self):
        pass

    __repr__ = __str__


member = Table('member', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(50), unique=True),
               Column('id_no', Integer, unique=True),
               Column('phone', Integer),
               Column('card', String(50)),
               Column('email', String(120)))

mapper(Member, member)


if __name__ == '__main__':
    member = Member(u'Kevin')
    print member

