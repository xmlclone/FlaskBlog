import logging
import typing

from sqlalchemy import exc
from markdown import markdown
from flask_sqlalchemy import Pagination

from .models import db, UserOrm, BlogOrm
from .typing import ErrorMessage

class UserService:
    logger = logging.getLogger('UserService')

    @staticmethod
    def insert(username, password) -> typing.Union[ErrorMessage, None]:
        try:
            db.session.add(UserOrm(username=username, password=password))
            db.session.commit()
        except exc.IntegrityError: # 用户已经存在
            return f'用户: {username} 已经存在，请重新注册'

    @staticmethod
    def select(userid=None, username=None) -> typing.Union[typing.List[UserOrm], None]:
        if userid:
            return UserOrm.query.filter(UserOrm.id == userid).all()
        elif username:
            return UserOrm.query.filter(UserOrm.username == username).all()
        else:
            return UserOrm.query.all()

class BlogService:
    logger = logging.getLogger('BlogService')

    @staticmethod
    def insert(title, body, author_id) -> typing.Union[ErrorMessage, None]:
        try:
            mdcontent = markdown(body, output_format='html')
            db.session.add(BlogOrm(title=title, body=body, html=mdcontent, author_id=author_id))
            db.session.commit()
        except Exception as e:
            return e

    @staticmethod
    def select(blogid=None, author_id=None) -> typing.Union[typing.List[BlogOrm], None]:
        # 排序使用
        # 按创建时间升序排列，即默认的asc方式
        # BlogOrm.query.filter(BlogOrm.id == blogid).order_by(BlogOrm.created).all()
        # 按创建时间降序排列
        # BlogOrm.query.filter(BlogOrm.id == blogid).order_by(BlogOrm.created.desc()).all()
        if blogid:
            return BlogOrm.query.filter(BlogOrm.id == blogid).order_by(BlogOrm.created.desc()).all()
        elif author_id:
            return BlogOrm.query.filter(BlogOrm.author_id == author_id).order_by(BlogOrm.created.desc()).all()
        else:
            return BlogOrm.query.order_by(BlogOrm.created.desc()).all()

    @staticmethod
    def test404():
        # first不需要参数，并且返回一个ORM对象，如果没有则触发404 
        # get_or_404类似于https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.get
        # 的get，它需要一个primary key作为参数，结果和first一样
        # return BlogOrm.query.filter(BlogOrm.id == 1).first_or_404()
        # return BlogOrm.query.filter(BlogOrm.id == -1).first_or_404()
        # return BlogOrm.query.get_or_404(1)
        return BlogOrm.query.get_or_404(-1)

    @staticmethod
    def get_pagination(page=None, per_page=None, author_id=None) -> Pagination:
        if author_id:
            return BlogOrm.query.filter(BlogOrm.author_id == author_id).order_by(BlogOrm.created.desc()).paginate(page=page, per_page=per_page)
        else:
            return BlogOrm.query.order_by(BlogOrm.created.desc()).paginate(page=page, per_page=per_page)

    @staticmethod
    def test_paginate(per_page=None):
        # 注意paginate是flask-sqlalchemy插件的功能，原生的sqlalchemy并没有这个功能，但是可以通过limit等方式实现，也可参考flask插件的方式实现
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate
        # 当前验证期间BlogOrm共有9条数据，以下输出均是基于此数据进行的验证
        '''
        # demo1
        p: Pagination = BlogOrm.query.paginate()
        print(f'paginate object: {p}')
        print(f'paginate total: {p.total}') #9
        print(f'paginate page: {p.page}') #1
        print(f'paginate pages: {p.pages}') #1
        print(f'paginate has_next: {p.has_next}') #False
        print(f'paginate has_prev: {p.has_prev}') #False
        print(f'paginate items: {p.items}') #[<BlogOrm 1>, <BlogOrm 2>, <BlogOrm 3>, <BlogOrm 4>, <BlogOrm 5>, <BlogOrm 6>, <BlogOrm 7>, <BlogOrm 8>, <BlogOrm 9>]
        print(f'paginate next_num: {p.next_num}') #None
        print(f'paginate per_page : {p.per_page}') #20
        print(f'paginate prev_num : {p.prev_num}') #None
        print(f'paginate query : {p.query}') #具体的query对象， 打印出来就是一个select语句
        # SELECT blog.id AS blog_id, blog.author_id AS blog_author_id, blog.created AS blog_created, blog.title AS blog_title, blog.body AS blog_body, blog.star AS blog_star, blog.html AS blog_html FROM blog
        print(f'paginate prev : {p.prev()}')
        print(f'paginate next : {p.next()}')
        for page in p.iter_pages():
            print(f'paginate iter_pages : {page}') #1
        '''

        # demo2
        # 会执行多条sql语句，一条是limit ? offset ?，另外一条是count(*)，也就是limit限制的是per_page参数，offset是根据上一次查询的偏移量
        # 其实是根据(page - 1) * per_page获取到的数据，即flask_sqlalchemy并没有记录相关的偏移量，是根据我们传递的参数进行计算的
        p: Pagination = BlogOrm.query.paginate(per_page=5) #per_page指定每页最大数量
        # print(f'paginate object: {p}')
        # print(f'paginate total: {p.total}') #9
        # print(f'paginate page: {p.page}') #1 当前页
        # print(f'paginate pages: {p.pages}') #2 总页数
        # print(f'paginate has_next: {p.has_next}') #True 因为有两页，并且当前在第一页
        # print(f'paginate has_prev: {p.has_prev}') #False
        # print(f'paginate items: {p.items}') #[<BlogOrm 1>, <BlogOrm 2>, <BlogOrm 3>, <BlogOrm 4>, <BlogOrm 5>] 当前页的数据
        # print(f'paginate next_num: {p.next_num}') #2 下一页序号
        # print(f'paginate per_page : {p.per_page}') #5 每页数量
        # print(f'paginate prev_num : {p.prev_num}') #None 上一页序号
        # print(f'paginate query : {p.query}') #具体的query对象， 打印出来就是一个select语句
        # # SELECT blog.id AS blog_id, blog.author_id AS blog_author_id, blog.created AS blog_created, blog.title AS blog_title, blog.body AS blog_body, blog.star AS blog_star, blog.html AS blog_html FROM blog
        # print(f'paginate prev : {p.prev()}') # 上一页对象，虽然没有，但是也是一个对象
        # print(f'paginate next : {p.next()}') # 下一页对象
        # for page in p.iter_pages():
        #     print(f'paginate iter_pages : {page}, items: {type(page)}') #1 2

        p1: Pagination = BlogOrm.query.paginate(page=1, per_page=5) #page参数表示从当前页获取per_page条数据
        p1: Pagination = BlogOrm.query.paginate(page=2, per_page=5)
        p1: Pagination = BlogOrm.query.paginate(page=3, per_page=5)
        p1: Pagination = BlogOrm.query.paginate(page=4, per_page=5)
        # print(f'p1 paginate items: {p1.items}') #[<BlogOrm 6>, <BlogOrm 7>, <BlogOrm 8>, <BlogOrm 9>]

        # iter_pages(left_edge=2,left_current=2,right_current=5,right_edge=2)
        # 假设当前共有100页，当前页为50页，按照默认的参数设置调用iter_pages获得的列表为：
        # [1,2,None,48,49,50,51,52,53,54,55,None,99,100]
        # 即edge表示最前最后显示的数量，current表示当前页前后显示的数量

        # p: Pagination = BlogOrm.query.paginate(per_page=per_page)
        return p

    @staticmethod
    def update(blogid, title, body) -> typing.Union[ErrorMessage, None]:
        try:
            # udpate需要使用session的commit功能
            BlogOrm.query.filter(BlogOrm.id == blogid).update({
                BlogOrm.body: body, 
                BlogOrm.title: title,
                BlogOrm.html: markdown(body, output_format='html')
            })
            # 另外一种可选方式，先查询在更新，都需要commit
            # blog.title = title
            # blog.body = body
            db.session.commit()
        except Exception as e:
            return e

    @staticmethod
    def like(blogid) -> typing.Union[ErrorMessage, None]:
        try:
            BlogOrm.query.filter(BlogOrm.id == blogid).update({BlogOrm.star: BlogOrm.star + 1})
            db.session.commit()
        except Exception as e:
            return e

    @staticmethod
    def delete(blogid) -> typing.Union[ErrorMessage, None]:
        try:
            # delete同理，也需要commit
            BlogOrm.query.filter(BlogOrm.id == blogid).delete()
            # 另外一种可选方式，先查询数据在删除，都需要commit
            # db.session.delete(blog)
            db.session.commit()
        except Exception as e:
            return e
