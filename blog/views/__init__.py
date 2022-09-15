from flask import Flask
from flask_pagedown import PageDown
from flask_simplemde import SimpleMDE
# 增加对flask_login的支持
# 注意在当前使用时Werkzeug2.2.2和Flask-Login==0.6.1貌似不兼容
# 需要修改site-packages\flask_login\utils.py的如下引入
# from werkzeug.routing import parse_rule 修改为下面的方式(修改后，重启flask服务)
# from werkzeug.urls import url_parse as parse_rule
from flask_login import LoginManager

from blog.service import UserService

from .auth import bp as auth_bp
from .blog import bp as blog_bp
from .demo import bp as demo_bp

page_down = PageDown()
simple_mde = SimpleMDE()

# 增加对flask_login的支持
login_manager = LoginManager()
# 登录的页面
login_manager.login_view = 'auth.login'
# 当用户被重定向到登录页面时flash的消息
login_manager.login_message = '拒绝访问'
# 必须设定的回调函数，也就是从session加载用户时使用，必须返回一个User对象或None
# 这个User类，参考UserMixin的基本实现
# 回调函数的唯一一个参数是userid，用于唯一标识用户的信息
@login_manager.user_loader
def load_user(userid):
    users = UserService.select(userid=userid)
    if users:
        return users[0]

def init_app(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(demo_bp)
    page_down.init_app(app)
    simple_mde.init_app(app)
    # 增加对flask_login的支持
    login_manager.init_app(app)