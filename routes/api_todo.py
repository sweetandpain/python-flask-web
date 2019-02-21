from flask import (
    jsonify,
    request,
    Blueprint,
)
from routes import current_user
from models.todo import Todo
from routes import (
    current_user,
    salt_password,
    new_csrf_token,
    # csrf_tokens,
)

todo_api = Blueprint('todo_api', __name__)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@todo_api.route('/api/todo/all', methods=['GET'])
def all():
    u = current_user()
    uid = u.id
    todos = Todo.all_todos(user_id=uid)
    todos_dict = []
    for t in todos:
        todo = {
            'id': t.id,
            'title': t.title,
            'user_id': t.user_id,
            'created_time': t. created_time,
            'updated_time': t.updated_time,
        }
        todos_dict.append(todo)
    return jsonify(todos_dict)


@todo_api.route('/api/todo/add', methods=['POST'])
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    u = current_user()
    Todo.add_todo(title=form['title'], user_id=u.id)
    t = Todo.one_todo(title=form['title'], user_id=u.id)
    todo = {
        'id': t.id,
        'title': t.title,
        'user_id': t.user_id,
        'created_time': t. created_time,
        'updated_time': t.updated_time,
    }
    # 把创建好的 todo 返回给浏览器
    return jsonify(todo)


@todo_api.route('/api/todo/delete', methods=['GET'])
def delete():
    todo_id = int(request.args['id'])
    Todo.delete(id=todo_id)
    d = dict(
        message="成功删除 todo"
    )
    return jsonify(d)


@todo_api.route('/api/todo/update', methods=['POST'])
def update():
    """
    用于增加新 todo 的路由函数
    """
    form = request.get_json()
    todo_id = int(form['id'])
    title = form['title']
    Todo.update(todo_id, title=title)
    t = Todo.one_todo(id=todo_id)
    todo = {
        'id': t.id,
        'title': t.title,
        'user_id': t.user_id,
        'created_time': t. created_time,
        'updated_time': t.updated_time,
    }
    return jsonify(todo)
