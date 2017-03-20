#!/usr/bin/python3

import os
import sqlite3


def init(path, randomize, file_challenge_name=None):

    init_db(path, file_challenge_name, randomize)
    init_secret(path, randomize)


def init_db(path, file_challenge_name, randomize):

    db = os.path.join(os.path.sep, "tmp", "idor.db")

    if file_challenge_name:
        db = os.path.join(path, "broken_idor.db")
        file_challenge_path = os.path.join(path, file_challenge_name)
        with open(file_challenge_path, "r") as chall:
            file_chall_content = chall.read()
            new_file_chall_content = file_chall_content.replace("/tmp/idor.db", db)
        with open(file_challenge_path, "w") as chall:
            chall.write(new_file_chall_content)

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS accounts")
    conn.commit()
    cur.execute("""CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                token TEXT NOT NULL UNIQUE,
                balance INT NOT NULL DEFAULT 100,
                description TEXT NOT NULL DEFAULT '')""")
    conn.commit()

    token = 'JqcY6oUYCiVtvyfyN7r6z461hjhG!r7SzfnndZDYvuzicSmAyaVvr6RFlZZhEorS'
    cur.execute(
        "INSERT INTO accounts(username, token, balance, description) VALUES(?, ?, ?, ?)",
        ('586b652384404', token, 1337, 'The secret is {}'.format(randomize))
    )
    conn.commit()
    conn.close()

    os.system('chown idor:idor ' + db)
    os.system('chmod 640 ' + db)


def init_secret(path, randomize):

    with open(os.path.join(path, 'secret'), "w") as secret:
        secret.write(randomize)
