#!/usr/bin/python3

import sys

from redis import Redis
from rq import Connection, Queue, Worker
from browser import Browser


def get_screenshot(host=None, port=None, path=None, client=None, secret=None, db_path=None):
    """
        Take a screenshot for given path
    """
    Browser.get('http://{}:{}/favicon.ico'.format(host, port))

    Browser.add_cookie({
        'name': 'secret',
        'value': secret,
        'domain': '{}:{}'.format(host, port),
        'path': '/'
    })

    Browser.get('http://{}:{}{}?client={}&db={}'.format(host, port, path, client, db_path))
    img = Browser.get_screenshot_as_base64()

    return '<img alt="Embedded Image" src="data:image/png;base64,{}"/>'.format(img)


def main():
    """ Main
    """
    with Connection(connection=Redis()):
        qs = map(Queue, sys.argv[1:]) or [Queue()]

        worker = Worker(qs)
        worker.work()


if __name__ == "__main__":

    main()
