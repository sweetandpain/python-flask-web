from flask import (
    render_template,
    Blueprint,
    request,
    session,
    redirect,
    url_for,
)

from models.user import User
from models.news import News
from routes import (
    current_user,
    new_csrf_token,
    # csrf_tokens,
)

main = Blueprint('allnews', __name__)


@main.route('/news')
def news():
    u = current_user()
    if u is None:
        return render_template('index.html')
    else:
        all_news = News.all_news()
        return render_template('news.html', all_news=all_news)