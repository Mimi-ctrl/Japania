from app import app
from flask import render_template, request, redirect
import decks
import stats
import users

@app.route("/")
def index():
    return render_template("front_page.html")
# , decks=decks.get_all_decks()

@app.route("/hiragana_and_katakana")
def hiragana_and_katakana():
    return render_template("hiraganakatakana.html")

@app.route("/words")
def words():
    return render_template("words.html")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 15:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-15 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        status = request.form["status"]

        if password1 == "" or password2 == "":
            return render_template("error.html", message="Salasana puuttuu")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if status not in ("1","2"):
            return render_template("error.html", message="Tuntematon status")
        if not users.register(username, password1, status):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        return redirect("/")

@app.route("/statistic")
def show_stats():
    users.require_role(2)

    data = stats.get_full_stats(users.user_id())
    return render_template("statistics.html", data=data)

@app.route("/deck")
def deck():
    return render_template("deck.html")

@app.route("/new_deck")
def new_deck():
    return render_template("new_deck.html")

@app.route("/play")
def play():
    return render_template("play.html")

@app.route("/play/result")
def result():
    return render_template("result.html")

@app.route("/remove")
def remove():
    return render_template("remove.html")

