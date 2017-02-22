FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install --fix-missing -y git && \
    apt-get install --fix-missing -y nodejs && \
    apt-get install --fix-missing -y golang && \
    apt-get install --fix-missing -y libauthen-passphrase-perl && \
    apt-get install --fix-missing -y libdbi-perl && \
    apt-get install --fix-missing -y libdbd-sqlite3-perl && \
    apt-get install --fix-missing -y python3-bcrypt && \
    apt-get install --fix-missing -y sudo && \
    apt-get install --fix-missing -y npm && \
    apt-get install --fix-missing -y nginx
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower
ADD . /pedagogic_ctf
RUN cd /pedagogic_ctf/frontend-angular && bower install --allow-root
RUN cd /pedagogic_ctf && ./init.sh

CMD service nginx restart && sudo -u ctf_interne /pedagogic_ctf/run.sh
