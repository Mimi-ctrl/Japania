import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    x = db.session.execute("SELECT password, id, status FROM users WHERE username=:username", {"username":username}).fetchone()
    if not x:
        return False
    if not check_password_hash(x[0], password):
        return False
    session["user_id"] = x[1]
    session["user_username"] = username
    session["user_role"] = x[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_status"]

def register(username, password, status):
    y = generate_password_hash(password)
    try: 
        sql = """INSERT INTO users (username, password, status)
                VALUES (:username, :password, :status)"""
        db.session.execute(sql, {"username":username, "password":y, "status":status})
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
