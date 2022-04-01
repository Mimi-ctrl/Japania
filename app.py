from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("front_page.html")

@app.route("/hiraganat_ja_katakanat")
def page1():
    return render_template("hiraganakatakana.html")

@app.route("/sanastoa")
def page2():
    return render_template("words.html")

@app.route("/kirjaudu_sisään")
def page3():
    return render_template("login.html")

@app.route("/kirjaudu_sisään/luo_tunnus")
def page4():
    return render_template("register.html")

@app.route("/pakka")
def page5():
    return render_template("deck.html")