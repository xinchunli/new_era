# coding:utf-8

__author__ = 'xinchun.li'

import sys
import os


def get_module():

    def main_module_name():
        mod = sys.modules['__main__']
        file_ = getattr(mod, '__file__', None)
        return file_ and os.path.splitext(os.path.basename(file_))[0]

    def modname(dict_):

        file_, name = dict_.get('__file__'), dict_.get('__name__')
        if file_ is None or name is None:
            return None

        if name == '__main__':
            name = main_module_name()
        return name

    # print globals()
    return modname(globals())


if __name__ == '__main__':
    print get_module()
    module = get_module()
    print sys.modules
    print sys.modules['__main__']
    g = globals()
    print type(g['__builtins__'])