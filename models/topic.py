import time

from models.base_model import db
from sqlalchemy import Column, Integer, String

from models.user import User
from models.reply import Reply


def utctime():
    return int(time.time())


class Topic(db.Model):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    user_id = Column(Integer, nullable=False)
    views = Column(Integer, default=0)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)

    @classmethod
    def all_topic(cls):
        all = cls.query.all()
        return all

    @classmethod
    def get(cls, id):
        t = cls.query.filter_by(id=id).first()
        t.views = t.views + 1
        db.session.add(t)
        db.session.commit()
        return t

    @classmethod
    def add_topic(cls, form, user_id):
        title = form['title']
        content = form['content']
        t = cls(title=title, content=content, user_id=user_id)
        db.session.add(t)
        db.session.commit()

    @classmethod
    def one(cls, title):
        t = cls.query.filter_by(title=title).first()
        return t

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.onetopic_reply(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count