#!/usr/bin/python3

import sys

from redis import Redis
from rq import Connection, Queue, Worker
from browser import Browser


def get_screenshot(host=None, port=None, path=None, client=None, secret=None):
    """
        Take a screenshot for given path
    """
    Browser.get('http://{}:{}/favicon.ico'.format(host, port))

    for cookie in ('secret', 'client'):
        Browser.add_cookie({
            'name': cookie,
            'value': locals()[cookie],
            'domain': '{}:{}'.format(host, port),
            'path': '/'
        })
    Browser.get('http://{}:{}{}'.format(host, port, path))
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
