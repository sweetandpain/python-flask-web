from datetime import datetime

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

import time


Bsae = declarative_base()
url = 'mysql+pymysql://root:198788@localhost:3306/?charset=utf8mb4'
e = create_engine(url, echo=True)
Session = sessionmaker(bind=e)


def utctime():
    return int(time.time())


def salt_password(s, salt='$!@><?>HUI&DWQa`'):
    import hashlib
    hash1 = hashlib.sha256()
    hash2 = hashlib.sha256()
    hash1.update(bytes(s, encoding='utf-8'))
    hash2.update(bytes(hash1.hexdigest() + salt, encoding='utf-8'))
    return hash2.hexdigest()


class User(Bsae):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(50), nullable=False)
    image = Column(String(300), default='/static/images/1.jpg')
    signature = Column(String(100), )
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)
    usertype = Column(Integer, default=1)


class News(Bsae):
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


class Todo(Bsae):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    user_id = Column(Integer, nullable=False)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)


class Topic(Bsae):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    user_id = Column(Integer, nullable=False)
    views = Column(Integer, default=0)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)


class Reply(Bsae):
    __tablename__ = 'reply'
    id = Column(Integer, primary_key=True)
    content = Column(String(2000), nullable=False)
    user_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, nullable=False)
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)


def reset_table(table_name):
    with e.connect() as c:
        c.execute('USE webnews')
        
    table_name.metadata.create_all(bind=e)

class orm_test(object):
    def __init__(self):
        self.session = Session()
    
    def add_one(self):
        new1 = News(
            title='147',
            content='asdasd',
            types='1',
        )
        user1 = User(
            username='sweetandpain',
            password=salt_password('123'),
            email='jr10101010@163.com',
            usertype='0',
        )
        todo1 = Todo(
            title='asdasd',
            user_id='1',
        )
        todo2 = Todo(
            title='asdasdzxcasdqwe',
            user_id='1',
        )
        topic = Topic(
            title='asdas的的的sdqwe',
            content='自行车自行车',
            user_id='1',
        )
        self.session.add_all([new1, user1, todo1, todo2, topic])
        self.session.commit()


def main():
    reset_table(News)
    reset_table(User)
    reset_table(Todo)
    reset_table(Topic)
    reset_table(Reply)
    a = orm_test()
    a.add_one()

if __name__ == "__main__":
    main()