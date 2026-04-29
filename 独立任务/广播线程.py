
import time
import json
import socket
import ez.config


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = json.dumps({
        "更新端口": f"{ez.config.更新端口}",
        "日志端口": f"{ez.config.日志端口}"
    }).encode()

    while True:
        sock.sendto(message, ("192.168.1.255", ez.config.广播端口))
        time.sleep(ez.config.广播间隔)
