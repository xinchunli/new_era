# coding:utf-8

__author__ = 'xinchun.li'

import logging
import logging.config


ROOT = 'root'
ERROR = 'error'
SQL = 'sql'

logging.config.fileConfig(r'D:\workspace\python-workspace\new_era\config\logger.conf')


def get_logger(name=None):
    return logging.getLogger(name)


if __name__ == '__main__':
    logger = get_logger(ERROR)
    logger.debug('This is debug message')
    logger.info('This is info message')
    logger.warning('This is warning message')
    logger.error('This is error message')