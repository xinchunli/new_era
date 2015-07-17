# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from common.decorator import to_string, logger


ROOT = u'根节点'


class Node:
    def __init__(self, text, cnodes):
        """

        :param text:
        :param cnodes:
        """
        self.text = text
        self.cnodes = cnodes

    @to_string
    def __str__(self):
        pass

    __repr__ = __str__

    @logger
    def append_cnodes(self, node):
        self.cnodes.append(node)


if __name__ == '__main__':
    node = Node('aaa', None)
    print node
    node.append_cnodes(None)
    # @to_string
    # def aaa(x):
    #     pass
    # aaa(1)
    # @to_string
    # def bbb():
    #     pass
    # bbb()
