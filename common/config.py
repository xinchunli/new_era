# coding:utf-8

__author__ = 'xinchun.li'

import pyetc


conf = pyetc.load(r'D:\workspace\python-workspace\new_era\config\tech.conf')


def get(name, default=None):
    value = getattr(conf, name, default)
    if value is None:
        raise ValueError('No config named %s' % name)
    return value


if __name__ == '__main__':
    print get('host', '1.1.1.1')
    print get('port', 0)

    print get('server')
