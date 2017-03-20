#!/usr/bin/python3

import sys

from base64 import b64encode
from time import time

from Crypto.Cipher import AES
from flask import Flask, g


def create_app():
    """
        Initialize Flask application
    """
    app = Flask(__name__)

    @app.route('/encrypted-text')
    def encrypted_text():
        """
            Return encrypted text
        """
        # following SOC advisory:
        with open('key') as key:
            # 1) Removed plain AES key used to cipher secret from code
            secretKey = key.read()
            # 2) use an IV that change at every request
            iv = b64encode(bytes(str(int(time())), "utf-8"))
            # 3) Use military grade encryption cipher
            obj = AES.new(secretKey, AES.MODE_CBC, iv)
            try:
                ciphertext = obj.encrypt(g.plain)
            except:
                # hum... anyway, crypto should not rely on obscurity!
                return "Encryption problem!\nIs your message 16 bytes long?\nDumping usefull info:\n {}".format(
                    secretKey)
            return "Here is the encrypted text to be pass to your other app: {}.{}".format(
                iv.decode('ascii'), b64encode(ciphertext).decode('ascii')
            )

    return app


APP = create_app()
APP.config['DEBUG'] = True
APP.config['TESTING'] = True


if __name__ == '__main__':

    # Init app and db cursor
    try:
        tester = APP.test_client()
        ctx = APP.test_request_context()
        ctx.push()
        if len(sys.argv) > 1:
            g.plain = sys.argv[1]
        else:
            with open('secret') as secret:
                g.plain = secret.read()
    except:
        print('Error while Initialize.')
        sys.exit(1)

    endpoint = '/encrypted-text'

    # Make request
    response = tester.get(
        endpoint
    )

    print(response.get_data().decode('unicode_escape'))
