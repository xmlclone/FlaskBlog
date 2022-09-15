# config文件应该放在instance目录下，这里为了归档放到了此处

import os
import logging

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'instance')

# ===================================================================app===================================================================
SECRET_KEY = 'DEV'

# 开启csrf保护，需要设置WTF_CSRF_SECRET_KEY配置，这个一般和SECRET_KEY一致(默认不配置的情况下)，也可以自定义
WTF_CSRF_SECRET_KEY = SECRET_KEY

# ===================================================================db===================================================================

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "blog.db")}'
# 数据库连接地址格式,其中driver可以省略,如果省略则表示使用一些知名的driver
# port端口如果是默认的,也可以省略
# 更多可以参考: https://docs.sqlalchemy.org/en/14/core/engines.html
# dialect+driver://username:password@host:port/database

# postgresql://scott:tiger@localhost:5432/mydatabase # 默认使用driver是: psycopg2
# postgresql+psycopg2://scott:tiger@localhost/mydatabase
# postgresql+pg8000://scott:tiger@localhost/mydatabase

# mysql://scott:tiger@localhost/foo #默认mysqlclient 
# mysql+mysqldb://scott:tiger@localhost/foo
# mysql+pymysql://scott:tiger@localhost/foo

# oracle://scott:tiger@127.0.0.1:1521/sidname #默认cx_oracle 
# oracle+cx_oracle://scott:tiger@tnsname

# mssql+pyodbc://scott:tiger@mydsn #默认pyodbc 
# mssql+pymssql://scott:tiger@hostname:port/dbname

# sqlite:///foo.db
# sqlite:////absolute/path/to/foo.db #unix
# sqlite:///C:\\path\\to\\foo.db #windows
# r'sqlite:///C:\path\to\foo.db' #windows
# sqlite:// #memory

# 是否打印底层sql，这个是控制控制台是否输出，日志无法控制这块内容
# 如果日志也输出到了控制台，这里也设置为True，那么控制台会打印两个重复的日志
SQLALCHEMY_ECHO = False

# 后续版本会删除,暂时设置为False屏蔽warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGGING = {
    'version': 1,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s',
        },
        'file': {
            'format': '%(asctime)s %(levelname)s %(name)s %(filename)s(%(lineno)d): %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': logging.INFO,
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'blog.log'),
            'when': 'D',
            # 'when': 'M',
            'backupCount': 10,
            'level': logging.DEBUG,
        },
        'sqlalchemy_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'sqlalchemy.log'),
            'when': 'D',
            # 'when': 'M',
            'backupCount': 10,
            'level': logging.INFO,
        },
        'werkzeug_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'werkzeug.log'),
            'when': 'D',
            # 'when': 'M',
            'backupCount': 10,
            'level': logging.INFO,
        }
    },
    'loggers': {
        'sqlalchemy': {
            'level': logging.INFO,
            'propagate': False,
            'handlers': ['sqlalchemy_file']
        },
        'werkzeug': {
            'level': logging.INFO,
            'propagate': False,
            'handlers': ['console', 'werkzeug_file']
        }
    },
    'root': {
        'level': logging.DEBUG,
        'handlers': ['console', 'file']
    },
}