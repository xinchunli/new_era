# coding:utf-8

__author__ = 'xinchun.li'

import datetime
import sys

from common import logger

error_logger = logger.get_logger(logger.ERROR)


def error_log(default=None):
    """

    :param default: 被装饰的函数默认的返回值
    :return:
    """

    def _error_log(func):
        """

        :param func:    被装饰的函数
        :return:
        """

        def __error_log(*args, **kwargs):
            """

            :param args:    被装饰函数的位置参数
            :param kwargs:  被装饰函数的关键字参数
            :return:
            """
            begin_time = datetime.datetime.now()
            try:
                return func(*args, **kwargs)
            except Exception, e:
                end_time = datetime.datetime.now()
                try:
                    if args[0].__class__ is type:
                        class_ = args[0]
                    else:
                        class_ = args[0].__class__
                    error_logger.error('%s.%s() execute error: %s, time: %s, args: %s, kwargs: %s' %
                                       (class_.__name__, func.__name__, e, end_time - begin_time, args, kwargs))

                except:
                    module = sys.modules[func.__module__]
                    error_logger.error('%s.%s() execute error: %s, time: %s, args: %s, kwargs: %s' %
                                       (module.__name__, func.__name__, e, end_time - begin_time, args, kwargs))
            return default

        return __error_log

    return _error_log


def to_string(func):
    """

    :param func:    被装饰的函数
    :return:
    """

    def _to_string(*args, **kwargs):
        """

        :param args:    被装饰函数的位置参数
        :param kwargs:  被装饰函数的关键字参数
        :return:
        """
        ret = func(*args, **kwargs)

        if not args:
            error_logger.error('%s() is not a instance method!' % func.__name__)
            return ret

        try:
            obj = args[0]
            return '%s=%s' % (obj.__class__, obj.__dict__)
        except Exception, e:
            error_logger.error('%s() to string error! %s' % (func.__name__, e))

        return ret

    return _to_string
