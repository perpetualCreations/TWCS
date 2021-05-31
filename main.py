"""
Temporary Web Captive Service.

Made by perpetualCreations
"""

import flask
import flask_socketio
import configparser
from os import urandom
from ast import literal_eval

config = configparser.ConfigParser()
config.read("main.cfg")
application = flask.Flask(__name__)
application.secret_key = urandom(4096)
socket_io = flask_socketio.SocketIO(application)


@application.route("/")
def index() -> any:
    """
    Render template when root is requested, start handling referrer.

    :return: any
    :rtype: any
    """


if __name__ == "__main__":
    socket_io.run(application, debug=literal_eval(config["CORE"]["DEBUG"]),
                  port=80, use_reloader=False)
