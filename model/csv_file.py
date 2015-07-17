# coding:utf-8

__author__ = 'xinchun.li'
__metaclass__ = type

from csv import DictReader

from common.decorator import logger, to_string
from model.node import Node, ROOT


class CsvReader(DictReader):
    @logger
    def __init__(self, f):
        DictReader.__init__(self, f)
        self._node = Node(ROOT, [])
        self.col_num = 0
        self._init()

    @to_string
    def __str__(self):
        pass

    __repr__ = __str__

    def _init(self):
        def get_index(line):
            default_index = -1
            if line is None:
                return default_index

            for index, ele in enumerate(line):
                if is_text(ele):
                    return index

            return default_index

        def is_text(ele):
            if not ele:
                return False
            if ' ' in ele \
                    or '|' in ele \
                    or '-' in ele \
                    or '+' in ele:
                return False
            return True

        def __init(gnode, pnode, node_stack, reader, last_index):
            """

            :param gnode: 祖父节点
            :param pnode: 父节点
            :param node_stack: 父节点栈
            :param reader:
            :param last_index:
            :return:
            """
            try:
                line = reader.next()
                cur_index = get_index(line)
                text = line[cur_index].decode('gbk')
                cnode = Node(text, [])

                # 计算列数
                if len(line) > self.col_num:
                    self.col_num = len(line)

                # 计算行数
                self.line_num += 1

                # 兄弟节点
                if cur_index == last_index:
                    # 挂在祖父节点下
                    gnode.append_cnodes(cnode)
                    # 递归调用
                    __init(gnode, cnode, node_stack, reader, cur_index)
                # 子节点
                elif cur_index - last_index == 1:
                    # 挂在父节点下
                    pnode.append_cnodes(cnode)
                    # 将父节点压入栈
                    node_stack.append(pnode)
                    # 递归调用
                    __init(pnode, cnode, node_stack, reader, cur_index)
                # 既不是子节点也不是兄弟节点
                elif cur_index < last_index:
                    while last_index - cur_index >= 0:
                        # 循环弹出栈，找到父节点
                        pnode = node_stack.pop()
                        last_index -= 1
                    # 挂在父节点下
                    pnode.append_cnodes(cnode)
                    # 将父节点压入栈
                    node_stack.append(pnode)
                    # 递归调用
                    __init(pnode, cnode, node_stack, reader, cur_index)
                # 非法节点，退出
                else:
                    # TODO 非法节点处理
                    return
            # 循环结束，退出
            except StopIteration:
                return

        rnode = self._node
        reader = self.reader
        last_index = -1
        node_stack = []
        __init(None, rnode, node_stack, reader, last_index)

    def get_col_num(self):
        return self.col_num

    def get_line_num(self):
        return self.line_num

    def get_node(self):
        return self._node


if __name__ == '__main__':
    reader = CsvReader(file('D:\\hierarchy.csv', 'rb'))

    node = reader.get_node()
    print reader

    def print_node(node, c):
        if node is None:
            return
        # print c
        print c + node.text
        if not node.cnodes:
            return
        for cnode in node.cnodes:
            print_node(cnode, c + '--')

    print_node(node, '|')

    # print reader
    # for line in reader.reader:
    #     print line
    #
    # print '****************'
    # for line in reader.reader:
    #     print line
    # print reader
    # print reader.__dict__
    # # print reader.reader
    print reader.get_col_num()
    print reader.get_line_num()
    # print reader.get_node()
    # a = [1,2,3,4,5]
    # print a.pop()
    # a.append(6)
    # print a
    # print a.pop()
    # print a