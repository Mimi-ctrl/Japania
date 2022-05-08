from db import db

def get_deck_stats(deck_id, user_id):
    return db.session.execute("""SELECT COUNT(*), COALESCE(SUM(a.result),0) FROM answers a, 
                    cards c WHERE c.deck_id=:deck_id AND a.user_id=:user_id AND a.card_id=c.id""", {"deck_id":deck_id, "user_id":user_id}).fetchone()

def get_full_stats(user_id):
    decks = db.session.execute("""SELECT id, deck_name FROM decks WHERE teacher_id=:user_id AND visible=1""", {"user_id": user_id}).fetchall()
    data = []
    for deck in decks:
        data.append((deck[1], db.session.execute("""SELECT u.username, COUNT(*), COALESCE(SUM(a.result),0) 
                    FROM answers a, cards c, users u WHERE c.deck_id=:deck_id AND a.card_id=c.id AND u.id=a.user_id
                    GROUP BY u.id, u.username ORDER BY u.username""", {"deck_id": deck[0]}).fetchall()))
    return data