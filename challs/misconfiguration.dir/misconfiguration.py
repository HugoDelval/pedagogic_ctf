#!/usr/bin/python3

import sqlite3
import sys

from flask import Flask, g, request
from werkzeug.exceptions import (BadRequest, Forbidden,
                                 Unauthorized)


def get_params():
    """
        Check script params
    """
    if len(sys.argv) != 4:
        print("Missing parameters")
        sys.exit(0)

    username = sys.argv[1]
    token = sys.argv[2]
    endpoint = sys.argv[3]

    return username, token, endpoint


def create_app():
    """
        Initialize Flask application
    """
    app = Flask(__name__)

    @app.before_request
    def get_user_from_token():
        """
            Get token from HTTP header
        """

        try:
            token = request.environ['HTTP_X_API_TOKEN']
        except (KeyError, IndexError, TypeError):
            if APP.config['DEBUG']:
                g.cursor.execute("SELECT username FROM users")
                rows = g.cursor.fetchall()
                username = ""
                for row in rows:
                    username = row[0] + "\n" + username
                raise BadRequest("DEBUG: username list: {}".format(username))
            raise BadRequest('Missing or invalid token')

        g.cursor.execute("SELECT username FROM users WHERE token=?", (token,))
        user = g.cursor.fetchone()
        if not user:
            if APP.config['DEBUG']:
                g.cursor.execute("SELECT token FROM users")
                rows = g.cursor.fetchall()
                token = ""
                for row in rows:
                    token = row[0] + "\n" + token
                raise BadRequest("DEBUG: token list: {}".format(token))
            raise Unauthorized("Invalid X-Api-Token")

        g.user_token_mapping = user[0]  # Store username in the request context

    @app.route('/me')
    def me():
        """
            Returns username based on api token value
        """
        return "Your token match the user '{}'".format(g.user_token_mapping)

    @app.route('/get-secret')
    def get_secret():
        """
            Return secret page
        """
        if g.user_token_mapping != 'admin':
            raise Forbidden('You are not allowed to request /get-secret')

        with open('secret') as secret:
            return "You are logged in. And congratz ! Here is the secret : {}".format(
                secret.read()
            )

    return app


APP = create_app()
# please remove this setting in production.
APP.config['DEBUG'] = True
APP.config['TESTING'] = True


if __name__ == '__main__':

    # Parse params
    username, token, endpoint = get_params()

    # Init app and db cursor
    try:
        tester = APP.test_client()
        ctx = APP.test_request_context()
        ctx.push()
        conn = sqlite3.connect('/tmp/misconfiguration.db', isolation_level=None)
        cursor = conn.cursor()
        g.cursor = cursor
        g.username = username
    except:
        print('Error while connecting to db.')
        sys.exit(1)

    if not endpoint:
        endpoint = '/me'

    if token:
        headers = {'X-API-TOKEN': token}
    else:
        headers = ""

    # Make request
    response = tester.get(
        endpoint,
        headers=headers,
    )

    conn.close()
    print(response.get_data().decode('unicode_escape'))
