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

If you need to make changes, help yourself, then launch:

	docker build . -t hugodelval/pedagogic-ctf

To kill the running app press Ctrl-C then :
	
	docker ps
	docker kill <CONTAINER ID>

## How does it work?

The user can do 2 things :

- exploit programs (and learn the vulnerability)
- correct challenges (learn how to fix the vulnerability)

### Exploit

The server launch the program with the user input as *stdin*. The user goal is to find the **secret** of the program (something that should not be visible if there are no vulnerabilities).

If the user finds the secret, he can submit it to the server, which will check the secret validity and add points to the user.

### Correct

The user can then correct the program:

1. the user send the corrected code
2. the server copies the code in a new temporary directory and create a temporary user (+chmod / chown...)
4. the server executes (with the new temp user's permissions) the init script of the program (init.py) this initialise the program, create secrets, databases and so on...
5. the server executes the user code (with the new temp user's permissions) using several tests that check if the program still works (challs/*/check.py)
6. the server executes the user code (with the new temp user's permissions) using several tests that check if the program is no more exploitable (challs/*/exploit.py)
7. the server delete the temporary folder and user
8. the server gives points to the users if the program still works and is no more exploitable
