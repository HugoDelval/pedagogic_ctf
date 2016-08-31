#!/usr/bin/python3
import sys, os
import re

## check params
if len(sys.argv) != 2 or not sys.argv[1]:
    print("Please send me a server address so I can dig it ! (ex: 127.0.0.1 or www.ovh.com)")
    sys.exit(0)
server = sys.argv[1]
server_regex = r"[!;&\|'\"`\${}><]"
server_regex_compiled = re.compile(server_regex)
if not server or server_regex_compiled.match(server):
    print("Error, server param not valid.")
    sys.exit(0)
## end check params

## launch dig
result_dig = os.popen("/usr/bin/dig " + server).read()
## end launch dig

print(result_dig)
