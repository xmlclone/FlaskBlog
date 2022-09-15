from flask import Flask, flash, redirect, request
from flask_wtf.csrf import CSRFError, CSRFProtect

csrf = CSRFProtect()

def init_app(app: Flask):
    # 处理csrf异常
    csrf.init_app(app)
    # 不需要保护的视图，可以使用@csrf.exempt进行屏蔽
    # 开启csrf保护，需要设置WTF_CSRF_SECRET_KEY配置，这个一般和SECRET_KEY一致(默认情况下，也就是不配置这个参数情况下)，也可以自定义
    # 另外可以全局设置 WTF_CSRF_ENABLED = False 进行全局屏蔽，但是强烈建议不这么做
    # 也可以在初始化表单时传递meta={'csrf': False}参数，比如form = FlaskForm(meta={'csrf': False})
    # 注意flask-wtf默认增加了csrf保护，原生的wtform支持，但是不是默认配置，需要自行添加相关的校验
    # 参考: https://wtforms.readthedocs.io/en/3.0.x/csrf/
    @app.errorhandler(CSRFError)
    def error_csrf(exc):
        # 发生csrf异常，使用flash进行提醒，并重定向到原始url
        flash(f'[csrf error] {exc}')
        return redirect(request.url)