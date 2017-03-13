#!/usr/bin/python3

import random
import sqlite3
import string
import sys

from flask import Flask, g, request
from werkzeug.exceptions import (BadRequest,
                                 NotFound, Unauthorized)


def generate_token():
    """
        Generate a pseudo-random token
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))


def get_user_account_details(account_id):
    """
        Get account details for user
    """
    g.cursor.execute("SELECT id, balance, description FROM accounts WHERE id=?", (account_id,))
    account = g.cursor.fetchone()
    if not account:
        return

    return "Account ID: {},\nBalance: {},\nDescription: {}".format(
        account[0],
        account[1],
        account[2],
    )


def create_app():
    """
        Initialize Flask application
    """
    app = Flask(__name__)

    @app.before_request
    def verify_token():
        """
            Get token from HTTP header
        """
        if request.path == '/accounts/new':
            return

        try:
            token = request.environ['HTTP_X_API_TOKEN']
        except (KeyError, IndexError, TypeError):
            raise BadRequest('Missing or invalid token')

        g.cursor.execute(
            "SELECT username FROM accounts WHERE token=? and username=?",
            (token, g.username)
        )
        user = g.cursor.fetchone()
        if not user:
            raise Unauthorized("Invalid X-Api-Token")

    @app.route('/accounts/new')
    def create_account():
        """
            Get or create an account for user
        """
        token = generate_token()
        default_balance = 100
        g.cursor.execute(
            "INSERT OR REPLACE INTO accounts(username, token, balance) VALUES(?,?,?)",
            (g.username, token, default_balance)
        )
        account_id = g.cursor.execute(
            "SELECT id from accounts WHERE username=?",
            (g.username,)
        )
        account_id = g.cursor.fetchone()[0]

        response = """Your account {} has been successfully created.
        Your associated token is {}
        You can view account details here /accounts/{}/details"""
        return response.format(account_id, token, account_id)

    @app.route('/accounts/<account_id>/details')
    def get_account_details(account_id):
        """
            Return user account details
        """
        # Username and token already verified in function verify_token

        account_details = get_user_account_details(
            account_id=account_id,
        )
        if not account_details:
            raise NotFound('Account not found')

        return account_details

    return app

APP = create_app()
APP.config['DEBUG'] = True
APP.config['TESTING'] = True


if __name__ == '__main__':

    # Parse params
    if len(sys.argv) != 4:
        print("Missing parameters")
        sys.exit(0)

    username = sys.argv[1]
    token = sys.argv[2]
    endpoint = sys.argv[3]

    if not username:
        print("Missing username")
        sys.exit(0)

    # Init app and db cursor
    try:
        tester = APP.test_client()
        ctx = APP.test_request_context()
        ctx.push()
        conn = sqlite3.connect('/tmp/idor.db', isolation_level=None)
        cursor = conn.cursor()
        g.cursor = cursor
        g.username = username
    except:
        print('Error while connecting to db.')
        sys.exit(1)

    if not endpoint:
        endpoint = '/accounts/new'

    # Make request
    response = tester.get(
        endpoint,
        headers={'X-API-TOKEN': token},
    )

    conn.commit()
    conn.close()
    print(response.get_data().decode('unicode_escape'))
