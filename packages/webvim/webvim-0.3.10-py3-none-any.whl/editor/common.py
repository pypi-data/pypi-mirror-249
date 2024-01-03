# -*- coding: utf-8 -*-
import os
import sys
import typing

import click
from flask import Response, jsonify

from editor.daemon import mac, utils, termux

RESULT_CODE_ERROR = 0
RESULT_CODE_SUCCESS = 1


def build_response(code: int = RESULT_CODE_SUCCESS,
                   data: typing.Any = None,
                   message: str = None) -> Response:
    """
    build response
    """
    datas = {
        "code": code
    }
    if data:
        datas["data"] = data
    if message:
        datas["message"] = message
    return jsonify(datas)


def exist_file(file: str) -> bool:
    """
    exist file
    """
    return os.path.exists(file) and os.path.isfile(file)


def run_service(app_name: str, signal: str):
    """
    run service
    """
    try:
        cmd_path = os.path.abspath(sys.argv[0])
        if cmd_path.endswith(".py"):
            click.echo(message="Not Support", err=True)
            return
        if signal == "install":
            cmd = [cmd_path, "--init"]
            if utils.is_mac():
                mac.mac_install(name=app_name, program_arguments=cmd)
            if utils.is_termux():
                termux.sv_install(name=app_name, run_content=" ".join(cmd))
            click.secho("Done", fg="green")
        elif signal == "start":
            if utils.is_mac():
                mac.mac_start(name=app_name)
            if utils.is_termux():
                termux.sv_start(name=app_name)
            click.secho("Done", fg="green")
        elif signal == "stop":
            if utils.is_mac():
                mac.mac_stop(name=app_name)
            if utils.is_termux():
                termux.sv_stop(name=app_name)
            click.secho("Done", fg="green")
        elif signal == "status":
            if utils.is_mac():
                is_install = mac.mac_is_install(name=app_name)
                if is_install:
                    is_running = mac.mac_is_running(name=app_name)
                    if is_running:
                        click.secho("Running", fg="green")
                    else:
                        click.secho("Stopped", fg="red")
                else:
                    click.secho("Not Install", fg="red")
            if utils.is_termux():
                is_install = termux.sv_is_install(name=app_name)
                if is_install:
                    is_running = termux.sv_is_running(name=app_name)
                    if is_running:
                        click.secho("Running", fg="green")
                    else:
                        click.secho("Stopped", fg="red")
                else:
                    click.secho("Not Install", fg="red")
        elif signal == "rm":
            if utils.is_mac():
                mac.mac_rm(name=app_name)
            if utils.is_termux():
                termux.sv_rm(name=app_name)
            click.secho("Done", fg="green")
        else:
            pass
    except RuntimeError as e:
        click.secho(e, fg="red")


def init_launch_agents() -> [str]:
    """
    init LaunchAgents
    """
    launch_agent_list = []
    if utils.is_mac():
        launch_agents = os.path.join(os.path.expanduser("~"), "Library", "LaunchAgents")
        plists = [x for x in os.listdir(launch_agents) if x.endswith(".plist") and "org.seven" in x]
        for plist in plists:
            launch_agent_list.append(os.path.join(launch_agents, plist))
    return launch_agent_list
