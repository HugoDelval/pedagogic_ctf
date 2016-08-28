#!/bin/bash

useradd ctf_interne
chattr -i -R /srv/ctf_go/challs/
rm -rf /srv/ctf_go && mkdir /srv/ctf_go
cp . -R /srv/ctf_go
rm -rf /srv/writable && mkdir /srv/writable && chmod 733 /srv/writable -R
cp /srv/ctf_go/src/ctf/utils/config.json.example /srv/ctf_go/src/ctf/utils/config.json
chown ctf_interne /srv/ctf_go -R
chmod o-rwx /srv/ctf_go -R

# Init challenges
userdel injection_conf
echo "thesecret" > /srv/ctf_go/challs/injection_conf.dir/secret
(cd /srv/ctf_go/ && ./load_challenges.py injection_conf)

echo
echo "Check src/ctf/utils/config.json !"


