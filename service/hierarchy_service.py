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
    return '/hierarchy/add_member/name/%s' % text


@logger('0')
def get_subordinates_count(cnodes):
    return str(len(cnodes))


@logger()
def get_member_by_name(name):
    return sqlite_dao.query_by_condition(Member, name=name)[0]


@logger(False)
def add_member(member):
    return sqlite_dao.add(member)


if __name__ == '__main__':
    # node = Node(ROOT, ())
    # print print_node(node)

    # print output_node_json()

    print get_member_by_name(u'哈哈')

