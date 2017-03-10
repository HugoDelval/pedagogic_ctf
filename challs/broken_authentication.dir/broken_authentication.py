#!/usr/bin/python3

import sqlite3
import sys

from base64 import b64encode
from hashlib import sha1

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

    if not username:
        print("Missing username")
        sys.exit(0)

    return username, token, endpoint


def generate_user_token(username):
    """
        Generates an API token for given username
    """
    return sha1(b64encode(bytes(username, "utf-8"))).hexdigest()


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
        if request.path == '/get-token':
            return

        try:
            token = request.environ['HTTP_X_API_TOKEN']
        except (KeyError, IndexError, TypeError):
            raise BadRequest('Missing or invalid token')

        g.cursor.execute("SELECT username FROM users WHERE token=?", (token,))
        user = g.cursor.fetchone()
        if not user:
            raise Unauthorized("Invalid X-Api-Token")

        g.user_token_mapping = user[0]  # Store username in the request context

    @app.route('/me')
    def me():
        """
            Returns username based on api token value
        """
        return "Your token match the user '{}'".format(g.user_token_mapping)

    @app.route('/get-token')
    def get_token():
        """
            Create or update token for current user
        """
        if g.username == 'admin':
            raise Forbidden('You are not allowed to request token for user admin')

        token = generate_user_token(g.username)
        g.cursor.execute(
            "INSERT OR REPLACE INTO users(username, token) VALUES(?, ?)",
            (g.username, token)
        )
        return "Your API token is {}".format(token)

    @app.route('/get-secret')
    def get_secret():
        """
            Return secret page
        """
        if g.user_token_mapping != 'admin':  # Fetched from db in get_user_from_token() line #47
            raise Forbidden('You are not allowed to request /get-secret')

        with open('secret') as secret:
            return "You are logged in. And congratz ! Here is the secret : {}".format(
                secret.read()
            )

    return app


APP = create_app()
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
        conn = sqlite3.connect('/tmp/broken_authentication.db', isolation_level=None)
        cursor = conn.cursor()
        g.cursor = cursor
        g.username = username
    except:
        print('Error while connecting to db.')
        sys.exit(1)

    if not endpoint:
        endpoint = '/get-token'

    # Make request
    response = tester.get(
        endpoint,
        headers={'X-API-TOKEN': token},
    )

    conn.commit()
    conn.close()
    print(response.get_data().decode('unicode_escape'))
