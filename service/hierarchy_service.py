# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

import json

from model.csv_file import CsvReader
from model.node import ROOT
from model.member import Member
from model.relation import Relation
from common.decorator import error_log
from common import config
from common import logger
from config import constant
from dao import sqlite_dao


diagnose_logger = logger.get_logger(logger.DIAGNOSE)


@error_log("")
def output_node_json():
    """
    输出组织结构树需要的json串

    :return:
    """
    file_path = config.get(constant.CSV_FILE_FULLPATH)
    with open(file_path, 'rb') as f:
        reader = CsvReader(f)
        node = reader.get_node()
        if node is None \
                or node.text != ROOT:
            return ""

        dict_ = _get_json_dict(node)
        if not dict_:
            return ""

        return json.dumps(dict_['nodes'], indent=2)


def load_from_db():
    pass


@error_log()
def load_from_file():
    file_path = config.get(constant.CSV_FILE_FULLPATH)
    diagnose_logger.info('file_path=' + file_path)
    with open(file_path, 'rb') as f:
        reader = CsvReader(f)
        return reader.get_node()


@error_log(False)
def save_to_db(node):
    """

    :param node:
    :return:
    """

    def _save_to_db(node, pid):
        """

        :param node:
        :param pid:
        :return:
        """
        if node is None:
            return

        if node.text != ROOT:
            relation = Relation(node.text, pid)
            if not sqlite_dao.add(relation):
                return
            pid = relation.id

        if not node.cnodes:
            return

        for cnode in node.cnodes:
            _save_to_db(cnode, pid)
    sqlite_dao.delete_all(Relation)
    _save_to_db(node, 0)
    return True


@error_log()
def save_to_file(node, pid):
    pass

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


@error_log('')
def gen_detail_url(text):
    """
    获取会员详情页的url
    :param text:
    :return:
    """
    return '/hierarchy/save_member/name/%s/source/index' % text


@error_log('0')
def get_subordinates_count(cnodes):
    """
    获取直属下级的数量
    :param cnodes:
    :return:
    """
    return str(len(cnodes))


@error_log()
def get_member_by_name(name):
    """
    根据会员姓名获取会员
    :param name:    会员姓名
    :return:        会员对象
    """
    members = sqlite_dao.query_by_condition(Member, name=name)
    if members:
        return members[0]


@error_log(False)
def add_member(member):
    """
    添加会员信息
    :param member:  会员对象
    :return:        成功或失败
    """
    return sqlite_dao.add(member)


@error_log(False)
def update_member(member):
    """
    更新会员信息
    :param member:  会员对象
    :return:        成功或失败
    """
    return sqlite_dao.update(member)


@error_log(False)
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


@error_log([])
def fetch_all_members():
    """
    获取所有会员对象

    :return:    会员、关系元组列表
    """
    rel_mem_tuple_list = sqlite_dao.query_all_left_join(Relation, Member, 'name', 'name')
    rel_sup_tuple_list = sqlite_dao.query_all_self_join(Relation, Relation, 'pid', 'id')

    relation_list = map(lambda x: x[0], rel_mem_tuple_list)
    member_list = map(lambda x: x[1], rel_mem_tuple_list)
    superior_list = map(lambda x: x[1], rel_sup_tuple_list)
    return zip(relation_list, member_list, superior_list)


@error_log([])
def fetch_all_relations():
    return sqlite_dao.query_all(Relation)


if __name__ == '__main__':
    # node = Node(ROOT, ())
    # print print_node(node)

    # print output_node_json()

    # print get_member_by_name(u'哈哈')
    node = load_from_file()
    print node

    save_to_db(node)

    relations = fetch_all_relations()

    for relation in relations:
         print relation.id, relation.name, relation.pid

    # print fetch_all_members()


