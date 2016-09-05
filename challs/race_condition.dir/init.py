import os
import random, string

def init(path, randomize):
	db_race_cond = os.path.join(path, "race_condition.db")
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
	cur.execute("INSERT INTO users(login, password) VALUES(?, ?)", [randomize, randomize])
	conn.close()
	with open(os.path.join(path, 'secret'), "w") as secret:
		secret.write(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30)))

if __name__ == "__main__":
	try:
		init("/srv/ctf_go/challs/race_condition.dir/")
	except Exception as e:
		print(e)
