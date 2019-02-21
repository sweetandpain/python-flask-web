from models.base_model import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import time


def utctime():
    return int(time.time())


class Todo(db.Model):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    user_id = Column(Integer, nullable=False)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)

    @classmethod
    def all_todos(cls, **kwargs):
        all = cls.query.filter_by(**kwargs).all()
        return all

    @classmethod
    def add_todo(cls, **kwargs):
        todo1 = cls(**kwargs)
        db.session.add(todo1)
        db.session.commit()

    @classmethod
    def one_todo(cls, **kwargs):
        todo2 = cls.query.filter_by(**kwargs).first()
        return todo2

    @classmethod
    def delete(cls, **kwargs):
        todo = cls.query.filter_by(**kwargs).first()
        db.session.delete(todo)
        db.session.commit()

    @classmethod
    def update(cls, id, **kwargs):
        todo = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(todo, name, value)
        todo.updated_time = utctime()
        db.session.add(todo)
        db.session.commit()
