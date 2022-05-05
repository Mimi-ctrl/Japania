from app import app
from flask import render_template, request, redirect
import decks
import stats
import users

@app.route("/")
def index():
    return render_template("front_page.html", decks=decks.get_all_decks())

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
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

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

@app.route("/new_deck", methods=["get", "post"]) 
def new_deck():
    users.require_role(2)
    if request.method == "GET":
        return render_template("new_deck.html")

    if request.method == "POST":
        users.check_csrf()

        deck_name = request.form["deck_name"]
        if len(deck_name) < 1 or len(deck_name) > 15:
            return render_template("error.html", message="Nimen pituuden tulee olla 1-15 merkkiä")

        words = request.form["words"]
        if len(words) > 20000:
            return render_template("error.html", message="Sanalista on liian pitkä")

        deck_id = decks.add_deck(deck_name, words, users.user_id())
        return redirect("/deck/"+str(deck_id))
        
@app.route("/deck/<int:deck_id>")
def deck(deck_id):
    info = decks.get_deck_info(deck_id)
    size = decks.get_deck_size(deck_id)
    total, correct = stats.get_deck_stats(deck_id, users.user_id())
    reviews = decks.get_reviews(deck_id)
    return render_template("deck.html", id=deck_id, deck_name=info, username=info, size=size, total=total, correct=correct, reviews=reviews)

@app.route("/play/<int:deck_id>")
def play(deck_id):
    users.require_role(1)
    return render_template("play.html", deck_id=deck_id, card_id=decks.get_random_card(deck_id)[0], question=decks.get_random_card(deck_id)[1])
  
@app.route("/result", methods=["post"])
def result():
    users.require_role(1)
    users.check_csrf()
    decks.send_answer(request.form["card_id"], request.form["answer"].strip(), users.user_id())
    words = decks.get_card_words(request.form["card_id"])
    return render_template("result.html", deck_id=request.form["deck_id"], question=words[0],
                           answer=request.form["answer"].strip(), correct=words[1])

@app.route("/remove", methods=["get", "post"])
def remove():
    users.require_role(2)
    if request.method == "GET":
        return render_template("remove.html", list=decks.get_my_decks(users.user_id()))
    if request.method == "POST":
        users.check_csrf()
        if "deck" in request.form:
            decks.remove_deck(request.form["deck"], users.user_id())
        return redirect("/")


@app.route("/statistic")
def show_stats():
    users.require_role(2)
    return render_template("stats.html", data=stats.get_full_stats(users.user_id()))

@app.route("/review", methods=["post"])
def review():
    users.require_role(1)
    users.check_csrf()
    if int(request.form["grade"]) < 1 or int(request.form["grade"]) > 5:
        return render_template("error.html", message="Virheellinen arvosana")
    if len(request.form["comment"]) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä")
    if request.form["comment"] == "":
        request.form["comment"] = "-"
    decks.add_review(request.form["deck_id"], users.user_id(), int(request.form["grade"]), request.form["comment"])
    return redirect("/deck/"+str(request.form["deck_id"]))