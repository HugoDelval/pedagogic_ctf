#!/usr/bin/python3

import bleach
import lxml
import sqlite3
import subprocess
import sys

from flask import Flask, g, request
from werkzeug.exceptions import BadRequest


def create_app():
    """
        Initialize Flask application
    """
    app = Flask(__name__)

    @app.route('/comments', methods=['POST'])
    def post_comment():
        """
            Post a new comment
        """
        comment = request.form.get('comment')
        if not comment:
            raise BadRequest('Missing comment param')

        g.cursor.execute(
            "INSERT INTO comments(author, comment) VALUES(?,?)",
            (g.email, comment)
        )
        return "Your comment has been inserted"

    @app.route('/comments', methods=['GET'])
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

    tester.post(
        '/comments',
        data=dict(comment=comment)
    )
    conn.close()

    # Render
    process = subprocess.Popen(('python3', 'victim_browser.py', email), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output.decode())
