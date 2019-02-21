from flask import (
    render_template,
    Blueprint,
    request,
    session,
    redirect,
    url_for,
)

from models.user import User

from routes import (
    current_user,
    new_csrf_token,
    # csrf_tokens,
)

main = Blueprint('alltodo', __name__)


@main.route('/todo')
def todo_index():
    return render_template('todo.html')