#!/usr/bin/python3

import sqlite3
import sys

from flask import Flask, g
from werkzeug.exceptions import NotFound


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

    @app.route('/accounts/new')
    def create_account():
        """
            Get or create an account for user
        """
        default_balance = 100
        g.cursor.execute(
            "INSERT OR REPLACE INTO accounts(username, balance) VALUES(?,?)",
            (g.username, default_balance)
        )
        account_id = g.cursor.execute(
            "SELECT id from accounts WHERE username=?",
            (g.username,)
        )
        account_id = g.cursor.fetchone()[0]

        response = "Your account {} has been successfully created.\nYou can view details here /accounts/{}/details"
        return response.format(account_id, account_id)

    @app.route('/accounts/<account_id>/details')
    def get_account_details(account_id):
        """
            Return user account details
        """
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
    if len(sys.argv) != 3:
        print("Missing parameters")
        sys.exit(0)

    username = sys.argv[1]
    endpoint = sys.argv[2]

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
    )

    conn.commit()
    conn.close()
    print(response.get_data().decode('unicode_escape'))
