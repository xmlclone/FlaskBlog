import typing
import click

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, validator

# flask_sqlalchemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

db = SQLAlchemy()

class UserModel(BaseModel):
    id: typing.Optional[int]
    username: str
    password: str
    
    class Config:
        orm_mode = True

class UserOrm(db.Model):
    # 如果ORM类需要初始化__init__，必须调用父类的__init__
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

class BlogModel(BaseModel):
    id: typing.Optional[int]
    author_id: int
    created: typing.Optional[datetime]
    title: str
    body: typing.Optional[str]
    star: typing.Optional[int]
    html: typing.Optional[str]

    class Config:
        orm_mode = True

    @validator('created')
    def created_validator(cls, created):
        return created.strftime("%Y-%m-%d %H:%M:%S")

class BlogOrm(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, nullable=False)
    # created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text)
    star = db.Column(db.Integer, nullable=False, default=0)
    html = db.Column(db.Text)

@click.command('init-db', help='初始化数据库')
def init_db():
    db.drop_all()
    db.create_all()

def init_app(app: Flask):
    db.init_app(app)
    app.cli.add_command(init_db)