import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    result = db.session.execute("SELECT password, id, status FROM users WHERE username=:name", {"name":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_username"] = username
    session["user_status"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_status"]

def register(username, password, status):
    y = generate_password_hash(password)
    try: 
        db.session.execute("""INSERT INTO users (username, password, status) VALUES (:username, :password, :status)""", {"username":username, "password":y, "status":status})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def require_role(status):
     if status > session.get("user_status", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
