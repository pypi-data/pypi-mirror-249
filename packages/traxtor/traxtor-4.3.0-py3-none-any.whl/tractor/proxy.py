#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022

"""
module for setting and removing proxy
"""

from gi.repository import Gio
from . import checks


def proxy_set() -> None:
    """
    setup proxy
    """
    if checks.proxy_set():
        print("Proxy is already set")
    else:
        proxy = Gio.Settings.new("org.gnome.system.proxy")
        socks = Gio.Settings.new("org.gnome.system.proxy.socks")
        myip, socks_port = checks.ip_port()
        ignored = [
            "localhost",
            "127.0.0.0/8",
            "::1",
            "192.168.0.0/16",
            "10.0.0.0/8",
            "172.16.0.0/12",
        ]
        socks.set_string("host", myip)
        socks.set_int("port", socks_port)
        proxy.set_string("mode", "manual")
        proxy.set_strv("ignore-hosts", ignored)
        print("Proxy set")


def proxy_unset() -> None:
    """
    unset proxy
    """
    if checks.proxy_set():
        proxy = Gio.Settings.new("org.gnome.system.proxy")
        proxy.set_string("mode", "none")
        print("Proxy unset")
    else:
        print("Proxy is not set")
