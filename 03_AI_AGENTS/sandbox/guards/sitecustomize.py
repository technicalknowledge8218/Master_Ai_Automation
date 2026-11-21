"""
sitecustomize.py
MASTER-AI Offline Sandbox Network Interceptor

Automatically imported by Python during startup when running in offline
sandboxed environments (Trust Levels 0, 1, 2). Intercepts socket connection
attempts and blocks outbound WAN connections.
"""

import socket
import errno

_orig_socket_connect = socket.socket.connect
_orig_socket_connect_ex = socket.socket.connect_ex
_orig_socket_sendto = socket.socket.sendto

def _is_loopback(address):
    if isinstance(address, tuple) and len(address) >= 2:
        host = str(address[0]).lower()
        return host in ("127.0.0.1", "localhost", "::1")
    elif isinstance(address, str):
        return address.lower() in ("127.0.0.1", "localhost", "::1")
    return False

def _master_ai_guarded_connect(self, address):
    if _is_loopback(address):
        return _orig_socket_connect(self, address)
    raise PermissionError(
        f"MASTER-AI Network Block: Outbound network connection to '{address}' is prohibited "
        f"under offline sandbox execution policy."
    )

def _master_ai_guarded_connect_ex(self, address):
    if _is_loopback(address):
        return _orig_socket_connect_ex(self, address)
    # Return ECONNREFUSED or raise PermissionError to fail closed
    return errno.ECONNREFUSED

def _master_ai_guarded_sendto(self, data, *args):
    # args can be (address,) or (flags, address)
    target_addr = args[-1] if args else None
    if target_addr and _is_loopback(target_addr):
        return _orig_socket_sendto(self, data, *args)
    raise PermissionError(
        f"MASTER-AI Network Block: Outbound UDP datagram to '{target_addr}' is prohibited "
        f"under offline sandbox execution policy."
    )

socket.socket.connect = _master_ai_guarded_connect
socket.socket.connect_ex = _master_ai_guarded_connect_ex
socket.socket.sendto = _master_ai_guarded_sendto
