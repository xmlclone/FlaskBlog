from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length
# https://pypi.org/project/Flask-PageDown/
# 需要在html模板中引入相关的js支持: <head>{{ pagedown.include_pagedown() }}</head>
# 目前看效果pagedown效果不好,代码片段没有很好的支持
from flask_pagedown.fields import PageDownField

class RegisterForm(FlaskForm):
    username = StringField(
        label='用户名', 
        validators=[Length(min=4, max=20, message='用户名长度在4-20之间')]
    )
    password = PasswordField(
        label='密码', 
        validators=[Length(min=6, max=20, message='密码长度必须在6-20之间')]
    )
    submit = SubmitField(label='注册')

class LoginForm(FlaskForm):
    username = StringField(
        label='用户名', 
        validators=[Length(min=4, max=20, message='用户名长度在4-20之间')]
    )
    password = PasswordField(
        label='密码', 
        validators=[Length(min=6, max=20, message='密码长度必须在6-20之间')]
    )
    submit = SubmitField(label='登录')

class BlogViewForm(FlaskForm):
    body = TextAreaField(label='内容')

class BlogAddForm(FlaskForm):
    title = StringField(
        label='标题', 
        validators=[Length(min=1, max=20, message='文章标题长度需要在1-20之间')]
    )
    # body = PageDownField(label='内容')
    body = TextAreaField(label='内容')
    submit = SubmitField(label='创建')

class BlogUpdateForm(FlaskForm):
    title = StringField(
        label='标题', 
        validators=[Length(min=1, max=20, message='文章标题长度需要在1-20之间')]
    )
    body = TextAreaField(label='内容')
    submit = SubmitField(label='保存')