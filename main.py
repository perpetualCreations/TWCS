"""
Temporary Web Captive Service.

Made by perpetualCreations
"""

import configparser
import threading
import json
import sqlite3
from os import urandom
from os.path import isfile
from ast import literal_eval
from time import sleep, time
import flask
import flask_socketio
import requests

config = configparser.ConfigParser()
config.read("main.cfg")
application = flask.Flask(__name__)
application.secret_key = urandom(4096)
socket_io = flask_socketio.SocketIO(application)

check_daemons: dict = {}

if not isfile("eta.db"):
    eta_database = sqlite3.connect("eta.db")
    eta_database.cursor().execute('''CREATE TABLE eta (
    nid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    referrer VARCHAR(2000) NOT NULL,
    eta INT DEFAULT NULL);''')
else:
    eta_database = sqlite3.connect("eta.db")


@socket_io.on("requestETA")
def eta_request_handler(json_payload) -> None:
    """
    Handle client requests for ETA times, when given a referrer URL.

    :param json_payload: JSON request data from client
    """
    json_payload = json.loads(str(json_payload).replace("'", '"'))
    flask_socketio.emit("postETA",
                        {"eta": eta_database.cursor().execute(
                            "SELECT * FROM eta WHERE referrer=:ref",
                            {"ref": json_payload["referrer"]}).fetch()[2]})


@socket_io.on("revealFate")
def fate_broadcaster(fate: bool, url: str):
    """
    Broadcast to clients over web sockets the referrer fate.

    The fate informs the client whether the referrer is up, or if maximum
    ping attempts have occured.
    The client will decide whether to abort with an error message, or redirect
    back to referrer, based on the referrer fate.

    :param fate: True for referrer being up, False for max ping attempts being
        passed, and referrer still down
    :type fate: bool
    :param url: URL to referrer
    :type url: str
    """
    with application.app_context():
        flask_socketio.emit("revealFate", {"url": url, "fate": fate},
                            broadcast=True)


def check(url: str) -> None:
    """
    Check URL to see if referrer is up. If so, redirect clients.

    :param url: URL to referrer
    :type url: str
    """
    first_pass = True
    pings = 0
    if url[:4] != "http":
        url = "http://" + url
    init_time = time()
    while True:
        # pylint: disable=broad-except
        try:
            status = requests.get(url).status_code
        except Exception:
            status = None
        if status in (list(range(200, 227)) + [302, 401]):
            if first_pass is True:
                sleep(int(config["CORE"]["DELAY_INITIAL"]))
                first_pass = False
            exit_time = time() - init_time
            eta_data = eta_database.cursor().execute(
                "SELECT * FROM eta WHERE referrer=:ref",
                {"ref": flask.request.referrer}).fetch()
            if not eta_data:
                eta_database.cursor().execute(
                    "INSERT INTO eta VALUES (referrer, eta) VALUES" +
                    " (:ref, :eta)", {"ref": url, "eta": time() - exit_time})
            else:
                eta_database.cursor().execute(
                    "UPDATE eta SET eta=:eta WHERE referrer=:ref",
                    {"ref": url, "eta": round((eta_data[2] + exit_time)/2)})
            fate_broadcaster(True, url)
            break
        pings += 1
        if int(config["CORE"]["PING_MAX"]) != -1 and \
                pings >= int(config["CORE"]["PING_MAX"]):
            fate_broadcaster(False, url)
            break
        first_pass = False
        sleep(int(config["CORE"]["DELAY_PING"]))


@application.route("/")
def index() -> any:
    """
    Render template when root is requested, start handling referrer.

    :return: any
    :rtype: any
    """
    if flask.request.referrer not in check_daemons:
        check_daemons.update(
            {flask.request.referrer:
                threading.Thread(target=check, args=(flask.request.referrer,))}
            )
    return flask.render_template(config["UI"]["TEMPLATE_NAME"],
                                 referrer=flask.request.referrer)


if __name__ == "__main__":
    socket_io.run(application, debug=literal_eval(config["CORE"]["DEBUG"]),
                  port=80, use_reloader=False)
