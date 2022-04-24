from random import randint
from db import db

def get_deck_info(deck_id):
    return db.session.execute("""SELECT d.deck_name, u.username FROM decks d, users u WHERE d.id=:deck_id AND d.teacher_id=u.id""", {"deck_id":deck_id}).fetchone()[0]

def get_deck_size(deck_id):
    return db.session.execute("SELECT COUNT(*) FROM cards WHERE deck_id = :deck_id",{"deck_id":deck_id}).fetchone()[0]

def get_reviews(deck_id):
    return db.session.execute("""SELECT u.username, r.grade, r.comment FROM reviews r, users u WHERE r.user_id=u.id AND r.deck_id=:deck_id ORDER BY r.id""",{"deck_id": deck_id}).fetchall()
#korjaa uder user:iksi
def get_all_decks():
    return db.session.execute("SELECT id, deck_name FROM decks WHERE visible=1").fetchall()

def get_my_decks(user_id):
    return db.session.execute("""SELECT id deck_name FROM decks WHERE teacher_id=:user_id AND visible=1""", {"user_id":user_id}).fetchall()

def add_deck(deck_name, words, teacher_id):
    deck = db.session.execute("""INSERT INTO decks(teacher_id, deck_name, visible) VALUES(:teacher_id, :deck_name, 1) RETURNING id""", {"teacher_id":teacher_id, "deck_name":deck_name}).fetchone()[0]
    for i in words.split("\n"):
        y = i.strip().split(";")
        if len(y) != 2:
            continue
        db.session.execute("""INSERT INTO cards(deck_id, word, word2) VALUES (:deck_id, :word, :word2)""", {"deck_id":deck, "word":y[0], "word2":y[1]})
    db.session.commit()
    return deck

def remove_deck(deck_id, user_id):
    db.session.execute("UPDATE decks SET visible=0 WHERE id:=id AND teacher_id=:user_id",{"id":deck_id, "user_id":user_id})
    db.session.commit()

#def get_random_card(deck_id):

#def get_card_words(card_id):

#def send_answer(card_id, answer, user_id):

def add_review(deck_id, user_id, grades, comment):
    db.session.execute("""INSERT INTO reviews(deck_id, user_id, grades, comment)  VALUES (:deck_id, :user_id, :stars, :comment)""", {"deck_id":deck_id, "user_id":user_id,"grades":grades, "comment":comment})
    db.session.commit()
