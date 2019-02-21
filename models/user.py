from models.base_model import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import time


def utctime():
    return int(time.time())


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(50), nullable=False)
    image = Column(String(300), default='/static/images/1.jpg')
    signature = Column(String(100), )
    # 以下插入的是数据插入时间
    created_time = Column(Integer, default=utctime)
    # 以下插入的是程序部署时间
    # created_time = Column(Integer, default=utctime())
    updated_time = Column(Integer, default=utctime)
    usertype = Column(Integer, default=1)

    @classmethod
    def one(cls, **kwargs):
        u = cls.query.filter_by(**kwargs).first()
        return u
    
    @classmethod
    def register(cls, **kwargs):
        user = cls(**kwargs)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update(cls, id, **kwargs):
        u = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(u, name, value)
        u.updated_time = utctime()
        db.session.add(u)
        db.session.commit()