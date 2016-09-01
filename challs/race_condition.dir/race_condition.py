#!/usr/bin/python3
import sqlite3, sys
import bcrypt, time

## Usage :
# ex : ./race_condition.py register admin password123
# ex : ./race_condition.py login admin password123

## check params
if len(sys.argv) != 4 or not sys.argv[1] or not sys.argv[2] or not sys.argv[3]:
    print("Please send me an 'action' (register or login) with your credentials (login, then password)")
    sys.exit(0)
action = sys.argv[1]
login = sys.argv[2]
passwd = sys.argv[3]
hashed_passwd = str(bcrypt.hashpw(sys.argv[3], bcrypt.gensalt()))
## end check params

try:
	conn = sqlite3.connect('race_condition.db', isolation_level=None)
	cur = conn.cursor()
except:
	print('Error connecting to db.')
	sys.exit(0)


def get_user_id():
	cur.execute("SELECT id, password FROM users WHERE login=?", [login])
	user = cur.fetchone()
	if user:
		if bcrypt.hashpw(passwd, user[1]) == user[1]:
			return user[0]
	return -1


def do_register():
	cur.execute("INSERT INTO users(login, password) VALUES(?, ?)", [login, hashed_passwd])
	user_id = get_user_id()
	cur.execute("INSERT INTO forbidden_ids(user_id) VALUES(?)", [user_id])


def do_login():
	user_id = get_user_id()
	if user_id < 0:
		return "We failed to log you in :/"
	cur.execute("SELECT count(*) FROM forbidden_ids WHERE user_id=?", [user_id])
	if cur.fetchone()[0] > 0:
		return "You are logged in. But sorry you are not allowed to see the secret."
	with open('secret') as s:
		return "You are logged in. And congratz ! Here is the secret : " + s.read()


if action == 'register':
	try:
		do_register()
		print("You are registered !")
	except Exception as e:
		print("An error occurred : " + str(e))
elif action == 'login':
	try:
		print(do_login())
	except Exception as e:
		print("An error occurred : " + str(e))
else:
	print("Error, action param not valid.")

conn.close()