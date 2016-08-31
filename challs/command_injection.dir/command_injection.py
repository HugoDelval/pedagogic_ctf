#!/usr/bin/python3
import sys, os
import re
import random, string

## check params
if len(sys.argv) != 2 or not sys.argv[1]:
    print("Please send me a directory path so I can launch my configuration script !")
    sys.exit(0)
directory = sys.argv[1]
regex_dir = r"(/tmp/|/srv/writable/)[a-zA-Z0-9_-]+"
regex_dir_compiled = re.compile(regex_dir)
if not directory or not regex_dir_compiled.match(directory):
    print("Error, directory param not valid.")
    sys.exit(0)
if os.path.isdir(directory):
    print("Directory already exists.")
    sys.exit(0)
## end check params

## write configuration file
configuration_file_name = "/srv/writable/"
configuration_file_name += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
configuration_file_name += "_config.sh"
with open(configuration_file_name, "w") as fh:
    fh.write("DATE=`date`\n")
    fh.write("DIRECTORY=" + directory + "\n")
## end write configuration file

## launch application based on the config file
command = ". " + configuration_file_name + " && "
command += 'mkdir "${DIRECTORY}" && '
command += 'echo ${DATE} > "${DIRECTORY}/folder_configured"'
os.system(command)
## end launch application based on the config file

if os.path.isdir(directory):
    print("Directory configured.")
else:
    print("Failed to configure directory.")
