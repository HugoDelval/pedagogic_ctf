#!/usr/bin/python3

import os
from random import choice
from string import ascii_lowercase


def init(path, randomize, file_challenge_name=None):

    init_secret(path, randomize)
    init_key(path, randomize)


def init_secret(path, randomize):

    with open(os.path.join(path, 'secret'), "w") as secret:
        secret.write(''.join(choice(ascii_lowercase) for i in range(16)))


def init_key(path, randomize):

    with open(os.path.join(path, 'key'), "w") as secret:
        secret.write(''.join(choice(ascii_lowercase) for i in range(16)))
