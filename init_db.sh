#!/bin/bash

ENDPOINT="http://localhost:8080/v1.0"


######### REGISTER USERS ############
curl $ENDPOINT/user/register -d '{"nick":"test","password":"test1"}'
token=`curl $ENDPOINT/user/login -d '{"nick":"test","password":"test1"}' | python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj)'`

curl $ENDPOINT/user/register -d '{"nick":"test1","password":"test1"}'
token1=`curl $ENDPOINT/user/login -d '{"nick":"test1","password":"test1"}' | python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj)'`

curl $ENDPOINT/user/register -d '{"nick":"test2","password":"test1"}'
token2=`curl $ENDPOINT/user/login -d '{"nick":"test2","password":"test1"}' | python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj)'`

curl $ENDPOINT/user/register -d '{"nick":"test3","password":"test1"}'
token3=`curl $ENDPOINT/user/login -d '{"nick":"test3","password":"test1"}' | python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj)'`

curl $ENDPOINT/user/register -d '{"nick":"test4","password":"test1"}'
token4=`curl $ENDPOINT/user/login -d '{"nick":"test4","password":"test1"}' | python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj)'`

curl $ENDPOINT/user/register -d '{"nick":"test5","password":"test1"}'
token5=`curl $ENDPOINT/user/login -d '{"nick":"test5","password":"test1"}' | python3 -c 'import json,sys;obj=json.load(sys.stdin);print(obj)'`
######### END REGISTER USERS ############


######### VALIDATE CHALLENGES ##########
curl $ENDPOINT/challenge/injection_conf/validate -d '{"secret":"thesecret"}' -H "X-CTF-AUTH: $token"
# curl $ENDPOINT/challenge/.../validate -d '{"secret":"test"}' -H "X-CTF-AUTH: $token"
# curl $ENDPOINT/challenge/.../validate -d '{"secret":"test"}' -H "X-CTF-AUTH: $token"

curl $ENDPOINT/challenge/injection_conf/validate -d '{"secret":"thesecret"}' -H "X-CTF-AUTH: $token1"
# curl $ENDPOINT/challenge/.../validate -d '{"secret":"test"}' -H "X-CTF-AUTH: $token1"

# curl $ENDPOINT/challenge/injection_conf/validate -d '{"secret":"TheSup3rS3cr37P@550RDThatn0OneknowsAbout"}' -H "X-CTF-AUTH: $token2"
# curl $ENDPOINT/challenge/.../validate -d '{"secret":"test"}' -H "X-CTF-AUTH: $token2"

# curl $ENDPOINT/challenge/injection_conf/validate -d '{"secret":"TheSup3rS3cr37P@550RDThatn0OneknowsAbout"}' -H "X-CTF-AUTH: $token3"

######### lALIDATE CHALLENGES ##########

