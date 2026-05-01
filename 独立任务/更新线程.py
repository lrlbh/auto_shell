import struct

import time

import json
import threading

import socket
import ez.config
import ez.pub


def recv_all(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            # 返回空代表连接已关闭
            return None
        data += packet
    return data


# 为了只保留最新单片机,让send线程退出
当前端口 = None


def read(cs: socket.socket, addr):
    global 当前端口
    try:
        while True:
            当前端口 = addr[1]
            t_l = struct.unpack("!I", recv_all(cs, 4))[0]
            ez.pub.单片机心跳 = time.time()
            ez.pub.单片机ip = addr[0]
            ez.pub.单片机端口 = addr[1]
            data = recv_all(cs, t_l)
            ez.pub.cli_ip = json.loads(data.decode())
    except:  # noqa: E722
        cs.close()


def send(cs: socket.socket, addr):
    global 当前端口
    try:
        while True:
            if 当前端口 != addr[1]:
                cs.close()

            if ez.pub.send_msg is None:
                time.sleep(0.03)
                continue
            cs.sendall(ez.pub.send_msg)
            ez.pub.send_msg = None
            # ez.pub.日志控件.cyan("发送成功")
            # ez.pub.日志控件.cyan(str(addr))

    except:  # noqa: E722
        cs.close()


def run():
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_socket.bind(("0.0.0.0", ez.config.更新端口))
    s_socket.listen(3)

    while True:
        c_soket, client_address = s_socket.accept()

        threading.Thread(
            target=read, args=(c_soket, client_address), daemon=True
        ).start()

        threading.Thread(
            target=send, args=(c_soket, client_address), daemon=True
        ).start()
