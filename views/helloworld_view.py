# coding:utf-8

__author__ = 'xinchun.li'

from flask import Blueprint


bp = Blueprint('helloworld', __name__)

@bp.route('/')
def hello_world():
    return 'Hello World!'

