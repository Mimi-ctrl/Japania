from app import app
from flask import render_template, request, redirect
import decks
import stats
import users

@app.route("/")
def index():
    return render_template("front_page.html")

@app.route("/hiragana_and_katakana")
def page1():
    return render_template("hiraganakatakana.html")

@app.route("/words")
def page2():
    return render_template("words.html")

@app.route("/login")
def page3():
    return render_template("login.html")

@app.route("/login/register")
def page4():
    return render_template("register.html")

@app.route("/deck")
def page5():
    return render_template("deck.html")

@app.route("/new_deck")
def page6():
    return render_template("new_deck.html")

@app.route("/play")
def page7():
    return render_template("play.html")

@app.route("/result")
def page8():
    return render_template("result.html")