FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install --fix-missing -y nginx
RUN apt-get install --fix-missing -y git
RUN apt-get install --fix-missing -y nodejs
RUN apt-get install --fix-missing -y golang
RUN apt-get install --fix-missing -y libauthen-passphrase-perl
RUN apt-get install --fix-missing -y libmojolicious-perl
RUN apt-get install --fix-missing -y libdigest-sha-perl
RUN apt-get install --fix-missing -y libdbi-perl
RUN apt-get install --fix-missing -y libdbd-sqlite3-perl
RUN apt-get install --fix-missing -y python3-pip
RUN apt-get install --fix-missing -y python3-bcrypt
RUN apt-get install --fix-missing -y sudo
RUN apt-get install --fix-missing -y npm
RUN apt-get install --fix-missing -y php
RUN apt-get install --fix-missing -y dnsutils
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower
ADD . /pedagogic_ctf
RUN cd /pedagogic_ctf/frontend-angular && bower install --allow-root
RUN cd /pedagogic_ctf && ./init.sh

CMD service nginx restart && sudo -u ctf_interne /pedagogic_ctf/run.sh
