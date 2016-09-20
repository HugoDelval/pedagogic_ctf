# Pedagogic CTF

This project is meant to ease the learning of software security.

First thing first :

	git clone https://github.com/HugoDelval/pedagogic_ctf

## Run with docker

### Installation

Installation varies a lot depending on your system. Please refer to the official documentation (kept up to date !) here : https://docs.docker.com/engine/installation/linux/debian (for example).

### Running !

Every commands is executed with root privileges.

	cd pedagogic_ctf
	docker build -t pedagogic_ctf .
	docker run -t --rm -p 8081:80 pedagogic_ctf &

To kill the running app :

	docker ps
	docker kill <docker_id>
