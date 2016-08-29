#!/bin/bash

user=`whoami`
if [ ${user} != 'ctf_interne' ] ; then
    echo "please launch using : "
    echo "    sudo -u ctf_interne ./run.sh"
    exit
fi

cd /srv/ctf_go
export GOPATH=`pwd`
export PATH=$PATH:${GOROOT}/bin:${GOPATH}/bin
echo "Building.."
go build ctf/main
echo "Built"
echo "Launching app!"
./main
