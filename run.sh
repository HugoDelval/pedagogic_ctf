#!/bin/bash

cd /srv/ctf_go
export GOPATH=`pwd`
export PATH=$PATH:${GOROOT}/bin:${GOPATH}/bin
sudo -u ctf_interne go get ctf/main
sudo -u ctf_interne go build ctf/main
echo "build done"
sudo -u ctf_interne ./main
