

import struct

import time

import json
import threading

import socket
import ez.config
import ez.pub
import tl.dir
import os


def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            # 返回空代表连接已关闭
            return None
        data += packet
    return data


def read(c_soket: socket.socket, addr):
    try:
        while True:
            t_l = struct.unpack('!I', recv_all(c_soket, 4))[0]
            data = recv_all(c_soket, t_l)
            ez.pub.cli_ip = json.loads(data.decode())
    except:
        c_soket.close()


def send(c_soket: socket.socket, addr):
    try:
        while True:
            if ez.pub.send_msg is None:
                time.sleep(0.05)
                continue
            c_soket.sendall(ez.pub.send_msg)
            ez.pub.日志控件.cyan("发送成功")
            ez.pub.send_msg = None
    except:
        c_soket.close()


def run():
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_socket.bind(("0.0.0.0", ez.config.更新端口))
    s_socket.listen(3)

    while True:
        c_soket, client_address = s_socket.accept()

        threading.Thread(target=read, args=(
            c_soket, client_address), daemon=True).start()

        threading.Thread(target=send, args=(
            c_soket, client_address), daemon=True).start()
