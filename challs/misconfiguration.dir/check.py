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
            'params': ['', '', '/get-secret'],
            'response': 'missing or invalid token',
            'message': 'User check seems broken. Expecting : Missing or invalid token\n\n Your code output \n\n{}',
        },
        {
            'params': ['test', 'test', '/get-secret'],
            'response': 'invalid x-api-token',
            'message': 'Token check seems broken. Expecting :Invalid X-Api-Token \n\n Your code output \n\n{}',
        },
        {
            'params': ['debug-e9bc7d25d163', 'e9bc7d25d16348f9c5f6b9251c270c0da39aff8b', '/aze'],
            'response': 'not found',
            'message': 'Calling invalid endpoint does not return "not found". Your code output \n\n{}',
        },
        {
            'params': ['debug-e9bc7d25d163', 'e9bc7d25d16348f9c5f6b9251c270c0da39aff8b', '/me'],
            'response': 'debug-e9bc7d25d163',
            'message': 'Calling /me does not return my user. Your code output \n\n{}',
        },
        {
            'params': ['debug-e9bc7d25d163', 'e9bc7d25d16348f9c5f6b9251c270c0da39aff8b', '/get-secret'],
            'response': 'you are not allowed to request',
            'message': '/get-secret endpoint seems unavailable or broken. Your code output \n\n{}',
        },
    ]

    for _check in checks:

        _check['params'].insert(0, binary)
        streamdata, return_code = run_cmd(_check['params'])
        if return_code != 0 or _check['response'] not in streamdata.lower():
            print(_check['message'].format(streamdata))
            return False

    return True
