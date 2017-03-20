#!/usr/bin/python3

import os
import sqlite3


def init(path, randomize, file_challenge_name=None):

    init_db(path, file_challenge_name)
    init_secret(path, randomize)


def init_db(path, file_challenge_name):

    db = os.path.join(os.path.sep, "tmp", "stored_xss.db")

    if file_challenge_name:  # Means correction context
        db = os.path.join(path, "stored_xss.db")
        file_challenge_path = os.path.join(path, file_challenge_name)
        with open(file_challenge_path, "r") as chall:
            file_chall_content = chall.read()
            new_file_chall_content = file_chall_content.replace("/tmp/stored_xss.db", db)
        with open(file_challenge_path, "w") as chall:
            chall.write(new_file_chall_content)

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS comments")
    conn.commit()
    cur.execute("""CREATE TABLE comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                comment TEXT NOT NULL)""")
    conn.commit()

    cur.execute(
        "INSERT INTO comments(author, comment) VALUES(?, ?)",
        ('admin', 'Not funny comment, please.')
    )
    conn.commit()
    conn.close()

    os.system('chown stored_xss:stored_xss ' + db)
    os.system('chmod 640 ' + db)


def init_secret(path, randomize):

    with open(os.path.join(path, 'secret'), "w") as secret:
        secret.write(randomize)
