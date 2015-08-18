# coding:utf-8

__author__ = 'xinchun.li'

from flask import Blueprint, request, render_template, abort
from jinja2 import TemplateNotFound

from common import logger
from service import fileupload_service, hierarchy_service


diagnose = logger.get_logger(logger.DIAGNOSE)

APP_NAME = 'fileupload'
ROOT_PATH = 'fileupload'
INDEX = 'index'
UPLOAD = 'upload'
bp = Blueprint(APP_NAME, __name__)


@bp.route('/')
@bp.route('/%s' % INDEX)
def index(status=None):
    try:
        return render_template('%s/%s.html' % (ROOT_PATH, INDEX), id=4, status=status)
    except TemplateNotFound:
        abort(404)


@bp.route('/%s' % UPLOAD, methods=['GET', 'POST'])
def upload_file():
    status = {}
    if request.method == 'POST':
        file_ = request.files['hierarchy_file']
        ret = fileupload_service.upload_file(file_)
        if ret:
            diagnose.info(u'上传文件成功。')

            node = hierarchy_service.load_from_file()
            ret = hierarchy_service.save_to_db(node)
            if ret:
                diagnose.info(u'保存数据库成功。')
            else:
                diagnose.error(u'保存数据库失败！')
        else:
            diagnose.error(u'上传文件失败！')

        if ret:
            status['ret'] = True
            status['msg'] = u'上传文件成功。'
        else:
            status['ret'] = False
            status['msg'] = u'上传文件失败！'

    return index(status)



if __name__ == '__main__':
    pass