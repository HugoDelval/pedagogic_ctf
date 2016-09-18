# CTF Pédagogique

This project is meant to ease the learning of software security.

Note : every command in this tuto is executed with root privileges.

First thing first :

    git clone https://github.com/HugoDelval/pedagogic_ctf

## Configure Bower :

Install nodejs && npm && bower :

    apt-get update && apt-get upgrade
    apt-get install nodejs
If you can't do :

    npm -v
Consider doing a :
    
    apt-get install npm
    ln -s /usr/bin/nodejs /usr/bin/node # (on some distribs you have to do that)
Now you should be able to launch :

    npm -v
If not, please refer to the official documentation : https://docs.npmjs.com/getting-started/installing-node .
Finally run :

    npm install -g bower
    cd frontend_angular
    bower install --allow-root
   
## Installation :
first, be sure that you have go installed :

    sudo apt-get install golang
some modules :

    apt-get install libauthen-passphrase-perl
    apt-get install libdbi-perl
    apt-get install libdbd-sqlite3-perl
    apt-get install python3-bcrypt
    apt-get install sudo
    apt-get install nginx
    apt-get install dnsutils

Then run the script *init.sh* :

    cd pedagogic_ctf
    ./init.sh
    
You are now good to go(lang :p) !

    (cd /srv/ctf_go && sudo -u ctf_interne ./run.sh)



# TODO

--allow-root
nginx
add challenges
fichiers statiques en relatifs
lancer init avec le load_challenges.py
docker -> bdd
