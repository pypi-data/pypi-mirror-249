# -*- coding: utf-8 -*-
import os
import shutil

SERVICE_ROOT = "/data/data/com.termux/files/usr/var/service"
RUN_TEMPLATE = "#!/data/data/com.termux/files/usr/bin/sh\nexec {0} 2>&1"


def service_root() -> str:
    """
    launch agents
    """
    if not os.path.exists(SERVICE_ROOT):
        os.mkdir(SERVICE_ROOT)
    if not os.path.isdir(SERVICE_ROOT):
        raise RuntimeError("Service root is not dir")
    return SERVICE_ROOT


def _read_file(file: str) -> str:
    """
    read file
    :param file:
    :return:
    """
    with open(file, 'r') as f:
        content = f.read()
    return content.strip()


def sv_start(name: str) -> None:
    """
    sv start
    """
    if not sv_is_install(name=name):
        raise RuntimeError("Not Install")
    if not sv_is_running(name):
        os.system("sv-enable {0}".format(name))


def sv_stop(name: str) -> None:
    """
    sv stop
    """
    if not sv_is_install(name=name):
        raise RuntimeError("Not Install")
    if sv_is_running(name):
        os.system("sv-disable {0}".format(name))


def sv_rm(name: str) -> None:
    """
    sv rm
    """
    if sv_is_install(name):
        if sv_is_running(name):
            sv_stop(name)
        shutil.rmtree(os.path.join(service_root(), name))


def sv_is_running(name: str) -> bool:
    """
    sv is running
    """
    pid_file = os.path.join(service_root(), name, "supervise", "pid")
    pid_content = _read_file(pid_file)
    return pid_content and int(pid_content) > 0


def sv_is_install(name: str) -> bool:
    """
    is install
    """
    run_file = os.path.join(service_root(), name, "run")
    return os.path.exists(run_file)


def sv_install(name: str, run_content: str) -> None:
    """
    sv install
    """
    if not name:
        raise ValueError("name empty")
    if not run_content:
        raise ValueError("run_content empty")
    service_dir = os.path.join(service_root(), name)
    if os.path.exists(service_dir):
        raise RuntimeError("service {0} exist".format(name))
    os.mkdir(service_dir)
    run_file = os.path.join(service_dir, "run")
    with open(run_file, 'w') as f:
        f.write(RUN_TEMPLATE.format(run_content))
    os.chmod(run_file, 0o755)
