CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    status INTEGER
);

CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    deck_id INTEGER REFERENCES decks,
    word TEXT,
    word2 TEXT
);

CREATE TABLE decks (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES users,
    visible INTEGER,
    deck_name TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    card_id INTEGER REFERENCES decks,
    result INTEGER,
    time TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    uder_id INTEGER REFERENCES users,
    deck_id INTEGER REFERENCES decks,
    comment TEXT
);

