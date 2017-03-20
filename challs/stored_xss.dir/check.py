
import os
import requests
import subprocess

from shutil import copyfile


def run_cmd(cmd_list):
    child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    ret = child.returncode
    return streamdata.decode(), ret


def check(binary, randomize):
    """
        Check if the corrected source code is still usable
    """
    # Copy victim_browser script to correction context
    current_path = os.path.dirname(os.path.realpath(__file__))
    victim_browser_file = '{}/victim_browser.py'.format(current_path)
    copyfile('/srv/ctf_go/challs/stored_xss.dir/victim_browser.py', victim_browser_file)

    user = 'debug'

    out, return_code = run_cmd((binary, user, 'test'))
    if return_code != 0:
        print("Invalid execution : {}".format(out))
        return False

    if not all(k in out.lower() for k in ('running', 'base64', 'img', '8888')):
        print("Unable to parse victim_browser.py output {}".format(out))
        return False

    temp_db = os.path.join(current_path, "stored_xss.db")  # Specify the dedicated correction db
    path = "http://my-site.com:8888/internal/debug/get-comments?client={}&db={}".format(
        user,
        temp_db
    )

    response = requests.get(path).text

    if '<tr><td>{}</td><td>test</td></tr>'.format(user) not in response:
        print("POST comments seems broken, unable to find 'test' in {}".format(response))
        return False

    return True
