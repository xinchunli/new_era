# coding:utf-8

__author__ = 'xinchun.li'
__emails__ = 'lxc2018@qq.com'

from flask import Flask


app = Flask(__name__)

from view import hierarchy_view
app.register_blueprint(hierarchy_view.bp, url_prefix='/%s' % hierarchy_view.ROOT_PATH)

from view import helloworld_view
app.register_blueprint(helloworld_view.bp, url_prefix='')


from dao import database
@app.teardown_appcontext
def shutdown_session(exception=None):
    database.shutdown_session()

if __name__ == '__main__':
    database.init_db()
    app.debug = True
    app.run()