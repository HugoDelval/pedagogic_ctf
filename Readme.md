# CTF Pédagogique

Ce repo permettra à ceux qui souhaitent apprendre la sécurité informatique de se lancer facilement.

First things first :

    git clone https://github.com/HugoDelval/ctf_pedagogique

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

    npm install bower
Pulling the nedeed files will be done by a script when needed. If, one day, you have to do it manually run:
`bower install` or `bower install [package]`
    
## Installation :
first, be sure that you have go installed :

    sudo apt-get install golang

Then run the script *init.sh* :

    cd ctf_pedagogique
    sudo ./init.sh
    
You are now good to go(lang :p) !

    sudo -u ctf_interne ./run.sh
