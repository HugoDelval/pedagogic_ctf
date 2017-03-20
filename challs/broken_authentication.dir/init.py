#!/usr/bin/python3

import os
import sqlite3


def init(path, randomize, file_challenge_name=None):

    init_db(path, file_challenge_name)
    init_secret(path, randomize)


def init_db(path, file_challenge_name):

    db = os.path.join(os.path.sep, "tmp", "broken_authentication.db")

    if file_challenge_name:
        db = os.path.join(path, "broken_authentication.db")
        file_challenge_path = os.path.join(path, file_challenge_name)
        with open(file_challenge_path, "r") as chall:
            file_chall_content = chall.read()
            new_file_chall_content = file_chall_content.replace("/tmp/broken_authentication.db", db)
        with open(file_challenge_path, "w") as chall:
            chall.write(new_file_chall_content)

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    cur.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                token TEXT NOT NULL)""")
    conn.commit()

    cur.execute(
        "INSERT INTO users(username, token) VALUES(?, ?)",
        ('admin', 'f5c828ff122cd8d0509051584236cceb28c78bfa')
    )
    conn.commit()

    cur.execute(
        "INSERT INTO users(username, token) VALUES(?, ?)",
        ('debug-e9bc7d25d163', 'e9bc7d25d16348f9c5f6b9251c270c0da39aff8b')
    )

    conn.commit()
    conn.close()

    os.system('chown broken_authentication:broken_authentication ' + db)
    os.system('chmod 640 ' + db)


def init_secret(path, randomize):

    with open(os.path.join(path, 'secret'), "w") as secret:
        secret.write(randomize)
