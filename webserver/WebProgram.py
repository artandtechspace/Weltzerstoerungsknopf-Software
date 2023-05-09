import asyncio

from flask import Flask, jsonify, request, Response
from MainProgram import MainProgram
from core.CoreData import CoreData

# Flask-app
app = Flask("Weltzerstörungsknopf-Webaccess")
app.config['CORS_HEADERS'] = 'Content-Type'

# References to the main program and core-data
main_program: MainProgram  # Will be willed as soon as the server starts
core: CoreData


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
def get_config():
    return create_cors_resp(core.config.get().data, 200)


@app.route("/api/start_tests", methods=["POST", "OPTIONS"])
async def update_config():
    if request.method == "OPTIONS":
        return enable_cors()

    # Checks if the content type is invalid
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        # Sends back an invalid-request response
        return create_cors_resp("Content-Type must be json.", 400)

    cfg_json = request.json

    # Ensures the test-type is specified

    # Validates the data
    if not core.config.try_add_custom(cfg_json):
        # Sends back an invalid-request response
        return create_cors_resp("Content has an invalid format.", 400)

    # Saves the config to disk
    core.config.save()

    # Sends back success
    return create_cors_resp({}, 200)


# Start-function for the web-thread to run the webserver
def run_web_thread(prog: MainProgram, cr: CoreData):
    global main_program, core
    main_program = prog
    core = cr
    app.run(debug=False, use_reloader=False)
