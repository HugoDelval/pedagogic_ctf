#!/bin/bash

userdel ctf_interne
groupdel ctf_interne
useradd ctf_interne
mkdir /home/ctf_interne && chown ctf_interne:ctf_interne /home/ctf_interne -R
rm -rf /srv/ctf_go && mkdir /srv/ctf_go

export GOPATH=`pwd`
export PATH=$PATH:${GOROOT}/bin:${GOPATH}/bin
echo "Fetching golang requirements.."
go get ctf/main

cp . -R /srv/ctf_go
rm -rf /srv/writable && mkdir /srv/writable && chmod 733 /srv/writable
chmod 733 /tmp
cp /srv/ctf_go/src/ctf/utils/config.json.example /srv/ctf_go/src/ctf/utils/config.json
touch /srv/ctf_go/database.db
chown ctf_interne /srv/ctf_go -R
chmod o-rwx /srv/ctf_go -R
chmod o+rx /srv/ctf_go/
chmod o+rx /srv/ctf_go/challs/
chown :www-data /srv/ctf_go/frontend-angular/ -R

# Build app that check if user has well corrected the script
gcc /srv/ctf_go/check_challenge_corrected.c -o /srv/ctf_go/check_challenge_corrected
chown root:ctf_interne /srv/ctf_go/check_challenge_corrected
chmod 4750 /srv/ctf_go/check_challenge_corrected
chown root:root /srv/ctf_go/check_challenge_corrected.py
chmod 500 /srv/ctf_go/check_challenge_corrected.py

# Init challenges
userdel injection_conf
printf "thesecret" > /srv/ctf_go/challs/injection_conf.dir/secret
(cd /srv/ctf_go/ && ./load_challenges.py injection_conf)
userdel command_injection
printf "thesecret" > /srv/ctf_go/challs/command_injection.dir/secret
(cd /srv/ctf_go/ && ./load_challenges.py command_injection)
userdel race_condition
printf "thesecret" > /srv/ctf_go/challs/race_condition.dir/secret
(cd /srv/ctf_go/ && ./load_challenges.py race_condition)

chown ctf_interne /srv/ctf_go/challenges.json

# configure nginx
cp /srv/ctf_go/nginx.conf /etc/nginx/sites-available/pedagogictf
ln -s /etc/nginx/sites-available/pedagogictf /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
service nginx reload

echo
echo "Check src/ctf/utils/config.json !"
