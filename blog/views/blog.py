import logging

from flask import Blueprint, render_template, views, request, flash, redirect, url_for, g
from flask_sqlalchemy import Pagination

from blog.service import BlogService, UserService
from blog.models import BlogModel

from .auth import login_require
from .wtf import BlogAddForm, BlogUpdateForm, BlogViewForm

bp = Blueprint('blog', __name__, url_prefix='/blog')

class BlogIndexView(views.MethodView):
    def __init__(self):
        self.logger = logging.getLogger(BlogIndexView.__name__)

    def get(self):
        page = request.args.get('page')
        page = page if page is None else int(page)
        per_page = int(request.args.get('per_page', 5))
        self.logger.debug(f'page: {page}, per_page: {per_page}')
        # 分页显示每页显示的数量
        # posts = BlogService.select()
        pagination: Pagination = BlogService.get_pagination(page=page, per_page=per_page)
        for post in pagination.items:
            setattr(post, 'username', UserService.select(userid=post.author_id)[0].username)
            # setattr(post, 'form', BlogViewForm(body=post.body))
        # return render_template('blog/index.html', posts=posts)
        return render_template('blog/index.html', pagination=pagination, per_page=per_page)

class BlogAddView(views.MethodView):
    def __init__(self):
        self.logger = logging.getLogger(BlogAddView.__name__)

    @login_require
    def get(self):
        form = BlogAddForm()
        return render_template('blog/add.html', form=form)

    @login_require
    def post(self):
        form = BlogAddForm()
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            self.logger.debug(f'Current create blog user is: {g.user.username}')
            error = BlogService.insert(title=title, body=body, author_id=g.user.id)
            if error:
                flash(error)
                return redirect(url_for('blog.create'))
            flash('创建文章成功')
            return redirect(url_for('blog.index'))
        else:
            self.logger.error(f'{form.title.errors}')
            self.logger.error(f'{form.body.errors}')
            self.logger.error(f'{form.errors}')
            return redirect(url_for('blog.index'))

class BlogUpdateView(views.MethodView):
    def __init__(self):
        self.logger = logging.getLogger(BlogUpdateView.__name__)

    @login_require
    def get(self):
        # form = BlogUpdateForm()
        post_id = request.args.get('post_id')
        post = BlogService.select(blogid=post_id)[0]
        self.logger.debug(f'Update blog id: {post_id}')
        # 第二种给表单传递默认值的方式,可以结合html模板解释进行了解
        form = BlogUpdateForm(title=post.title, body=post.body)
        return render_template('blog/update.html', post=post, form=form)
        # 因为删除要post的ID,故上面是传递了post变量,也可以改为post_id变量,让模板直接获取这个变量即可
        # return render_template('blog/update.html', form=form)

    @login_require
    def post(self):
        form = BlogUpdateForm()
        post_id = request.args.get('post_id')
        if form.validate_on_submit():
            title = request.form['title']
            body = request.form['body']
            self.logger.debug(f'Current update blog user is: {g.user.username}, post id: {post_id}')
            error = BlogService.update(blogid=post_id, title=title, body=body)
            if error:
                flash(error)
                return redirect(url_for('blog.create'))
            flash('编辑文章成功')
            return redirect(url_for('blog.index'))
        else:
            self.logger.error(f'{form.title.errors}')
            self.logger.error(f'{form.body.errors}')
            self.logger.error(f'{form.errors}')
            return redirect(url_for('blog.update', post_id=post_id))

bp.add_url_rule('/', view_func=BlogIndexView.as_view('index'))
bp.add_url_rule('/add', view_func=BlogAddView.as_view('create'))
bp.add_url_rule('/update', view_func=BlogUpdateView.as_view('update'))

@bp.route('/delete', methods=['POST'])
@login_require
def delete():
    # post_id = request.args.get('post_id')
    post_id = request.form['post_id']
    error = BlogService.delete(blogid=post_id)
    if error:
        flash(f'删除失败: {error}')
        return redirect(url_for('blog.update', post_id=post_id))
    flash('删除文章成功')
    return redirect(url_for('blog.index'))

@bp.route('/view')
def view():
    post_id = request.args.get('post_id')
    blog = BlogService.select(blogid=post_id)[0]
    setattr(blog, 'username', UserService.select(userid=blog.author_id)[0].username)
    form = BlogViewForm(body=blog.body)
    return render_template('blog/view.html', post=blog, form=form)

@bp.route('/like')
def like():
    post_id = request.args.get('post_id')
    BlogService.like(post_id)
    # 前端采用了jquery ajax，故这里需要返回点赞后文章的点赞最新数量
    blog = BlogService.select(blogid=post_id)[0]
    # 无法直接返回ORM，必须返回一个字典类型的数据，flask会自动转换为json格式
    return BlogModel.from_orm(blog).dict()
    # return redirect(url_for('blog.view', post_id=post_id))

# 测试404
@bp.route('/demo/test404')
def test404():
    print(BlogService.test404())
    return 'test404'

# 测试paginate
@bp.route('/demo/test_paginate')
def test_paginate():
    p: Pagination = BlogService.test_paginate()
    return 'test_paginate'