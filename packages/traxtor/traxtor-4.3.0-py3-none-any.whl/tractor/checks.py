#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2020-2023.

"""
actions for tractor internals
"""

from gi.repository import Gio, GLib
from requests import get
from stem.util import system

from . import db


def proc() -> int:
    """
    return the pid of tor process
    """
    port = db.get_val("socks-port")
    return system.pid_by_port(port)


def running() -> bool:
    """
    checks if Tractor is running or not
    """
    if proc():
        return system.is_running(proc())
    return False


def connected() -> bool:
    """
    checks if Tractor is connected or not
    """
    if running():
        port = db.get_val("socks-port")
        host = "https://check.torproject.org/"
        proxy = f"socks5h://127.0.0.1:{port}"
        expectation = "Congratulations."
        try:
            request = get(
                host, proxies={"http": proxy, "https": proxy}, timeout=10
            )
            if request.status_code == 200 and expectation in request.text:
                return True
            return False
        except Exception:
            return False
    return False


def proxy_set() -> bool:
    """
    checks if proxy is set or not
    """
    schema = "org.gnome.system.proxy"
    conf = Gio.Settings.new(schema)
    if conf.get_string("mode") != "manual":
        return False
    x_ip, x_port = ip_port()
    schema = "org.gnome.system.proxy.socks"
    conf = Gio.Settings.new(schema)
    my_ip = conf.get_string("host")
    my_port = conf.get_int("port")
    if my_ip == x_ip and my_port == x_port:
        return True
    return False


def ip_port() -> tuple[str, int]:
    """
    returns ip ans socks port
    """
    if db.get_val("accept-connection"):
        my_ip = "0.0.0.0"
    else:
        my_ip = "127.0.0.1"
    port = db.get_val("socks-port")
    return my_ip, port


def data_dir() -> str:
    """
    return the data directory of tractor
    """
    return GLib.get_user_config_dir() + "/tractor/"
