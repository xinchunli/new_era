# coding:utf-8

__author__ = 'xinchun.li'

from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from service import hierarchy_service
from model.member import Member


APP_NAME = 'hierarchy'
ROOT_PATH = 'hierarchy'
INDEX = 'index'
SAVE_MEMBER = 'save_member'
SAVE_MEMBER_DO = 'save_member_do'
bp = Blueprint(APP_NAME, __name__)


@bp.route('/')
@bp.route('/%s' % INDEX)
def index():
    try:
        json = hierarchy_service.output_node_json()
        return render_template('%s/%s.html' % (ROOT_PATH, INDEX), json=json)
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


@bp.route('/%s/name/<name>' % SAVE_MEMBER)
def save_member(name):
    try:
        member = hierarchy_service.get_member_by_name(name)
        return render_template('%s/%s.html' % (ROOT_PATH, SAVE_MEMBER), name=name, member=member)
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


@bp.route('/%s/' % SAVE_MEMBER_DO, methods=['GET', 'POST'])
def save_member_do():
    try:
        if request.method == 'POST':
            member = Member()
            member.name = request.form['name']
            member.card = request.form['card']
            member.phone = request.form['phone']
            member.email = request.form['email']

            hierarchy_service.add_or_update_member(member)
        return index()
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


if __name__ == '__main__':
    print dir(hierarchy_service)
    hierarchy_service.output_node_json()