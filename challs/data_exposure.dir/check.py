import subprocess
import shutil
import os


def run_cmd(cmd_list):
    child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    ret = child.returncode
    return streamdata.decode(), ret


def check(binary, randomize):
    """
        Check if the corrected source code is still usable
    """

    current_path = os.path.dirname(os.path.realpath(__file__))
    shutil.copyfile('/srv/ctf_go/challs/data_exposure.dir/key', '{}/key'.format(current_path))
    os.system('chown root:data_exposure ' + '{}/key'.format(current_path))

    checks = [
        {
            'params': ['odtokjupfpenmtyo'],
            'response': 'here is the encrypted text',
            'message': 'Encryption API is broken. Expecting : here is the encrypted text\n\n Your code output \n\n{}',
        },
        {
            'params': [''],
            'response': 'here is the encrypted text',
            'message': 'Encryption API is broken. Without user input, return exemple found in secret.\n Expecting : here is the encrypted text\n\n Your code output \n\n{}',
        },
        {
            'params': ['tooshort'],
            'response': 'encryption problem!',
            'message': 'Encryption API is broken. Expecting : Encryption problem!\n\n Your code output \n\n{}',
        },
    ]

    for _check in checks:

        _check['params'].insert(0, binary)
        streamdata, return_code = run_cmd(_check['params'])
        if return_code != 0 or _check['response'] not in streamdata.lower():
            print(_check['message'].format(streamdata))
            return False

    return True
