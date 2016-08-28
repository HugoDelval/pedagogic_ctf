#!/bin/bash

user=`whoami`
if [ ${user} != 'ctf_interne' ] ; then
    echo "please launch using : "
    echo "    sudo -u ctf_interne ./run.sh"
    exit
fi

the_umask=`umask`
if [ ${the_umask} != '0027' ] ; then
    echo "Warning ! Your umask is : ${the_umask} "
    echo "It should be 0027."
    read -p "Are you sure to continue !? (y/n)" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo "Good choice !"
        exit
    fi
fi

cd /srv/ctf_go
export GOPATH=`pwd`
export PATH=$PATH:${GOROOT}/bin:${GOPATH}/bin
go get ctf/main
go build ctf/main
echo "build done"
./main
