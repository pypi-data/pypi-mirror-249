# -*- coding: utf-8 -*-
import platform


def is_mac() -> bool:
    """
    is Mac
    :return:
    """
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """
    is linux
    """
    return platform.system() == "Linux"


def is_termux() -> bool:
    """
    is termux
    """
    return is_linux()
