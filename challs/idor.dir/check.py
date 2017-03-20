import re
import subprocess


def run_cmd(cmd_list):
    child = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    out = child.communicate()[0]
    ret = child.returncode
    return out.decode(), ret


def check(binary, randomize):
    """
        Check if the corrected source code is still usable
    """
    debug_token = 'JqcY6oUYCiVtvyfyN7r6z461hjhG!r7SzfnndZDYvuzicSmAyaVvr6RFlZZhEorS'
    debug_username = '586b652384404'

    checks = [
        {
            'params': ['test', '', ''],
            'response': 'has been successfully created',
            'message': 'Account creation seems broken. Your code output \n\n{}',
        },
        {
            'params': ['test', '', '/accounts/new'],
            'response': 'has been successfully created',
            'message': 'Account creation seems broken. Your code output \n\n{}',
        },
        {
            'params': [debug_username, debug_token, '/aze'],
            'response': 'not found',
            'message': 'Calling invalid endpoint does not return "not found". Your code output \n\n{}',
        },
        {
            'params': [debug_username, debug_token, '/accounts/4564645646546545646/details'],
            'response': 'not found',
            'message': 'Calling invalid account id does not return "not found". Your code output \n\n{}',
        }
    ]

    for _check in checks:

        _check['params'].insert(0, binary)
        out, return_code = run_cmd(_check['params'])
        if return_code != 0 or _check['response'] not in out.lower():
            print(_check['message'].format(out))
            return False

    out, return_code = run_cmd((binary, 'test123', '', '/accounts/new'))
    for reg in (r'Your account .* has been successfully created', r'You can view account details here /accounts/.*/details'):
        if not re.search(reg, out, re.I):
            print('Account creation seems broken. Please do not change API output... Your code output \n\n{}'.format(out))
            return False

    out, return_code = run_cmd((binary, 'test123', '', '/accounts/new'))
    reg = r'Your account (.*) has been successfully created'
    search = re.search(reg, out, re.I)
    if not search:
        print('Unable to extract account id')
        return False

    account_id = search.group(1)

    reg = r'Your associated token is (.*)'
    search = re.search(reg, out, re.I)
    if not search:
        print('Unable to extract token')
        return False

    token = search.group(1)
    out, return_code = run_cmd((binary, 'test123', token, '/accounts/{}/details'.format(account_id)))
    for detail in ('account', 'balance', 'description'):
        if detail not in out.lower():
            print('Unable to parse account details. Please do not change API output... Your code output \n\n{}'.format(out))
            return False

    return True
