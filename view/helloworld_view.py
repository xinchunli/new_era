# coding:utf-8

__author__ = 'xinchun.li'

from flask import Blueprint

APP_NAME = 'helloworld'
bp = Blueprint(APP_NAME, __name__)

@bp.route('/')
def hello_world():
    return 'Hello World!'

