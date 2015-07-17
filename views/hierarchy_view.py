# coding:utf-8

__author__ = 'xinchun.li'

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from services import hierarchy_service


bp = Blueprint('hierarchy', __name__)

@bp.route('/', defaults={'page': 'index'})
@bp.route('/<page>')
def index(page):
    try:
        json = hierarchy_service.output_node_json()
        return render_template('hierarchy/%s.html' % page, json=json)
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


if __name__ == '__main__':
    print dir(hierarchy_service)
    hierarchy_service.output_node_json()