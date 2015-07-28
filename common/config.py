# coding:utf-8


import pyetc


conf = pyetc.load(r'../config/new_era.conf')


def get(name, default):
    return getattr(conf, name, default)


if __name__ == '__main__':
    print get('host', '1.1.1.1')
    print get('port', 0)
