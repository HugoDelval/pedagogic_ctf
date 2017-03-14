#!/usr/bin/python3

import logging

from logging.handlers import RotatingFileHandler

import sqlite3

from flask import Flask, request

HOST = '127.0.0.1'
PORT = 12345
NOT_LOGGED_PATH = (
    '/favicon.ico',
    '/internal/debug/get-comments',
)

CSS = """<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>"""


def create_app():
    """
        Initialize Flask application
    """
    app = Flask(__name__)

    @app.before_request
    def log_request():

        if request.path not in NOT_LOGGED_PATH:

            msg = "{} {} with cookies: {}".format(
                request.method,
                request.path,
                request.cookies
            )
            app.logger.warning(msg)

    @app.route('/internal/debug/get-comments')
    def get_comments():

        conn = sqlite3.connect('/tmp/stored_xss.db', isolation_level=None)
        cursor = conn.cursor()
        comments = cursor.execute("SELECT author, comment from comments")
        comments = cursor.fetchall()
        conn.close()

        rows = ''
        response = "{}<table><tr><th>Author</th><th>comment</th></tr>{}"
        for entry in comments:
            rows += '<tr><td>{}</td><td>{}</td></tr>'.format(
                entry[0],
                entry[1],
            )

        response = response.format(CSS, rows)
        response = response + "</table>"
        return response

    return app


def main():
    """
        Start internal API for selenium-based challenges
    """
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app = create_app()

    handler = RotatingFileHandler('/tmp/api.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)

    app.logger.addHandler(handler)
    app.logger.warning('* Running on http://{}:{}/ (Press CTRL+C to quit)'.format(HOST, PORT))
    app.run(host=HOST, port=PORT)


if __name__ == '__main__':

    main()
