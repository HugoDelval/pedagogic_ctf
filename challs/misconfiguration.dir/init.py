#!/usr/bin/python3

import os
import sqlite3
from base64 import b64encode
from random import randrange
from hashlib import sha1


def init(path, randomize, file_challenge_name=None):

    init_db(path, file_challenge_name)
    init_secret(path, randomize)


def generate_user_token():
    """
    Generates an API token for given username
    """
    return sha1(b64encode(bytes(randrange(1, 99999)))).hexdigest()


def init_db(path, file_challenge_name):

    db = os.path.join(os.path.sep, "tmp", "misconfiguration.db")

    if file_challenge_name:
        db = os.path.join(path, "misconfiguration.db")
        file_challenge_path = os.path.join(path, file_challenge_name)
        with open(file_challenge_path, "r") as chall:
            file_chall_content = chall.read()
            new_file_chall_content = file_chall_content.replace("/tmp/misconfiguration.db", db)
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

    cur.execute("INSERT INTO users(username, token) VALUES(?, ?)", ('debug-e9bc7d25d163', 'e9bc7d25d16348f9c5f6b9251c270c0da39aff8b'))
    for user in "root", "debug", "user", "admin", "whynot", 'debug-true':
        trand = generate_user_token()
        cur.execute(
            "INSERT INTO users(username, token) VALUES(?, ?)",
            (user, trand)
            )
    conn.commit()
    conn.close()

    os.system('chown misconfiguration:misconfiguration ' + db)
    os.system('chmod 640 ' + db)


def init_secret(path, randomize):

    with open(os.path.join(path, 'secret'), "w") as secret:
        secret.write(randomize)
