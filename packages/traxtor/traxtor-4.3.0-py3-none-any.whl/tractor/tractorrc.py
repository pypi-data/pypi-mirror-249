#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2020-2023.

"""
this module creates tractorrc file
"""

import os
import tempfile

from . import bridges
from . import checks
from . import db


def create():
    """
    main function of the module
    # TODO: refactor to more little functions
    """
    my_ip, socks_port = checks.ip_port()
    dns_port_lines = (
        f"DNSPort {my_ip}:{str(db.get_val('dns-port'))}\n"
        "AutomapHostsOnResolve 1\n"
        "AutomapHostsSuffixes .exit,.onion\n"
    )
    data_dir = checks.data_dir()
    exit_node = db.get_val("exit-node")
    exit_node_policy = f"ExitNodes {'{'}{exit_node}{'}'}\n" "StrictNodes 1\n"
    bridge_type = db.get_val("bridge-type")
    with open(bridges.get_file(), encoding="utf-8") as file:
        my_bridges = file.read()
    my_bridges = bridges.relevant_lines(my_bridges, bridge_type)
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "tractorrc")
    with open(path, "w", encoding="utf-8") as file:
        file.write(f"SocksPort {my_ip}:{str(socks_port)}\n")
        if db.get_val("accept-connection"):
            file.write("SocksPolicy accept *\n")
        file.write(dns_port_lines)
        file.write(f"HTTPTunnelPort {my_ip}:{str(db.get_val('http-port'))}\n")
        file.write(f"DataDirectory {data_dir}\n")
        file.write(f"ControlSocket {data_dir}/control.sock\n")
        if exit_node != "ww":
            file.write(exit_node_policy)
        if bridge_type == 1:
            if not my_bridges:
                raise ValueError("No relevant bridges given")
            file.write("UseBridges 1\n")
            for line in my_bridges:
                file.write(f"Bridge {line}\n")
        elif bridge_type == 2:
            if not my_bridges:
                raise ValueError("No relevant bridges given")
            file.write("UseBridges 1\n")
            file.write(
                "ClientTransportPlugin obfs4 exec "
                + f"{db.get_val('plugable-transport')}\n"
            )
            for line in my_bridges:
                file.write(f"Bridge {line}\n")
        elif bridge_type != 0:
            raise ValueError("Bridge type is not supported")
    return tmpdir, path
