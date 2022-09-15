import logging
import logging.config

from flask import Flask

def create_app(configfile=None):
    # 初始化实例
    app = Flask(__name__, instance_relative_config=True)
    # 加载配置
    configfile = configfile if configfile else 'config.py'
    app.config.from_pyfile(configfile)
    # 初始化日志
    logging.config.dictConfig(app.config['LOGGING'])
    logger = logging.getLogger('create.app')
    # modles处理
    from .models import init_app as models_init_app
    models_init_app(app)
    # 异常处理
    from .errors import init_app as errors_init_app
    errors_init_app(app)
    # 事件监听
    from .events import init_app as events_init_app
    events_init_app(app)
    # 初始化视图
    from .views import init_app as views_init_app
    views_init_app(app)
    # 首页路由
    app.add_url_rule('/', endpoint='blog.index')
    return app