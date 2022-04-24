from db import db

def get_deck_stats(deck_id, user_id):
    return db.session.execute("""SELECT COUNT(*), COALESCE(SUM(a.result),0) FROM answers a, cards c WHERE c.deck_id=:deck_id AND a.user_id=:user_id AND a.card_id=c.id""", {"deck_id":deck_id, "user_id":user_id}).fetchone()

#def get_full_stats(user_id):