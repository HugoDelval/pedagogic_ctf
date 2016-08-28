#!/bin/bash

useradd ctf_interne
mkdir /srv/writable
chmod 733 /srv/writable
./load_challenges.py injection_conf
echo "don't forget src/ctf/utils/config.json.example"
echo "don't forget to change the wrapper too !"
