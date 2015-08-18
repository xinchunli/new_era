# coding:utf-8

__author__ = 'xinchun.li'
__emails__ = 'lxc2018@qq.com'

from flask import Flask

from common import logger, config
from config import constant


app = Flask(__name__)
diagnose = logger.get_logger(logger.DIAGNOSE)

# 注册blueprint
from view import hierarchy_view
app.register_blueprint(hierarchy_view.bp, url_prefix='/%s' % hierarchy_view.ROOT_PATH)

from view import helloworld_view
app.register_blueprint(helloworld_view.bp, url_prefix='')

from view import fileupload_view
app.register_blueprint(fileupload_view.bp, url_prefix='/%s' % fileupload_view.ROOT_PATH)

# 设置文件配置
UPLOAD_FOLDER = config.get(constant.FILE_UPLOAD_PATH)
diagnose.info("upload_folder=" + UPLOAD_FOLDER)
MAX_CONTENT_LENGTH = config.get(constant.MAX_CONTENT_LENGTH)
diagnose.info("max_content_length=" + str(MAX_CONTENT_LENGTH))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


from dao import database
@app.teardown_appcontext
def shutdown_session(exception=None):
    database.shutdown_session()

if __name__ == '__main__':
    database.init_db()
    app.debug = True
    app.run()