from random import randint
from db import db

def new_deck(deck_name, words, teacher_id):
    deck_id = db.session.execute("""INSERT INTO decks (teacher_id, deck_name, visible) VALUES (:teacher_id, :deck_name, 1) RETURNING id""", {"teacher_id":teacher_id, "deck_name":deck_name}).fetchone()[0]

    for pair in words.split("\n"):
        parts = pair.strip().split(";")
        if len(parts) != 2:
            continue
        db.session.execute("""INSERT INTO cards (deck_id, word, word2) VALUES (:deck_id, :word, :word2)""", {"deck_id":deck_id, "word":parts[0], "word2":parts[1]})

    db.session.commit()
    return deck_id

def get_deck_info(deck_id):
    return db.session.execute("""SELECT d.deck_name, u.username FROM decks d, users u WHERE d.id=:deck_id AND d.teacher_id=u.id""", {"deck_id":deck_id}).fetchone()[0]

def get_deck_size(deck_id):
    return db.session.execute("SELECT COUNT(*) FROM cards WHERE deck_id = :deck_id",{"deck_id":deck_id}).fetchone()[0]

def get_reviews(deck_id, user_id, grades, comment):
    db.session.execute("""INSERT INTO reviews (deck_id, user_id, grades, comment) VALUES (:deck_id, :user_id, :grades, :comment)""",
        {"deck_id":deck_id, "user_id":user_id,"grades":grades, "comment":comment})
    db.session.commit()

#def get_all_decks():

#def get_my_decks(user_id):

#def add_deck(name, words, creator_id):

#def remove_deck(deck_id, user_id):

#def get_random_card(deck_id):

#def get_card_words(card_id):

#def send_answer(card_id, answer, user_id):

#def add_review(deck_id, user_id, stars, comment):

