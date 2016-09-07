import os
import subprocess
import random, string


def run_cmd(cmd_list):
	child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
	streamdata = child.communicate()[0]
	ret = child.returncode
	return streamdata.decode(), ret


# return true if the challenge is usable
# AKA if he tests passes
def check(binary, randomize):
	directory = "/srv/writable/inject_conf_" + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
	folder_configured_path = os.path.join(directory, "folder_configured")
	streamdata, ret = run_cmd([binary, directory])
	if ret != 0 or not os.path.isdir(directory) or not os.path.isfile(folder_configured_path):
		print("Your code should have created a directory with an init file \"folder_configured in it\". But it appears it failed to do it. Here is the output of your code : " + streamdata)
		return False

	directory = "/home/whatever"
	streamdata, ret = run_cmd([binary, directory])
	if ret != 0 or streamdata != "Error, directory param not valid.\n":
		print("Output is wrong. The output of your code is : " + streamdata + "\nAnd it should be : \"Error, directory param not valid.\"")
		return False

	directory = "/srv/writable/&ls"
	streamdata, ret = run_cmd([binary, directory])
	if ret != 0 or streamdata != "Error, directory param not valid.\n":
		print("Output is wrong. The output of your code is : " + streamdata + "\nAnd it should be : \"Error, directory param not valid.\"")
		return False

	streamdata, ret = run_cmd([binary])
	if ret != 0 or streamdata != "Please send me a directory path so I can launch my configuration script !\n":
		print("Output of `./youcode_compiled` should be :\n\"Please send me a directory path so I can launch my configuration script !\"\n\nBut the output is :\n\"" + streamdata + "\"")
		return False

	return True
