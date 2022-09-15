import logging

from flask import Flask
from flask_pagedown import PageDown
from flask_simplemde import SimpleMDE
# 增加对flask_login的支持
# 注意在当前使用时Werkzeug2.2.2和Flask-Login==0.6.1貌似不兼容
# 需要修改site-packages\flask_login\utils.py的如下引入
# from werkzeug.routing import parse_rule 修改为下面的方式(修改后，重启flask服务)
# from werkzeug.urls import url_parse as parse_rule
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from blog.service import UserService

from .auth import bp as auth_bp
from .blog import bp as blog_bp
from .demo import bp as demo_bp

from .edemo.jwt_demo import bp as demo_jwt_bp

logger = logging.getLogger('views')

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

jwt_manager = JWTManager()
@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    logger.debug(f'user_identity_loader: {user}')
    return user

@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # {'fresh': False, 'iat': 1663243159, 'jti': '349eb619-4833-4720-bd70-02d905abec03', 'type': 'access', 'sub': 1, 'nbf': 1663243159, 'exp': 1663244059}
    logger.debug(f'user_lookup_loader: {jwt_data}')
    identity = jwt_data["sub"]
    return identity

def init_app(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(demo_bp)
    page_down.init_app(app)
    simple_mde.init_app(app)
    # 增加对flask_login的支持
    login_manager.init_app(app)

    # jwt_demo
    jwt_manager.init_app(app)
    app.register_blueprint(demo_jwt_bp)