#!/bin/bash

echo "Starting Selenium workers.."

cd /srv/ctf_go/challs/selenium
for i in {1..2}
do
    nohup python3 worker.py selenium &
done
