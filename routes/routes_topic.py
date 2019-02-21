from flask import (
    render_template,
    Blueprint,
    request,
    session,
    redirect,
    url_for,
)

from models.user import User
from models.topic import Topic
from models.reply import Reply
from routes import (
    current_user,
    new_csrf_token,
    # csrf_tokens,
)

main = Blueprint('topic_club', __name__)


@main.route('/topic')
def topic():
    u = current_user()
    all_topics = Topic.all_topic()
    if u is None:
        return render_template('index.html')
    else:
        return render_template('topic_index.html', u=u, all_topics=all_topics)


@main.route('/detail/<int:id>')
def detail(id):
    t = Topic.get(id)
    return render_template("topic_detail.html", topic=t)


@main.route('/topic/add')
def topic_add():
    return render_template("topic_add.html")


@main.route('/topic/add_topic', methods=["POST"])
def topic_addtopic():
    form = request.form
    title = form['title']
    u = current_user()
    Topic.add_topic(form, user_id=u.id)
    m = Topic.one(title=title)
    return redirect(url_for('.detail', id=m.id))


@main.route('/reply/add_reply', methods=["POST"])
def reply_add():
    form = request.form
    topic_id = form['topic_id']
    u = current_user()
    Reply.reply_add(form, topic_id, user_id=u.id)
    return redirect(url_for('.detail', id=topic_id))
