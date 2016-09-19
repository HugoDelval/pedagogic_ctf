import os
import random, string

def init(path, randomize):
	with open(os.path.join(path, 'secret'), "w") as secret:
		secret.write('FILTER_VALIDATE_EMAIL_FAILED_'.join(random.choice(string.ascii_letters + string.digits) for _ in range(3)))

if __name__ == "__main__":
	try:
		init("/srv/ctf_go/challs/php_exec.dir/")
	except Exception as e:
		print(e)
