FROM debian:stable

RUN apt-get update
RUN apt-get install -y git python  nodejs golang libauthen-passphrase-perl libdbi-perl libdbd-sqlite3-perl python3-bcrypt sudo
RUN apt-get -y install npm
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower
RUN git clone https://github.com/HugoDelval/ctf_pedagogique
RUN cd ctf_pedagogique/frontend-angular && \
    bower install --allow-root 
RUN cd ctf_pedagogique  && \
    ./init.sh 

CMD sudo -u ctf_interne ctf_pedagogique/run.sh 
