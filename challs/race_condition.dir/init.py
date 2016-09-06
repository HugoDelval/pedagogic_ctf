import os

def init(path, randomize, file_challenge_name=None):
	db_race_cond = os.path.join(os.path.sep, "tmp", "race_condition.db")
	if file_challenge_name:
		db_race_cond = os.path.join(path, "race_condition.db")
		file_challenge_path = os.path.join(path, file_challenge_name)
		with open(file_challenge_path, "r+") as chall:
			file_chall_content = chall.read()
			new_file_chall_content = file_chall_content.replace("/tmp/race_condition.db", db_race_cond)
			chall.write(new_file_chall_content)
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
	os.system('chown race_condition:race_condition ' + db_race_cond)
	os.system('chmod 640 ' + db_race_cond)
	with open(os.path.join(path, 'secret'), "w") as secret:
		secret.write(randomize)
