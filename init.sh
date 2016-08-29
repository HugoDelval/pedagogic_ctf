#!/bin/bash

useradd ctf_interne
mkdir /home/ctf_interne && chown ctf_interne:ctf_interne /home/ctf_interne -R
chattr -i -R /srv/ctf_go/challs/
rm -rf /srv/ctf_go && mkdir /srv/ctf_go
cp . -R /srv/ctf_go
rm -rf /srv/writable && mkdir /srv/writable && chmod 733 /srv/writable -R
cp /srv/ctf_go/src/ctf/utils/config.json.example /srv/ctf_go/src/ctf/utils/config.json
touch /srv/ctf_go/database.db
chown ctf_interne /srv/ctf_go -R
chmod o-rwx /srv/ctf_go -R
chmod o+x /srv/ctf_go/
chmod o+x /srv/ctf_go/challs/


# Init challenges
userdel injection_conf
printf "thesecret" > /srv/ctf_go/challs/injection_conf.dir/secret
(cd /srv/ctf_go/ && ./load_challenges.py injection_conf)

chown ctf_interne /srv/ctf_go/challenges.json

echo
echo "Check src/ctf/utils/config.json !"
