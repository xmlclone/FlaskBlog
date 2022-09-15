from flask import Blueprint, render_template, views, request, url_for

from blog.service import BlogService

bp = Blueprint('demo', __name__, url_prefix='/demo')

@bp.route('/test_html_extend')
def test_html_extend():
    return render_template('demo/extend2.html', var=1)

@bp.route('/test_html_include')
def test_html_include():
    return render_template('demo/include2.html', var=1)

@bp.route('/test_html_macro')
def test_html_macro():
    return render_template('demo/macro2.html', var=1)

@bp.route('/test_page')
def test_page():
    pagination = BlogService.test_paginate(1)
    return render_template('demo/page.html', pagination=pagination)

@bp.route('/css_display')
def css_display():
    return render_template('demo/css/css_display.html')

@bp.route('/css_float')
def css_float():
    return render_template('demo/css/css_float.html')

@bp.route('/css_flex')
def css_flex():
    return render_template('demo/css/css_flex.html')

@bp.route('/url_param_test1')
# http://127.0.0.1:5000/demo/url_param_test1?a=1
def url_param_test1():
    # return request.args.get('a')
    return url_for('demo.url_param_test1', a=1, b=2) #/demo/url_param_test1?a=1&b=2

@bp.route('/url_param_test2/<string:b>')
# http://127.0.0.1:5000/demo/url_param_test2/123?a=3
def url_param_test2(b):
    # return request.args.get('a') + b
    return url_for('demo.url_param_test2', a=1, b=b) #/demo/url_param_test2/123?a=1

class UrlParamCls1(views.MethodView):
    def get(self, b=3):
        return url_for('demo.url_param_test3', a=1, b=2) + str(b)

class UrlParamCls2(views.MethodView):
    def get(self, b=3):
        return url_for('demo.url_param_test4', a=1, b=2) + str(b)

bp.add_url_rule('/url_param_test3', view_func=UrlParamCls1.as_view('url_param_test3'))
bp.add_url_rule('/url_param_test4/<string:b>', view_func=UrlParamCls2.as_view('url_param_test4'))