#!/bin/bash

useradd ctf_interne
rm -rf /srv/ctf_go && mkdir /srv/ctf_go
cp . -R /srv/ctf_go
rm -rf /srv/writable && mkdir /srv/writable && chmod 733 /srv/writable
cp /srv/ctf_go/src/ctf/utils/config.json.example /srv/ctf_go/src/ctf/utils/config.json
chown ctf_interne /src/ctf_go -R
chmod o-rwx /src/ctf_go -R
/srv/ctf_go/load_challenges.py injection_conf
echo "Check src/ctf/utils/config.json !"

