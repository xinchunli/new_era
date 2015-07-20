# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

import json

from model.csv_file import CsvReader
from model.node import ROOT, Node
from model.member import Member
from common.decorator import logger
from dao import sqlite_dao


@logger("")
def output_node_json():
    """
    输出组织结构树需要的json串

    :return:
    """
    with open('D:\\hierarchy.csv', 'rb') as f:
        reader = CsvReader(f)
        node = reader.get_node()
        if node is None \
                or node.text != ROOT:
            return ""

        dict_ = _get_json_dict(node)
        if not dict_:
            return ""

        return json.dumps(dict_['nodes'], indent=2)


def _get_json_dict(node):
    """
    递归循环node对象的cnodes列表，构造json串的nodes节点
    :param node:
    :return:
    """
    if node is None:
        return None

    dict_ = {
        'text': node.text,
        'href': gen_detail_url(node.text),
        'tags': [get_subordinates_count(node.cnodes)]
    }
    if not node.cnodes:
        return dict_

    dict_['nodes'] = []
    for cnode in node.cnodes:
        dict_['nodes'].append(_get_json_dict(cnode))
    return dict_


@logger('')
def gen_detail_url(text):
    """
    获取会员详情页的url
    :param text:
    :return:
    """
    return '/hierarchy/save_member/name/%s' % text


@logger('0')
def get_subordinates_count(cnodes):
    """
    获取直属下级的数量
    :param cnodes:
    :return:
    """
    return str(len(cnodes))


@logger()
def get_member_by_name(name):
    """
    根据会员姓名获取会员
    :param name:    会员姓名
    :return:        会员对象
    """
    return sqlite_dao.query_by_condition(Member, name=name)[0]


@logger(False)
def add_member(member):
    """
    添加会员信息
    :param member:  会员对象
    :return:        成功或失败
    """
    return sqlite_dao.add(member)


@logger(False)
def update_member(member):
    """
    更新会员信息
    :param member:  会员对象
    :return:        成功或失败
    """
    return sqlite_dao.update(member)


@logger(False)
def add_or_update_member(member):
    """
    若会员不存在则新建会员信息，否则更新会员信息
    :param member:  会员对象
    :return:        成功或失败
    """
    old_member = get_member_by_name(member.name)
    if old_member:
        member.id = old_member.id
        return update_member(member)
    else:
        return add_member(member)


if __name__ == '__main__':
    # node = Node(ROOT, ())
    # print print_node(node)

    # print output_node_json()

    print get_member_by_name(u'哈哈')

