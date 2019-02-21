from models.base_model import db
from sqlalchemy import Column, Integer, String
import time
from models.user import User

def utctime():
    return int(time.time())


class Reply(db.Model):
    __tablename__ = 'reply'
    id = Column(Integer, primary_key=True)
    content = Column(String(2000), nullable=False)
    user_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, nullable=False)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)

    @classmethod
    def onetopic_reply(cls, **kwargs):
        all = cls.query.filter_by(**kwargs).all()
        return all

    @classmethod
    def reply_add(cls, form, topic_id, user_id):
        content = form['content']
        r = cls(content=content, topic_id=topic_id, user_id=user_id)
        db.session.add(r)
        db.session.commit()

    def user(self):
        u = User.one(id=self.user_id)
        return u