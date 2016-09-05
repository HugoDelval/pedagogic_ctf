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
WEB_USER = "ctf_interne"
with open(os.path.join(CHALLS_DIR, 'wrapper.c')) as wrapper_handler:
	WRAPPER = wrapper_handler.read()
if not WRAPPER:
	print({"error": "Cannot get C wrapper."})
	sys.exit(1)


def check_args():
	if len(sys.argv) < 2:
		print({"error": "Error: excepting at least 1 argument :\n" + __file__ + " chall_id1 [chall_id2 [chall_id3 [..]]]"})
		sys.exit(1)

	arguments = sys.argv[1:]
	regex_string = r"^[\w-]{4,30}$"
	re_safe_string = re.compile(regex_string)
	for arg in arguments:
		# are the args safe ?
		if not re_safe_string.search(arg):
			print({"error": "An argument does not match the regex : " + regex_string})
			sys.exit(1)
		
		# is folder exists ?
		folder = os.path.join(CHALLS_DIR, arg + ".dir")
		if not os.path.isdir(folder):
			print({"error": "Can't find a folder with the name :" + folder })
			sys.exit(1)

		chall_path = os.path.join(folder, arg)
		if not os.path.isfile(chall_path + ".json"):
			print({"error": "A challenge does not have is JSON description in " + folder})
			sys.exit(1)

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
				sys.exit(1)
			else:
				streamdata, return_code = run_cmd(['adduser', user, "challenge_group"])
				if return_code != 0:
					delete_users(users_added)
					print({"error": "A user cannot be added to challenge_group : " + user + "\n Here is the error : " + str(streamdata)})
					sys.exit(1)
				else:
					users_added.append(user)
	except Exception as e:
		delete_users(users_added)
		print({"error": "An error occured while creating users : " + str(e)})
		sys.exit(1)


def create_wrapper_and_change_perms(arguments):
	try:
		for user in arguments:
			# challs/chall.dir
			folder_name = user + ".dir"
			folder_path = os.path.join(CHALLS_DIR, folder_name)
			
			# create wrapper.c
			current_wrapper = WRAPPER.replace("CHALLENGE",
				os.path.join(os.path.sep, "srv", "ctf_go", "challs", folder_name, user + '.pl')
			)
			# we assume that there will always be a perl challenge, and base the wrapper on this file
			current_wrapper = current_wrapper.replace("THE_USER", user)
			current_wrapper_path = os.path.join(folder_path, "wrapper.c")
			with open(current_wrapper_path, "w") as wrapper_handler:
				wrapper_handler.write(current_wrapper)
			current_wrapper_bin_path = os.path.join(folder_path, "wrapper")
			streamdata, return_code = run_cmd(['gcc', "-o", current_wrapper_bin_path, current_wrapper_path])
			if return_code != 0:
				print({"error": "An error occured while compiling wrapper : " + str(streamdata)})
				sys.exit(1)

			# ch(mod/own/attr) challs/chall.dir/
			streamdata, return_code = run_cmd(['chown', user+":"+WEB_USER, folder_path, "-R"])
			if return_code != 0:
				print({"error": "An error occured while chowning : " + str(streamdata)})
				sys.exit(1)
			streamdata, return_code = run_cmd(['chown', "root:"+WEB_USER, current_wrapper_bin_path, "-R"])
			if return_code != 0:
				print({"error": "An error occured while chowning : " + str(streamdata)})
				sys.exit(1)
			streamdata, return_code = run_cmd(['chmod', "g+x,u+xs", current_wrapper_bin_path])
			if return_code != 0:
				print({"error": "An error occured while chmoding : " + str(streamdata)})
				sys.exit(1)
			streamdata, return_code = run_cmd(['chmod', "o-rwx", folder_path, "-R"])
			if return_code != 0:
				print({"error": "An error occured while chmoding : " + str(streamdata)})
				sys.exit(1)
			streamdata, return_code = run_cmd(['chattr', "+i", "-R", folder_path])
			if return_code != 0:
				print({"error": "An error occured while chattring : " + str(streamdata)})
				sys.exit(1)

			# add JSON description to global description
			try:
				with open("challenges.json") as challs_json_handler:
					challs_json = json.loads(challs_json_handler.read())
			except:
				challs_json = []
			chall_json_path = os.path.join(folder_path, user + '.json')
			try:
				with open(chall_json_path) as chall_json_handler:
					chall_json = json.loads(chall_json_handler.read())
			except:
				chall_json = None
			if not chall_json:
				print({"error": "An error occured while loading challenge's JSON description"})
				sys.exit(1)
			chall_json['challenge_id'] = user
			challs_json.append(chall_json)
			with open("challenges.json", "w") as challs_json_handler:
				challs_json_handler.write(json.dumps(challs_json))

	except Exception as e:
		print({"error": "An error occured while creating folders : " + str(e)})
		sys.exit(1)


if __name__ == "__main__":
	arguments = check_args()
	create_users(arguments)
	create_wrapper_and_change_perms(arguments)
