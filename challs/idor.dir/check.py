import re
import subprocess


def run_cmd(cmd_list):
    child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    ret = child.returncode
    return streamdata.decode(), ret


def check(binary, randomize):
    """
        Check if the corrected source code is still usable
    """
    checks = [
        {
            'params': ['test', ''],
            'response': 'has been successfully created',
            'message': 'Account creation seems broken. Your code output \n\n{}',
        },
        {
            'params': ['test', '/accounts/new'],
            'response': 'has been successfully created',
            'message': 'Account creation seems broken. Your code output \n\n{}',
        },
        {
            'params': ['debug-e9bc7d25d163', '/aze'],
            'response': 'not found',
            'message': 'Calling invalid endpoint does not return "not found". Your code output \n\n{}',
        },
        {
            'params': ['debug-e9bc7d25d163', '/accounts/4564645646546545646/details'],
            'response': 'not found',
            'message': 'Calling invalid account id does not return "not found". Your code output \n\n{}',
        }
    ]

    for _check in checks:

        _check['params'].insert(0, binary)
        streamdata, return_code = run_cmd(_check['params'])
        if return_code != 0 or _check['response'] not in streamdata.lower():
            print(_check['message'].format(streamdata))
            return False

    streamdata, return_code = run_cmd((binary, 'test123', '/accounts/new'))
    for reg in (r'Your account .* has been successfully created', r'You can view details here /accounts/.*/details'):
        if not re.search(reg, streamdata, re.I):
            print('Account creation seems broken. Please do not change API output...')
            return False

    streamdata, return_code = run_cmd((binary, 'test123', '/accounts/new'))
    reg = r'Your account (.*) has been successfully created'
    search = re.search(reg, streamdata, re.I)
    if not search:
        print('Unable to extract account id.')
        return False

    account_id = search.group(1)
    streamdata, return_code = run_cmd((binary, 'test123', '/accounts/{}/details'.format(account_id)))
    for detail in ('account', 'balance', 'description'):
        if detail not in streamdata.lower():
            print('Unable to parse account details. Please do not change API output...')
            return False

    return True
