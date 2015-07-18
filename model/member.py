# coding:utf-8

__author__ = 'xinchun.li'

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper

from dao.database import metadata
from common.decorator import to_string


class Member(object):
    def __init__(self, name=None, phone=None, card=None, email=None):
        self.name = name
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
               Column('phone', Integer),
               Column('card', String(50)),
               Column('email', String(120)))

mapper(Member, member)


if __name__ == '__main__':
    member = Member(u'Kevin')
    print member
