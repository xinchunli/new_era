# coding:utf-8

__author__ = 'xinchun.li'

import logging
import datetime
import sys


def logger(default=None):
    """

    :param default: 被装饰的函数默认的返回值
    :return:
    """

    def _logger(func):
        """

            :param func:    被装饰的函数
        :return:
        """

        def __logger(*args, **kwargs):
            """

            :param args:    被装饰函数的位置参数
            :param kwargs:  被装饰函数的关键字参数
            :return:
            """
            begin_time = datetime.datetime.now()
            result = default
            try:
                result = func(*args, **kwargs)
            except Exception, e:
                end_time = datetime.datetime.now()
                try:
                    if args[0].__class__ is type:
                        class_ = args[0]
                    else:
                        class_ = args[0].__class__
                    logging.error('%s.%s() execute time: %s, error: %s, args: %s, kwargs: %s' %
                                  (class_, func.__name__, end_time - begin_time, e, args, kwargs))

                except:
                    module = sys.modules[func.__module__]
                    logging.error('%s.%s() execute time: %s, error: %s, args: %s, kwargs: %s' %
                                  (module, func.__name__, end_time - begin_time, e, args, kwargs))
            return result

        return __logger

    return _logger


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
            logging.error('%s() is not a instance method!' % func.__name__)
            return ret

        try:
            obj = args[0]
            return '%s=%s' % (obj.__class__, obj.__dict__)
        except Exception, e:
            logging.error('%s() to string error! %s' % (func.__name__, e))

        return ret

    return _to_string