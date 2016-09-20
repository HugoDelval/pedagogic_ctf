FROM debian:stable

RUN apt-get update
RUN apt-get install --fix-missing
RUN apt-get install -y git nodejs golang libauthen-passphrase-perl libdbi-perl  libdbd-sqlite3-perl python3-bcrypt sudo npm nginx
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower
RUN git clone https://github.com/HugoDelval/pedagogic_ctf
RUN cd pedagogic_ctf/frontend-angular && \
    bower install --allow-root 
RUN cd pedagogic_ctf && \
    ./init.sh 

CMD service nginx restart && \
    sudo -u ctf_interne pedagogic_ctf/run.sh 
