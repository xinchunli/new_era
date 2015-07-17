# coding:utf-8

__author__ = 'xinchun.li'

import logging
import datetime
import sys


def logger(func):
    def _logger(*args, **kwargs):
        begin_time = datetime.datetime.now()
        ret = None
        try:
            ret = func(*args, **kwargs)
        except Exception, e:
            end_time = datetime.datetime.now()
            try:
                logging.error('%s.%s() execute time: %s, error: %s' %
                              (args[0].__class__, func.__name__, end_time - begin_time, e))
            except:
                logging.error('%s.%s() execute time: %s, error: %s' %
                              (sys.modules[func.__module__], func.__name__, end_time - begin_time, e))
        return ret
    return _logger


def to_string(func):
    def _to_string(*args, **kwargs):
        ret = func(*args, **kwargs)

        if not args:
            logging.error('%s() is not a instance method!' % func.__name__)
            return ret

        try:
            obj = args[0]
            return '%s=%s' % (obj.__class__, obj.__dict__)
        except Exception, e:
            logging.error('%s() to string error! %s' % (func.__name__, e))

        return ret
    return _to_string