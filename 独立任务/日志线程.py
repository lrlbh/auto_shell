import datetime
import socket
import os
import ez.pub
import ez.config


def run():
    """UDP 日志线程（内部闭包处理格式化和路径修正）"""

    def log_with_time(msg: str):
        """带时分秒毫秒的日志输出"""
        now = datetime.datetime.now()
        timestr = now.strftime("%H:%M:%S.%f")[:-3]
        return f"[{timestr}] {msg}"

    def fix_traceback_paths(text: str) -> str:
        """把 traceback 中的相对路径拼接成 BASE_DIR 下的绝对路径"""
        lines = []
        for line in text.splitlines():
            if line.strip().startswith('File "'):
                parts = line.split('"')
                if len(parts) >= 2:
                    filepath = parts[1]
                    abs_path = os.path.join(ez.pub.选中的项目目录, filepath)
                    line = line.replace(filepath, abs_path)
            lines.append(line)

        return "\n".join(lines).replace("/", "\\")

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", ez.config.日志端口))
    while True:
        data, addr = udp_sock.recvfrom(4096)
        text = data.decode(errors="ignore")
        if "Traceback (most recent call last):" in text:
            text = fix_traceback_paths(text)
        if ez.pub.日志控件 is not None:
            ez.pub.日志控件.all(text, ez.pub.日志字体大小)
