# Pedagogic CTF

This project is meant to ease the learning of software security.

You will be able to exploit simple programs with the source code in front of you. Then you will be ask to fix the code and submit it, the server will test your code (both looking for security vulnerabilities and testing functionalities). Then you will have your result, explaining where you failed.

## Contributions

Please feel free to contribute ! See in the */challs* directory for instructions of how to add challenges. Feel free to contact me on github or at: **hugodelval [at] gmail [dot] com**

## Run with docker

### Installation

Installation varies a lot depending on your system. Please refer to the official documentation (kept up to date !) here : https://docs.docker.com/engine/installation/linux/debian (for example).

### Running !

Easy :)

	docker run -t -p 8081:80 hugodelval/pedagogic-ctf

Then open your browser here: http://localhost:8081

To kill the running app press Ctrl-C then :
	
	docker ps
	docker kill <CONTAINER ID>

