from flask import Flask, session, g

from .service import UserService

def init_app(app: Flask):
    # 增加请求前处理
    @app.before_request
    def befor_request_events():
        userid = session.get('userid')
        # g.user = UserService.select(userid=userid)[0] if userid else None