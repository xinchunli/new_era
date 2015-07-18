# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

import json

from model.csv_file import CsvReader
from model.node import ROOT, Node
from common.decorator import logger


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
        'href': '#',
        'tags': [str(len(node.cnodes))]
    }
    if not node.cnodes:
        return dict_

    dict_['nodes'] = []
    for cnode in node.cnodes:
        dict_['nodes'].append(_get_json_dict(cnode))
    return dict_


if __name__ == '__main__':
    # node = Node(ROOT, ())
    # print print_node(node)

    print output_node_json()

