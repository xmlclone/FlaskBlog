from flask import Flask
from flask_pagedown import PageDown
from flask_simplemde import SimpleMDE

from .auth import bp as auth_bp
from .blog import bp as blog_bp
from .demo import bp as demo_bp

page_down = PageDown()
simple_mde = SimpleMDE()

def init_app(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(demo_bp)
    page_down.init_app(app)
    simple_mde.init_app(app)