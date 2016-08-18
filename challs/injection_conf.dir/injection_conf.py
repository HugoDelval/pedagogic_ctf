#!/usr/bin/python3
import sys, os
import re
import random, string

## check params
if len(sys.argv) != 2:
    print("Error, directory param not valid.")
    sys.exit(1)
directory = sys.argv[1]
regex_dir = r"[a-zA-Z0-9_\/-]+"
regex_dir_compiled = re.compile(regex_dir)
if not directory or not regex_dir_compiled.match(directory):
    print("Error, directory param not valid.")
    sys.exit(1)
if os.path.isdir(directory):
    print("Directory already exists.")
    sys.exit(1)
## end check params

## write configuration file
file_name = "/srv/writable/";
file_name += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
file_name += "_config.sh"
with open(file_name, "w") as fh:
	fh.write("/bin/mkdir " + directory + "\n")
	fh.write("/bin/touch " + directory + "/folder_configured\n")
	fh.write("exit 0\n")
## end write configuration file

## call configuration
os.system("/bin/sh " + file_name)
## end call configuration

if os.path.isdir(directory):
    print("Directory configured.")
else:
    print("Failed to configure directory.")
