#!/bin/bash

cd /srv/ctf_go
su ctf_interne
export GOPATH=`pwd`
export PATH=$PATH:${GOROOT}/bin:${GOPATH}/bin
go get ctf/main
go build ctf/main
echo "build done"
./main
