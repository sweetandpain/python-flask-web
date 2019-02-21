import os
import uuid

from flask import (
    render_template,
    Blueprint,
    request,
    session,
    redirect,
    url_for,
)

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models.user import User
from routes import (
    current_user,
    salt_password,
    new_csrf_token,
    # csrf_tokens,
    r,
)

main = Blueprint('index', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return render_template('index.html')
    else:
        return redirect(url_for('.profile'))


@main.route('/loginout')
def loginout():
    session.clear()
    # return render_template('index.html')
    return redirect(url_for('.index'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form['u']
    u = User.one(username=username)
    if u is not None and u.password == salt_password(form['p']):
        session['id'] = u.id
        session.permanent = True
        # return render_template('profile.html', user=u)
        return redirect(url_for('.profile'))
    else:
        return '用户名不存在或者密码错误'


@main.route('/register')
def register():
    return render_template('register.html')


@main.route('/registersuccess')
def registersuccess():
    return render_template('registersuccess.html')


@main.route('/registeruser', methods=['POST'])
def registeruser():
    form = request.form
    username = form['u']
    password = form['p']
    saltpassword = salt_password(password)
    email = form['e']
    u = User.one(username=username)
    if u is None:
        User.register(username=username, password=saltpassword, email=email)
        user = User.one(username=username)
        session['id'] = user.id
        session.permanent = True
        # return render_template('registersuccess.html')
        return redirect(url_for('.registersuccess'))
    else:
        return '用户名已经存在'


@main.route('/profile')
def profile():
    u = current_user()
    token = new_csrf_token()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u, token=token)


@main.route('/avatar_add', methods=['POST'])
def avatar_add():
    u = current_user()
    token = request.args['token']
    # if token in csrf_tokens and csrf_tokens[token] == u.id:
    if r.exists(token) and int(r.get(token).decode()) == u.id:
        file: FileStorage = request.files['avatar']
        suffix = file.filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        path = os.path.join('static/images', filename)
        file.save(path)
        User.update(u.id, image='/static/images/{}'.format(filename))
        # return render_template('profile.html', user=u)
        r.delete(token)
        return redirect(url_for('.profile'))
    else:
        return 'CSRF攻击'


@main.route('/signature', methods=['POST'])
def signature():
    u = current_user()
    form = request.form
    signature = form['signature']
    # 防止csrf攻击，加入token
    token = request.args['token']
    # if token in csrf_tokens and csrf_tokens[token] == u.id:
    if r.exists(token) and int(r.get(token).decode()) == u.id:
        User.update(u.id, signature=signature)
        r.delete(token)
        return redirect(url_for('.profile'))
    else:
        return 'CSRF攻击'
    # User.update(u.id, signature=signature)
    # return redirect(url_for('.profile'))


@main.route('/changepassword', methods=['POST'])
def changepassword():
    form = request.form
    old_password = form['old_p']
    password = salt_password(form['p'])
    u = current_user()
    if salt_password(old_password) == u.password:
        User.update(u.id, password=password)
        return '修改成功'
    else:
        return '原密码错误'