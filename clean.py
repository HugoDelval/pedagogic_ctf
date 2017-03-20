#!/usr/bin/python3

import os
import random, string
import importlib.machinery


def random_string(size):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def clean():
	os.system('rm -rf /srv/writable/* && rm -rf /tmp/*')
	root = os.path.join(os.path.sep, "srv", "ctf_go", "challs")
	for challenge_dir in [os.path.join(root, o) for o in os.listdir(root) if os.path.isdir(os.path.join(root, o))]:
		init = importlib.machinery.SourceFileLoader('init', os.path.join(challenge_dir, "init.py")).load_module()
		randomized = random_string(30)
		init.init(challenge_dir, randomized)

if __name__ == "__main__":
	try:
		clean()
	except Exception as e:
		print(e)
