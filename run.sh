#!/bin/bash

if [ whoami != 'ctf_interne' ] ; then
    echo "please launch using : "
    echo "    sudo -u ctf_interne ./run.sh"
    exit
fi

cd /srv/ctf_go
export GOPATH=`pwd`
export PATH=$PATH:${GOROOT}/bin:${GOPATH}/bin
go get ctf/main
go build ctf/main
echo "build done"
./main
