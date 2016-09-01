#!/usr/bin/python3

import sqlite3, os

def clean():
	os.system('rm -rf /srv/writable/* && rm -rf /tmp/*')
	db_race_cond = "/srv/ctf_go/challs/race_condition.dir/race_condition.db"
	conn = sqlite3.connect(db_race_cond)
	cur = conn.cursor()
	cur.execute("DROP TABLE IF EXISTS users")
	cur.execute("DROP TABLE IF EXISTS forbidden_ids")
	conn.commit()
	cur.execute("""CREATE TABLE users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		login TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL)""")

	cur.execute("""CREATE TABLE forbidden_ids (
		user_id INTEGER NOT NULL UNIQUE)""")
	conn.commit()
	conn.close() 


if __name__ == "__main__":
	try:
		clean()
	except Exception as e:
		print(e)
