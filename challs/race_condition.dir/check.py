import subprocess
import random, string


def random_string(size):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def run_cmd(cmd_list):
	child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
	streamdata = child.communicate()[0]
	ret = child.returncode
	return streamdata.decode(), ret


# return true if the challenge is usable
# AKA if he tests passes
def check(binary, randomize):
	streamdata, return_code = run_cmd([binary, "login", randomize, randomize])
	if return_code != 0 or "You are logged in. And congratz ! Here is the secret : " + randomize + "\n" not in streamdata:
		print("Output is wrong when the admin try to log in. The output of your code is : " + streamdata + "\nAnd it should contain : \"You are logged in. And congratz ! Here is the secret : " + randomize + "\"")
		return False
	user = random_string(20)
	password = random_string(20)
	streamdata_reg, return_code_reg = run_cmd([binary, "register", user, password])
	if return_code_reg != 0 or "You are registered !\n" not in streamdata_reg :
		print("Output is wrong when a regular user try to register. The output of your code is : " + streamdata + "\nAnd it should contain : \"You are registered !\"")
		return False
	streamdata_log, return_code_log = run_cmd([binary, "login", user, password])
	if return_code_log != 0 or "You are logged in. But sorry you are not allowed to see the secret.\n"  not in streamdata_log:
		print("Output is wrong when a regular user try to log in. The output of your code is : " + streamdata + "\nAnd it should contain : \"You are logged in. But sorry you are not allowed to see the secret.\"")
		return False

	streamdata_fake_log, return_code_fake_log = run_cmd([binary, "login", "reallyrandom", "reallyrandom"])
	if return_code_fake_log != 0 or "We failed to log you in :/\n" != streamdata_fake_log:
		print("Output is wrong when a user fail to log in. The output of your code is : " + streamdata + "\nAnd it should contain : \"We failed to log you in :/\"")
		return False

	streamdata, ret = run_cmd([binary])
	if ret != 0 or "Please send me an 'action' (register or login) with your credentials (login, then password)\n" not in streamdata:
		print("Output of `./youcode_compiled` should be :\n\"Please send me an 'action' (register or login) with your credentials (login, then password)\"\n\nBut the output is :\n\"" + streamdata + "\"")
		return False

	return True
