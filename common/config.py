# coding:utf-8


import pyetc


conf = pyetc.load(r'../config/new_era.conf')


def get(name, default=None):
    if default is not None:
        return getattr(conf, name, default)
    else:
        value = getattr(conf, name, default)
        if value is None:
            raise ValueError('No config named %s' % name)
        return value


if __name__ == '__main__':
    print get('host', '1.1.1.1')
    print get('port', 0)

    print get('server')
