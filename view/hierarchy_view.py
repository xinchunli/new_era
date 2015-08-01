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
LIST_MEMBER = 'list_member'
bp = Blueprint(APP_NAME, __name__)


@bp.route('/')
@bp.route('/%s' % INDEX)
def index():
    try:
        json = hierarchy_service.output_node_json()
        return render_template('%s/%s.html' % (ROOT_PATH, INDEX), id=2, json=json)
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


@bp.route('/%s/name/<name>/source/<source>' % SAVE_MEMBER)
def save_member(name, source):
    try:
        member = hierarchy_service.get_member_by_name(name)
        return render_template('%s/%s.html' % (ROOT_PATH, SAVE_MEMBER),
                               name=name, member=member, source=source)
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


@bp.route('/%s/source/<source>' % SAVE_MEMBER_DO, methods=['GET', 'POST'])
def save_member_do(source):
    try:
        if request.method == 'POST':
            member = Member()
            member.name = request.form['name']
            member.id_no = request.form['id_no']
            member.card = request.form['card']
            member.phone = request.form['phone']
            member.email = request.form['email']

            hierarchy_service.add_or_update_member(member)
        if source == LIST_MEMBER:
            return list_member()
        else:
            return index()
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


@bp.route('/%s' % LIST_MEMBER)
def list_member():
    try:
        rel_mem_sup_tuple_list = hierarchy_service.fetch_all_members()
        return render_template('%s/%s.html' % (ROOT_PATH, LIST_MEMBER),
                               id=3, rel_mem_sup_tuple_list=rel_mem_sup_tuple_list)
    except TemplateNotFound:
        # TODO 将这里的try except放入装饰器中，并打印日志
        abort(404)


if __name__ == '__main__':
    print dir(hierarchy_service)
    hierarchy_service.output_node_json()