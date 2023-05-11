import asyncio

from flask import Flask, jsonify, request, Response, send_from_directory
from MainProgram import MainProgram
from core.CoreData import CoreData
from peripherals.tests.PeripheralTestTypes import PeripheralTestType, as_json
from flask_socketio import SocketIO, emit
from loggingsystem.LoggingManager import LoggingManager
import os

# Flask-app
app = Flask("Weltzerstörungsknopf-Webaccess")
socketio = SocketIO(app, cors_allowed_origins='*')

# References to the main program and core-data
main_program: MainProgram  # Will be willed as soon as the server starts
core: CoreData


# Returns the webserver directory
def webserver_dir():
    return os.path.abspath(os.path.dirname(__file__)) + "/../rsc/webpage/Weltzerstoerungsknopf-Configinterface"


# Takes in an object, converts it to a request and adds the required cors headers
def create_cors_resp(blob: object, code: int):
    response = jsonify(blob)
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response, code


# Creates an options-request that tells the browser that cors is fully enabled
def enable_cors():
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp, 200


# Sends the config data as json
@app.route("/api/update_config", methods=["GET", "POST", "OPTIONS"])
async def update_config():
    if request.method == "OPTIONS":
        return enable_cors()

    # Checks if the content type is invalid
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        # Sends back an invalid-request response
        return create_cors_resp("Content-Type must be json.", 400)

    cfg_json = request.json

    # Validates the data
    if not core.config.try_add_custom(cfg_json):
        # Sends back an invalid-request response
        return create_cors_resp("Content has an invalid format.", 400)

    # Saves the config to disk
    core.config.save()

    # Sends back success
    return create_cors_resp({}, 200)


# Sends the config data as json
@app.route("/api/get_config", methods=["GET"])
async def get_config():
    return create_cors_resp(core.config.get().data, 200)


@app.route("/api/get_tests", methods=["GET"])
def get_tests():
    # Collects all peripheral-device test-types
    tests_json = {}

    for dev in PeripheralTestType:
        # Gets the data
        name = dev.value[0]
        # Appends the test
        tests_json[name] = as_json(dev)

    return create_cors_resp(tests_json, 200)


@app.route("/api/start_test", methods=["POST", "OPTIONS"])
async def start_tests():
    if request.method == "OPTIONS":
        return enable_cors()

    # Gets the data as a string
    raw_info = request.data.decode('ascii')

    # Tries to find the device
    for dev in PeripheralTestType:
        if dev.value[0] == raw_info:

            # Tries to start a test
            if await main_program.insert_test(dev):
                # Sends back success
                return create_cors_resp({}, 200)
            else:
                # Sends back the error that the server is not in idle mode
                return create_cors_resp({"message": "tests can only be run when the program is in idle-mode."}, 412)

    # Sends back the error that the given test couldn't be found
    return create_cors_resp({"message": "tests can not be found"}, 405)


@socketio.on('connect', namespace="/logs")
def connect():
    # Sends all logs that existed up until that point
    emit('inital', LoggingManager.get_logs_as_json())


# Serves the web-app for configuration
@app.route('/<path:filename>')
def access_webapp(filename):
    return send_from_directory(webserver_dir(), filename)


# Directly serves the index-html when only requesting the root
@app.route('/')
def webapp_quality_of_life():
    return send_from_directory(webserver_dir(), "index.html")


# Broadcasts a new log to all systems
def broadcast_log(log: object):
    socketio.emit("log", log, namespace="/logs")


# Start-function for the web-thread to run the webserver
def run_web_thread(prog: MainProgram, cr: CoreData):
    global main_program, core
    main_program = prog
    core = cr
    socketio.run(app, debug=False, use_reloader=False, host='0.0.0.0', allow_unsafe_werkzeug=True)
