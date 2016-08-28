#!/bin/bash

useradd ctf_interne
mkdir /srv/ctf_go
cp . -R /srv/ctf_go
mkdir /srv/writable
chmod 733 /srv/writable
/srv/ctf_go/load_challenges.py injection_conf
cp /srv/ctf_go/src/ctf/utils/config.json.example /srv/cf_go/src/ctf/utils/config.json
echo "Check src/ctf/utils/config.json !"

