# 项目使用到的一些内容记录

1. flask
2. sqlalchemy
1. wtform
1. pydantic
1. restful
1. click
1. logging
1. jinja
3. ajax
4. jquery
5. html
1. css
1. sqlite

> 后续增加redis mysql/pgsql vue等的使用集成

## 项目自定义的一些组件/框架

1. 分页组件(templates/components/pagination.html)，其它jinja模板里面可以直接调用这个宏实现分页，参考blog/index.html的使用方式

# 初次使用

1. 首先根据requirements.txt安装依赖,可以使用清华的源: https://pypi.tuna.tsinghua.edu.cn/simple
1. 首先应该在blog同级目录下手动创建`instance`目录(因为我们系统并没有自动创建这个目录)
2. 应该把blog下的`config.py`文件修改为实际的配置项后,放置到上面创建的`instance`目录下
3. 初次使用应该先使用命令行`flask --app blog init-db`初始化数据库

# 说明

## markdown支持

1. 使用过flask-pagedown,发现效果不是很好,转而使用富文本编辑器CKEditor,参考的: [为你的Flask项目添加富文本编辑器](https://zhuanlan.zhihu.com/p/23583960?refer=flask)
2. 后面又使用了[Flask-SimpleMDE](https://flask-simplemde.readthedocs.io/en/latest/)插件来支持md
3. 三方插件的js代码，如果没有修改原生代码，则未上传到git，另外instance目录也未归档到git

# 一些额外知识记录

## flask

### url_for与view视图类

```python
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

# 即url_for传递额外的参数，构造的url会根据实际的路由函数而定
# 如果url_for传递的参数，在路由函数中有定义，比如上面url_param_test2的b参数，那么会作为url的一部分传入，可以直接通过参数名获取到值
# 但是url_param_test2和url_param_test1都没有定义a这个参数，那么会作为url的查询参数部分传入，需要通过request.args获取值

# 同理，视图类也遵循相同的原则，只不过url的匹配是通过add_url_rule处设置的
class UrlParamCls1(views.MethodView):
    def get(self, b=3):
        return url_for('demo.url_param_test3', a=1, b=2) + str(b)

class UrlParamCls2(views.MethodView):
    def get(self, b=3):
        # 同理支持参数名获取url的参数，通过request.args获取url的查询参数
        return url_for('demo.url_param_test4', a=1, b=2) + str(b)

# url参数在这里进行设定，url_for也同理，根据get是否有额外的参数而确定应该是url参数还是查询参数
bp.add_url_rule('/url_param_test3', view_func=UrlParamCls1.as_view('url_param_test3'))
bp.add_url_rule('/url_param_test4/<string:b>', view_func=UrlParamCls2.as_view('url_param_test4'))
```

## css

### 选择器

```css
/*
两个元素并排，没有其它修饰，比如 div p 表示选择div下所有的p，不管p处于哪一个层级，只要在div下就生效
两个元素并排，有>修饰，比如 div > p 表示选择div下第一个p层级，只影响div下第一层p

上面两种描述适用于.#的类和ID选择符
比如:
li.pagination-item > a 表示选取class为pagination的所有li下的第一个层级的a
.content label 表示选择class为content下所有label，不分层级

多个选择器如果有相同的样式使用,即可，比如:
.content input, .content textarea { margin-bottom: 1em; }
表示.content input这个选择器和.content textarea这个选择器有相同的样式
*/
```

### 盒模型

从内容到最外层分为: content -> padding -> border -> margin

> 盒子的宽度 = width + padding-left + padding-right + border-left + border-right + margin-left + margin-right
> 盒子的高度 = height + padding-top + padding-bottom + border-top + border-bottom + margin-top + margin-bottom

> 注意: 很多浏览器默认body会有margin 8px，故一般可以使用如下代码设置为0。其实类似很多的元素都有默认的margin，比如我们常见的`p`

```css
body {
    margin: 0px;
    padding: 0px;
}
```

> 另外如果想让某一个盒子在页面左右居中显示，可以通过margin设置生效，比如:

```css
body {
    /* 即上下设置间距为0，左右设置为auto */
    margin: 0 auto;
}
```

### 块级元素和行内元素

#### 行内元素

> 行内元素也可以叫内联元素

1. 无法设置宽高
2. 针对padding和margin设置左右有效，上下无效
3. 默认情况下行内元素可以多个行内元素共存一行，即与其它行内元素并排

#### 块级元素

1. 可以设置宽高
2. padding、margin设置均有效
3. 自动换行
4. 块默认是从上到下排列
5. 不能与其它任何元素并排

### 盒模型相关的几个属性

```css
a {
    /* display有4个取值，
    none就是不渲染元素(注意和visibility属性的区别) 
    block表示是块级元素
    inline表示是内联元素，通过inline和block可以在行内和块级元素之间转换
    */
    display: none;

    /* 指定float后，元素变成块级元素，更准确的理解是inline-block类型，即同时具有内联和块级元素的特征
    none默认值，不浮动
    right向右浮动
    left向左浮动

    我们标准的文档流类似于水流一样，自上而下排列，不管是行内还是块级元素，只要一行满了就换行继续
    增加float后，元素就脱离了标准文档流，浮起来了，类似于漂浮在了标准文档流上
    对行内和块级元素的一个直接影响是: 行内元素可以设置宽高了、块级元素可以多个在同一行了

    浮动是相对于父元素就行浮动的，如果父元素的位置改变了，浮动也相当于父元素进行浮动

    指定了float的元素会浮动到包含边框(父元素)或者碰到另外一个浮动边框为止。其它非浮动元素该怎么排列仍然继续排列
     */
    float: left;

    /*指定元素某个方向不允许出现浮动元素
    none默认值，允许浮动元素出现
    left,左侧不允许有浮动元素
    right
    both 左右两侧均不允许
    注意只有左右，没有上下的概念
    */
    clear: none
}
```

### 参考

1. [css中float详解](https://blog.csdn.net/pingchuanz/article/details/82903397)
2. [常见的行内和块级元素](https://www.cnblogs.com/gujun1998/p/13917970.html)

# 扩展插件的用法

## flask-login

```python
from flask_login import login_user, logout_user, login_required
# 增加对flask_login的支持
# 注意在当前使用时Werkzeug2.2.2和Flask-Login==0.6.1貌似不兼容
# 需要修改site-packages\flask_login\utils.py的如下引入
# from werkzeug.routing import parse_rule 修改为下面的方式(修改后，重启flask服务)
# from werkzeug.urls import url_parse as parse_rule
from flask_login import LoginManager, UserMixin

# 首先必须要有1个User对象，插件提供了一个基本的UserMixin，我们在定义ORM时可以直接继承
# 注意必须要有1个ID字段，通常情况下ORM也会有此字段
class UserOrm(db.Model, UserMixin):
    ...

# 初始化LoginManager，并配置一些基本信息
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

# 在你的登录视图里面，经过确认后，认为用户登录成功则
login_user(UserOrm())

# 在需要受保护的视图上加上
@login_required
def get(self):

# 退出的时候调用
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))

# 在html模板或者python代码里面均可以使用current_user这个对象代表UserOrm，并且其有一些属性可以使用，比如
current_user.is_authenticated # flask-login的属性，其实也就是上面继承了UserMixin和db.Model时的全部字段均可以使用
current_user.username # ORM的字段
current_user.id
```

> 更多参考: 
> https://github.com/maxcountryman/flask-login
> http://www.pythondoc.com/flask-login/

# flask一些常见扩展

1. flask-admin: 一个类似django admin的后台管理插件
2. flask-sqlalchemy: 一个基于sqlalchemy的ORM插件
3. flask-migrate: 一个sqlalchemy迁移工具
4. flask-jwt-extended: 一个JWT认证插件
5. flask-limiter: 接口请求频率限制插件
6. flask-mail: 邮件插件
7. flask-wtf: wtf表单插件
8. flask-login: 认证
9. flask-script: 插件脚本
10. flask-restful: restful插件
11. flask-bootstrap: bootstrap插件
12. flask-moment: 本地化日志和时间插件
13. Connexion - Swagger/OpenAPI 第一个基于 Flask 的 Python 框架，具有自动端点验证和 OAuth2 支持
14. Flask-MongoRest - 围绕 MongoEngine 的 Restful API 框架
15. Eve - 由 Flask、MongoDB 和良好意图提供支持的 REST API 框架
16. Flask-Restless - 用于从 SQLAlchemy 模型创建简单的 ReSTful API 的 Flask 扩展、
17. Flask-RestPlus - 语法糖、助手和自动生成的 Swagger 文档。
18. Flask-Potion - Flask 和 SQLAlchemy 的 RESTful API 框架
19. Zappa - 在 AWS Lambda 和 API Gateway 上构建和部署无服务器 Flask 应用程序
20. Flask-Analytics - Flask 框架的分析片段生成器扩展
21. Flask-Matomo - 使用 Matomo 跟踪对 Flask 网站的请求
22. Flask-Security - Flask 应用程序的快速简单的安全性
23. Flask-User - 可自定义的 Flask 用户帐户管理
24. Flask-HTTPAuth - 为 Flask 路由提供基本和摘要 HTTP 身份验证的简单扩展
25. Flask-Praetorian - Flask API 的强大、简单和精确的安全性（使用 jwt）
26. Authlib - Authlib 是一个雄心勃勃的身份验证库，适用于 OAuth 1、OAuth 2、OpenID 客户端、服务器等
27. Authomatic - Authomatic 为许多使用 OAuth 1.0a（Twitter、Tumblr 等）和 OAuth 2.0（Facebook、Foursquare、GitHub、Google、LinkedIn、PayPal 等）的提供商提供开箱即用的支持
28. Flask-Pundit - 基于 Rails 的Pundit gem 的扩展，为您的模型组织访问控制提供了简单的方法
29. Flask-Dance - Flask 的 OAuth 消费者扩展，附带对 Facebook、GitHub、Google 等的预设支持
30. Flask-MongoEngine - 带有 WTF 模型表单支持的 MongoEngine 烧瓶扩展
31. Flask-Session - Flask 的服务器端会话扩展
32. Flask-Caching - 为 Flask 添加简单的缓存支持
33. flask-heroku-cacheify - Heroku 上的自动 Flask 缓存配置
35. flask-babel - i18n 和 l10n 支持基于 Babel 和 pytz 的 Flask
36. SQLAlchemy-Searchable - Flask-SQLAlchemy 的全文搜索（仅限 Postgres）
37. Flask-Dramatiq - Flask 应用程序的Dramatiq集成。
38. huey - python 的一个小任务队列
39. Flask-RQ - Flask 应用程序的 RQ（Redis 队列）集成
40. celery - 分布式任务队列
41. sentry-sdk - Sentry的Python 客户端。
42. airbrake-python -Airbrake的Python 客户端
43. flask-zipkin - 使用Zipkin进行分布式跟踪。
44. Flask-OpenTracing - 使用OpenTracing进行分布式跟踪。
45. elastic-apm - Python 的弹性 APM 代理
46. Flask-GoogleMaps - 在我们的 Flask 模板中构建和嵌入谷歌地图
47. Flask-Gravatar - Flask 中小而简单的 gravatar 用法
48. Flask-Pusher - Flask 的 Pusher 集成
49. Flask-Azure-Storage - 提供与 Azure 存储集成的 Flask 扩展
50. Flask-CORS - 用于处理跨域资源共享 (CORS) 的 Flask 扩展，使跨域 AJAX 成为可能
51. flask-assets - Flask 网络资产集成
52. flask-s3 - 从 Amazon S3 无缝地为您的 Flask 应用程序的静态资产提供服务
53. Flask-SSLify - 在您的 Flask 应用程序上强制使用 SSL
54. Flask-HTMLmin - Flask html 缩小器
1. Flasgger - 使用 Swagger 2.0 规范为 Flask 视图创建 API 文档
1. flask-apispec - 带有烧瓶的简单自记录 API
1. flask2postman - 从您的 Flask 应用程序生成 Postman 集合
1. flask_profiler - Flask 的端点分析器/分析器
1. Flask-DebugToolbar - django 调试工具栏到烧瓶的端口
1. flask-debug-toolbar-mongo - Flask 调试工具栏的 MongoDB 面板
1. Flask-Testing - Flask 的单元测试扩展
1. pytest-flask - 一组用于测试 Flask 应用程序的 pytest 夹具
1. Flask-MonitoringDashboard - 自动监控 Flask/Python Web 服务不断发展的性能。
1. nplusone - 使用 Flask 和 SQLAlchemy 自动检测 n+1 查询
1. connexion - Swagger/OpenAPI 第一个基于 Flask 的 Python 框架，具有自动端点验证和 OAuth2 支持.
1. flask-marshmallow Flask + marshmallow 用于漂亮的 API
1. flask-jsonrpc - Flask 驱动站点的基本 JSON-RPC 实现
1. Flask-Bcrypt - Flask-Bcrypt 是一个 Flask 扩展，为您的应用程序提供 bcrypt 哈希实用程序
1. Mixer - Mixer 是生成 Django 或 SQLAlchemy 模型实例的应用程序
1. Flask-FeatureFlags - 一个基于配置启用或禁用功能的 Flask 扩展
1. Flask-Reggie - Flask URL 路由的正则表达式转换器
1. Flask-SocketIO - Flask 应用程序的 Socket.IO 集成
1. Flask-Moment - 使用 moment.js 在 Flask 模板中格式化日期和时间
1. Flask-Paginate - 对 Flask 的分页支持
1. Flask-graphql - 为您的 Flask 应用程序添加 GraphQL 支持
