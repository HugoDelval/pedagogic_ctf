import sys
import subprocess

def run_cmd(cmd_list):
	child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
	streamdata = child.communicate()[0]
	ret = child.returncode
	return streamdata, ret


def clean_output(string_from_dig):
	array_from_dig = string_from_dig.split('\n')
	new_array = set()
	for line in array_from_dig:
		if line != "" and not line.startswith(';'):
			new_array.add(line)
	return new_array


# return true if the challenge is usable
# AKA if the tests passes
def check(randomize, binary):
	streamdata_ref, ret_ref = run_cmd(["/usr/bin/dig", "www.ovh.com"])
	streamdata_bin, ret_bin = run_cmd([binary, "www.ovh.com"])
	# should output the same thing
	if ret_bin != 0:
		print("Error executing `./youcode_compiled www.ovh.com`")
		print(streamdata_bin)
		sys.exit(1)
	streamdata_ref_set = clean_output(streamdata_ref)
	streamdata_bin_set = clean_output(streamdata_bin)
	if streamdata_ref_set != streamdata_bin_set:
		print("Output of `./youcode_compiled www.ovh.com` different from `/usr/bin/dig www.ovh.com`")
		print("\n\nYour code outputs : \n" + streamdata_bin + "\n\nAnd `dig` outputs : \n" + streamdata_bin)
		return False


	streamdata_ref, ret_ref = run_cmd(["/usr/bin/dig", "8.8.8.8"])
	streamdata_bin, ret_bin = run_cmd([binary, "8.8.8.8"])
	# should output the same thing
	if ret_bin != 0:
		print("Error executing `./youcode_compiled 8.8.8.8`")
		print(streamdata_bin)
		sys.exit(1)
	streamdata_ref_set = clean_output(streamdata_ref)
	streamdata_bin_set = clean_output(streamdata_bin)
	if streamdata_ref_set != streamdata_bin_set:
		print("Output of `./youcode_compiled 8.8.8.8` different from `/usr/bin/dig 8.8.8.8`")
		print("\n\nYour code outputs : \n" + streamdata_bin + "\n\nAnd `dig` outputs : \n" + streamdata_bin)
		return False

	streamdata, ret = run_cmd([binary, "test with w!erds charac|eres"])
	if ret != 0 or streamdata != "Error, server param not valid.\n":
		print("Output of `./youcode_compiled \"test with w!erds charac|eres\"` should be :\n\"Error, server param not valid.\"\n\nBut the output is :\n\"" + streamdata + "\"")
		return False

	streamdata, ret = run_cmd([binary])
	if ret != 0 or streamdata != "Please send me a server address so I can dig it ! (ex: 127.0.0.1 or www.ovh.com)\n":
		print("Output of `./youcode_compiled` should be :\n\"Please send me a server address so I can dig it ! (ex: 127.0.0.1 or www.ovh.com)\"\n\nBut the output is :\n\"" + streamdata + "\"")
		return False

	return True