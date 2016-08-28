# CTF Pédagogique

Ce repo permettra à ceux qui souhaitent apprendre la sécurité informatique de se lancer facilement.

First things first :

    git clone https://github.com/HugoDelval/ctf_pedagogique

## Configure Bower :

Install nodejs && npm && bower :

    apt-get update && apt-get upgrade
    apt-get install nodejs
    ln -s /usr/bin/nodejs /usr/bin/node # on some distribs you have to do that
    apt-get install npm

Pulling the nedeed files will be done by a script when needed. If you have to do it manually run:
`npm install bower && bower install`
    
## Installation :
first, be sure that you have go installed :

    sudo apt-get install golang

Then run the script *init.sh* :

    cd ctf_pedagogique
    sudo ./init.sh
    
Please consider changing your umask to 0027 for more privacy :
    
    sudo vim /etc/login.defs
Change :

    #     UMASK 022
To :

    #     UMASK 027

Also add this line to */etc/pam.d/common-session* (if it's not already there) :

    session optional pam_umask.so

You are now good to go(lang :p) !

    sudo -u ctf_interne ./run.sh
