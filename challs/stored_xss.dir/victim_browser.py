#!/usr/bin/python3

import sys

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
        client=ctf_user_email,
        secret=secret,
        db_path=None
    )

    while job.status == 'queued':
        sleep(0.5)

    return job.result


if __name__ == '__main__':

    ctf_user_email = sys.argv[1]

    with open('secret') as f:
        secret = f.read().strip()

    victim_response = victim_browse(ctf_user_email, secret)
    victim_soup = BeautifulSoup(victim_response, "html.parser")

    with open('/tmp/api.log', 'r') as log:
        srv_logs = log.readlines()

    srv_logs = '<br>'.join([l.strip() for l in srv_logs if ctf_user_email in l or '* Running' in l])
    srv_logs = srv_logs.replace('http://{}'.format(HOST), 'http://evil.com')

    response = "<h2>Victim browser's screenshot</h2><br>{}<h2>Server logs</h2><pre>{}</pre>"
    response = response.format(victim_soup.prettify(), srv_logs)
    print(response)
