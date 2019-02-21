import uuid

from flask import session
import redis

from models.user import User

# csrf_tokens = dict()
r = redis.StrictRedis(host='localhost', port=6379, db=0)


def current_user():
    uid = session.get('id', '')
    u = User.one(id=uid)
    return u


def salt_password(s, salt='$!@><?>HUI&DWQa`'):
    import hashlib
    hash1 = hashlib.sha256()
    hash2 = hashlib.sha256()
    hash1.update(bytes(s, encoding='utf-8'))
    hash2.update(bytes(hash1.hexdigest() + salt, encoding='utf-8'))
    return hash2.hexdigest()


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    # csrf_tokens[token] = u.id
    r.set(token, u.id, ex=3600)
    return token