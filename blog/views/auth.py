import logging
import functools

from flask import Blueprint, views, render_template, request, flash, redirect, url_for, session, g

from blog.service import UserService

from .wtf import RegisterForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

class RegisterView(views.MethodView):
    def __init__(self):
        self.logger = logging.getLogger(RegisterView.__name__)

    def get(self):
        form = RegisterForm()
        return render_template('auth/register.html', form=form)

    def post(self):
        form = RegisterForm()
        # flask-wtf插件新增的validate_on_submit，submit相当于是flask新增的，会判断请求方法是否是: {"POST", "PUT", "PATCH", "DELETE"}
        # 原始的wtf只有validate
        # 会校验请求数据有效并且验证csrf保护
        if form.validate_on_submit():
            # 要获取wtf表单数据，需要使用.data获取具体的值
            username = form.username.data
            password = form.password.data
            self.logger.debug(f'Rigster username: {username}, password: {password}')
            error = UserService.insert(username=username, password=password)
            if error:
                flash(error)
                return redirect(url_for('auth.register'))
            flash('注册成功，请登录')
            return redirect(url_for('auth.login'))
        else:
            self.logger.error(f'{form.username.errors}')
            self.logger.error(f'{form.password.errors}')
            self.logger.error(f'{form.errors}')
            return redirect(url_for('auth.register'))

class LoginView(views.MethodView):
    def __init__(self):
        self.logger = logging.getLogger(LoginView.__name__)

    def get(self):
        form = LoginForm()
        return render_template('/auth/login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            self.logger.debug(f'Login username: {username}, password: {password}')
            error = None
            user = UserService.select(username=username)[0]
            self.logger.debug(f'{user}')
            if user:
                if password != user.password:
                    error = f'密码错误'
            else:
                error = f'用户: {username} 不存在'
            if error:
                session.clear()
                flash(error)
                return redirect(url_for('auth.login'))
            session['userid'] = user.id
            # 验证session对象，session对象也是在当前请求上下文有效，并不是跨请求的
            # 当设置了session后,默认的session会通过secret_key加密,通过设置客户端的cookies(key就是session,value是加密数据)
            # 客户端下次请求的时候携带了这个cookies,然后session获取到后进行解密,设置为session对应的属性
            # 那么session对象在不同的请求中,获取到的同一个属性,比如这里的userid在不同的请求中值是不一样的,而且也不会影响其它请求的session
            # 因为session是当前请求有效,并且值是根据客户端携带的cookies进行计算的
            # self.logger.debug(dir(session))
            # self.logger.debug(id(session))
            # self.logger.debug(session.keys())
            flash(f'用户: {username} 登录成功')
            return redirect(url_for('blog.index'))
        else:
            self.logger.error(f'{form.username.errors}')
            self.logger.error(f'{form.password.errors}')
            self.logger.error(f'{form.errors}')
            return redirect(url_for('auth.login'))

bp.add_url_rule('/register', view_func=RegisterView.as_view('register'))
bp.add_url_rule('/login', view_func=LoginView.as_view('login'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

def login_require(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if 'user' in g and g.user is not None:
            return view(*args, **kwargs)
        else:
            flash('请先登录')
            return redirect(url_for('auth.login'))
    return wrapper