import time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models.base_model import db
from models.user import User
from models.news import News
from models.topic import Topic
from models.reply import Reply

from routes import current_user
from routes.index import main as index_routes
from routes.routes_news import main as news_routes
from routes.api_todo import todo_api
from routes.routes_todo import main as todo_routes
from routes.routes_topic import main as topic_routes
from routes.routes import main as main_blueprint
from routes.events import socketio

import secret


class MyModelView(ModelView):
    def is_accessible(self):
        u = current_user()
        if u.usertype == 0:
            return True
        else:
            return False


# 自定义过滤器
def count(input):
    return len(input)


# 自定义过滤器
def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


# 注册路由函数
def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(news_routes)
    app.register_blueprint(todo_routes)
    app.register_blueprint(todo_api)
    app.register_blueprint(topic_routes)
    app.register_blueprint(main_blueprint)


def configured_app():
    app = Flask(__name__)

    # session密钥
    app.secret_key = secret.session_secret_key

    # sqlalchemy连接数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost:3306/webnews?charset=utf8mb4'.format(
        secret.database_password
    )
    db.init_app(app)

    # 配置flask-admin
    admin = Admin(app, name='无权限', template_mode='bootstrap3')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(News, db.session))
    admin.add_view(MyModelView(Topic, db.session))
    admin.add_view(MyModelView(Reply, db.session))

    # 注册路由
    register_routes(app)

    #设置jinja2自定义过滤器
    app.template_filter()(count)
    app.template_filter()(format_time)

    # socket聊天室
    socketio.init_app(app)

    app.debug = True

    return app


if __name__ == "__main__":
    app = configured_app()
    # config = dict(
    #     debug=True,
    #     host='0.0.0.0',
    #     port=3000,
    # )
    # app.run(**config)
    socketio.run(app, host='localhost', port=3000)