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

