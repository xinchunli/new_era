# coding:utf-8

__author__ = 'xinchun.li'

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

APP_NAME = 'helloworld'
ROOT_PATH = 'helloworld'
INDEX = 'index'
bp = Blueprint(APP_NAME, __name__)


@bp.route('/')
def hello_world():
    try:
        return render_template('%s/%s.html' % (ROOT_PATH, INDEX), id=1)
    except TemplateNotFound:
        abort(404)

