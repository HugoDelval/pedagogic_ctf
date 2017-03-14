#!/usr/bin/python3

import random
import string

from time import sleep

from bs4 import BeautifulSoup
from redis import Redis
from rq import Queue

selenium_queue = Queue(
    connection=Redis(),
    name='selenium'
)

HOST = 'my-site.com'
PORT = 8888
DB_REQUEST_PATH = '/internal/debug/get-comments'


def victim_browse(rand, secret):
    """
        Fake a browser navigation
    """
    job = selenium_queue.enqueue(
        'worker.get_screenshot',
        host=HOST,
        port=PORT,
        path=DB_REQUEST_PATH,
        client=rand,
        secret=secret
    )

    while job.status == 'queued':
        sleep(0.5)

    return job.result


if __name__ == '__main__':

    with open('secret') as f:
        secret = f.read().strip()

    rand = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    victim_response = victim_browse(rand, secret)
    victim_soup = BeautifulSoup(victim_response, "html.parser")

    with open('/tmp/api.log', 'r') as log:
        server_logs = log.readlines()

    server_logs = '<br>'.join([l.strip() for l in server_logs if rand in l or '* Running' in l])
    server_logs = server_logs.replace('http://{}'.format(HOST), 'http://evil.com')

    response = "<h2>Victim browser's screenshot</h2><br>{}<h2>Server logs</h2><pre>{}</pre>"
    response = response.format(victim_soup.prettify(), server_logs)
    print(response)
