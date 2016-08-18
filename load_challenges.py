#!/usr/bin/python3

"""
take in param the name of challenge to add in challs/
add the user + chmod/chown/chattr the chall files
"""

import sys, os
import re
import subprocess
import json

CHALLS_DIR = "challs"
LOCK_FILE = ".lock_challs"
WEB_USER = "ctf_interne"
EXTENSIONS = ['.pl', '.py'] 
with open(os.path.join(CHALLS_DIR, 'wrapper.c')) as wrapper_handler:
	WRAPPER = wrapper_handler.read()
if not WRAPPER:
	print({"error": "Cannot get C wrapper."})
	sys.exit(1)


def exit_fail():
	os.remove(LOCK_FILE)
	sys.exit(1)


def lock():
	### check if we are the only process adding users & co
	if os.path.isfile(LOCK_FILE):
		print({"error": "Another process is currently doing the same thing."})
		exit_fail()
	try:
		# does not prevent from race condition ! Just for the admin
		with open(LOCK_FILE, "w") as lock_file:
			pass
	except:
		print({"error": "Another process is currently doing the same thing."})
		exit_fail()


def check_args():
	if len(sys.argv) < 2:
		print({"error": "Error: excepting at least 1 argument :\n" + __file__ + " test.pl [test.py [test.go [..]]]"})
		exit_fail()

	arguments = sys.argv[1:]
	regex_string = r"^[\w-]{4,30}$"
	re_safe_string = re.compile(regex_string)
	for arg in arguments:
		# is the args safe ?
		if not re_safe_string.search(arg):
			print({"error": "An argument does not match the regex : " + regex_string})
			exit_fail()
		
		# is folder exists ?
		folder = os.path.join(CHALLS_DIR, arg + ".dir")
		if not os.path.isdir(folder):
			print({"error": "Can't find a folder with the name :" + new_folder })
			exit_fail()

		# 
		chall_path = os.path.join(folder, arg)
		for ext in EXTENSIONS:
			if not os.path.isfile(chall_path + ext):
				print({"error": "An argument appears to not be a file in " + folder})
				exit_fail()

		if not os.path.isfile(chall_path + ".json"):
			print({"error": "A challenge does not have is JSON description in " + folder})
			exit_fail()

	return arguments


def run_cmd(cmd_list):
	child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
	streamdata = child.communicate()[0]
	ret = child.returncode
	return streamdata, ret


def delete_users(users):
	for user in users:
		streamdata, return_code = run_cmd(['userdel', user])
		if return_code != 0:
			print({"error": "A user cannot be deleted : " + user + "\n Here is the error : " + streamdata})


def create_users(arguments):
	users_added = []
	try:
		for user in arguments:
			streamdata, return_code = run_cmd(['useradd', user])
			if return_code != 0:
				delete_users(users_added)
				print({"error": "A user cannot be added : " + user + "\n Here is the error : " + str(streamdata)})
				exit_fail()
			else:
				users_added.append(user)
	except Exception as e:
		delete_users(users_added)
		print({"error": "An error occured while creating users : " + str(e)})
		exit_fail()


def create_wrapper_and_change_perms(arguments):
	try:
		for user in arguments:
			# challs/chall.dir
			folder_name = user + ".dir"
			folder_path = os.path.join(CHALLS_DIR, folder_name)
			
			# create wrapper.c
			current_wrapper = WRAPPER.replace("CHALLENGE", os.path.join(folder_name, user + '.pl')) # we assume that there will always be a perl challenge, and base the wrapper on this file
			current_wrapper_path = os.path.join(folder_path, "wrapper.c")
			with open(current_wrapper_path, "w") as wrapper_handler:
				wrapper_handler.write(current_wrapper)
			current_wrapper_bin_path = os.path.join(folder_path, "wrapper")
			streamdata, return_code = run_cmd(['gcc', "-o", current_wrapper_bin_path, current_wrapper_path])
			if return_code != 0:
				print({"error": "An error occured while compiling wrapper : " + str(streamdata)})
				exit_fail()

			# ch(mod/own/attr) challs/chall.dir/
			streamdata, return_code = run_cmd(['chown', user+":"+WEB_USER, folder_path, "-R"])
			if return_code != 0:
				print({"error": "An error occured while chowning : " + str(streamdata)})
				exit_fail()
			streamdata, return_code = run_cmd(['chown', user+":"+user, os.path.join(folder_path, "secret")])
			if return_code != 0:
				print({"error": "An error occured while chowning : " + str(streamdata)})
				exit_fail()
			streamdata, return_code = run_cmd(['chmod', "g+x,u+xs", current_wrapper_bin_path])
			if return_code != 0:
				print({"error": "An error occured while chmoding : " + str(streamdata)})
				exit_fail()
			streamdata, return_code = run_cmd(['chmod', "o-rwx", folder_path, "-R"])
			if return_code != 0:
				print({"error": "An error occured while chmoding : " + str(streamdata)})
				exit_fail()
			streamdata, return_code = run_cmd(['chattr', "+i", "-R", folder_path])
			if return_code != 0:
				print({"error": "An error occured while chattring : " + str(streamdata)})
				exit_fail()

			# add JSON description to global description
			try:
				with open("challenges.json") as challs_json_handler:
					challs_json = json.loads(challs_json_handler.read())
			except:
				challs_json = {}
			chall_json_path = os.path.join(folder_path, user + '.json')
			try:
				with open(chall_json_path) as chall_json_handler:
					chall_json = json.loads(chall_json_handler.read())
			except:
				chall_json = None
			if not chall_json:
				print({"error": "An error occured while loading challenge's JSON description"})
				exit_fail()
			challs_json[user] = chall_json
			with open("challenges.json", "w") as challs_json_handler:
				challs_json_handler.write(json.dumps(challs_json))

	except Exception as e:
		print({"error": "An error occured while creating folders : " + str(e)})
		exit_fail()


if __name__ == "__main__":
	lock()
	arguments = check_args()
	create_users(arguments)
	create_wrapper_and_change_perms(arguments)
	os.remove(LOCK_FILE)
