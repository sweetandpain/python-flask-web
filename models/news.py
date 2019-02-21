from models.base_model import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import time


def utctime():
    return int(time.time())


class News(db.Model):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300), )
    author = Column(String(20), )
    view_count = Column(Integer)
    is_valid = Column(Boolean)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)

    @classmethod
    def all_news(cls):
        all = cls.query.all()
        return all