#!/usr/bin/python3

import sqlite3
import subprocess
import sys

from flask import Flask, g


def create_app():
    """
        Initialize Flask application
    """
    app = Flask(__name__)

    @app.route('/post')
    def post_comment():
        """
            Post a new comment
        """
        g.cursor.execute(
            "INSERT INTO comments(author, comment) VALUES(?,?)",
            (g.email, g.comment)
        )
        return "Your comment has been inserted"

    @app.route('/get')
    def get_comment():
        """
            Get forum's comments
        """
        comments = g.cursor.execute("SELECT author, comment from comments")
        comments = g.cursor.fetchall()

        rows = ''
        response = "<table><tr><th>Author</th><th>comment</th></tr>{}"
        for entry in comments:
            rows += '<tr><td>{}</td><td>{}</td></tr>'.format(
                entry[0],
                entry[1],
            )

        response = response.format(rows)
        response = response + "</table>"
        return response

    return app


APP = create_app()
APP.config['DEBUG'] = True
APP.config['TESTING'] = True


if __name__ == '__main__':

    email = sys.argv[1]
    comment = sys.argv[2]

    if not comment:
        print('Missing comment')
        sys.exit(0)

    # Post comment
    conn = sqlite3.connect('/tmp/stored_xss.db', isolation_level=None)
    cursor = conn.cursor()
    tester = APP.test_client()
    ctx = APP.test_request_context()
    ctx.push()
    g.cursor = cursor
    g.email = email
    g.comment = comment

    response = tester.get(
        '/post',
    )

    conn.close()

    # Render
    process = subprocess.Popen(('python3', 'victim_browser.py'), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output.decode())
