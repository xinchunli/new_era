# coding:utf-8

__author__ = 'xinchun.li'
__emails__ = 'lxc2018@qq.com'

from flask import Flask


app = Flask(__name__)

from views import hierarchy_view
app.register_blueprint(hierarchy_view.bp, url_prefix='/hierarchy')

from views import helloworld_view
app.register_blueprint(helloworld_view.bp, url_prefix='')


if __name__ == '__main__':
    app.debug = True
    app.run()