from flask import (
    session,
    redirect,
    url_for,
    render_template,
    request,
    Blueprint
)

from routes import current_user

main = Blueprint('main', __name__)


@main.route('/socketchat')
def index():
    u = current_user()
    if u is None:
        return '先登录'
    else:
        return render_template('chat.html')
