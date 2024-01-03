# -*- coding: utf-8 -*-
import base64
import os.path
import sys
from urllib.parse import unquote

import click
from flask import Flask, request, make_response, Response
from flask_basicauth import BasicAuth

from editor import common

VERSION = "0.3.11"

APP_NAME = "webvim"

LOCAL_PORT = 8880
LOCAL_HOST = "0.0.0.0"

DEFAULT_FILE_LIST = [
    "/etc/hosts",
    "/etc/profile",
    os.path.join(os.path.expanduser("~"), ".zshrc"),
    os.path.join(os.path.expanduser("~"), ".ssh", "id_rsa.pub"),
    os.path.join(os.path.expanduser("~"), ".ssh", "authorized_keys"),
    "/opt/homebrew/etc/nginx/nginx.conf",
    "/usr/local/etc/nginx/nginx.conf"
]

file_to_edit = []

app = Flask(__name__, static_url_path='')

# basic auth
basic_auth = BasicAuth(app=app)


@app.after_request
def func_res(resp) -> Response:
    res = make_response(resp)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.errorhandler(Exception)
def handle_generic_error(error) -> Response:
    """
    handle error
    """
    return common.build_response(code=common.RESULT_CODE_ERROR, message=str(error))


@app.route('/', methods=["GET"])
def home() -> Response:
    """
    home page
    """
    return app.send_static_file(filename="index.html")


@app.route('/main', methods=["GET"])
def main_data() -> Response:
    """
    main data
    """
    key = request.args.get("key")
    path = base64.b64decode(key.encode("utf-8")).decode("utf-8") if key else file_to_edit[0]
    file_obj = get_file_obj(path=path)
    nav_obj = get_nav_obj(path=path)
    return common.build_response(data={
        "fobj": file_obj,
        "nobj": nav_obj
    })


@app.route('/save', methods=["POST"])
def save_content() -> Response:
    """
    save content
    """
    json_content = request.json
    content_sec = json_content["content"]
    key = json_content["key"]
    path = base64.b64decode(key.encode("utf-8")).decode("utf-8")
    content = unquote(base64.b64decode(content_sec).decode("utf-8"))
    if path and os.path.exists(path) and os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(content)
    return common.build_response(code=common.RESULT_CODE_SUCCESS, message="Success")


# ------------------------------------------------------------

def get_nav_obj(path: str) -> list:
    """
    get nav obj
    """
    navs = []
    for f in file_to_edit:
        file_obj = dict()
        file_obj["fileName"] = os.path.basename(f)
        file_obj["fileKey"] = base64.b64encode(f.encode("utf-8")).decode("utf-8")
        file_obj["fileStatus"] = (path == f)
        navs.append(file_obj)
    return navs


def get_file_obj(path: str) -> dict:
    """
    get file obj
    """
    file_obj = dict()
    file_obj["filePath"] = path
    file_obj["fileName"] = os.path.basename(path)
    file_obj["fileKey"] = base64.b64encode(path.encode("utf-8")).decode("utf-8")
    with open(path, 'r') as f:
        file_obj["fileContent"] = f.read()
    return file_obj


@click.command(epilog='make it easy', help='Web Editor {0}'.format(VERSION))
@click.option('-i', '--ip', type=str, show_default=True, default=LOCAL_HOST, help="Local IP")
@click.option('-p', '--port', type=int, show_default=True, default=LOCAL_PORT, help='Local Port')
@click.option('--file', multiple=True, default=[], help='File To Edit')
@click.option('--username', type=str, show_default=True, default='admin', help='Basic Auth Username')
@click.option('--password', type=str, show_default=True, default='admin', help='Basic Auth Password')
@click.option('--init', is_flag=True, help='Init Default Files')
@click.option('--auth', is_flag=True, help='Use Basic Auth')
@click.option('-s', '--signal', help='send signal to service',
              type=click.Choice(['install', 'start', 'stop', 'status', 'rm'], case_sensitive=False))
def run_web(signal: str, ip: str, port: int, init: bool, auth: bool, username: str, password: str, file):
    """
    run web
    """
    if signal:
        common.run_service(app_name=APP_NAME, signal=signal)
        return
    host = ip
    try:
        file_to_edit.clear()
        if init:
            for agent in common.init_launch_agents():
                DEFAULT_FILE_LIST.append(agent)
            temp_list = filter(common.exist_file, DEFAULT_FILE_LIST)
            for f in temp_list:
                file_to_edit.append(f)
        for f in file:
            if common.exist_file(f):
                file_to_edit.append(f)
            else:
                raise FileNotFoundError("File not found {0}".format(f))
        # ----------
        if len(file_to_edit) == 0:
            raise ValueError("No file to edit")
        # basic auth
        if auth:
            app.config['BASIC_AUTH_USERNAME'] = username
            app.config['BASIC_AUTH_PASSWORD'] = password
            app.config['BASIC_AUTH_FORCE'] = True
        # run server
        app.run(port=port, host=host, debug=False)
    except ValueError as e:
        click.echo(message=e, err=True)
    except FileNotFoundError as e:
        click.echo(message=e, err=True)


def execute():
    """
    execute
    """
    run_web()


if __name__ == '__main__':
    # sys.argv.append("--help")
    # sys.argv.append("-s")
    # sys.argv.append("install")
    sys.argv.append("--init")
    execute()
