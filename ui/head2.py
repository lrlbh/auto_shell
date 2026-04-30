import os.path
from shutil import which
import time
import re
import subprocess

from PyQt6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QCompleter,
)

from tl import pyb
import tl.all
import tl.dir
import tl.qt
import os
from PyQt6.QtCore import QThread, QTimer, Qt
import ez.config
import ez.pub
from PyQt6.QtGui import QFont, QTextCursor

from tl.qt import head
import sys
from PyQt6.QtWidgets import QApplication
from pathlib import Path
import ui.lib
from tl.pyb import Pyb


@head.add
def 选择屏幕():
    def on_change(index):
        # 1. 直接通过当前索引获取绑定的 Data (即屏幕["index"])
        current_id = combo.itemData(index)
        # print(f"id = {current_id}")
        tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)
        # tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)
        # tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)
        # tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)

    # 创建下拉框
    combo = QComboBox(ez.pub.mw)
    combo.setMinimumHeight(8)

    # 添加选项
    for 屏幕 in tl.qt.get_屏幕列表():
        combo.addItem(屏幕["name"], 屏幕["index"])
        # print(屏幕["index"])
        # print(屏幕["name"])

    combo.setCurrentIndex(ez.config.默认显示器)

    combo.activated.connect(on_change)

    return combo


@head.add
def 清空日志():
    def on_change():
        ez.pub.日志控件.clear()

    but = QPushButton(ez.pub.mw)
    but.setText("清空日志")
    but.clicked.connect(on_change)

    return but


@head.add
def 生成依赖():

    @ui.lib.选择项目没
    def on_change(checked=None):

        依赖目录 = os.path.join(ez.pub.shell项目目录, "mpy")
        file_path = tl.dir.get_files_path(
            依赖目录, ["__pycache__", "boot.py", "boot_run.py"]
        )
        # print(file_path)
        for file_name in file_path:
            with open(file_name, "rb") as f:
                file_data = f.read()

            # 相对路径
            file_name = file_name.replace(str(依赖目录), "").lstrip("\\/")

            # 写入文件
            tl.dir.ensure_path_exists(os.path.join(ez.pub.选中的项目目录, file_name))
            with open(os.path.join(ez.pub.选中的项目目录, file_name), "wb") as f:
                f.write(file_data)

    but = QPushButton(ez.pub.mw)
    but.setText("生成依赖")
    but.clicked.connect(on_change)

    return but


@head.add
def 生成boot():

    @ui.lib.选择项目没
    def on_change(checked=None):
        依赖目录 = os.path.join(ez.pub.shell项目目录, "mpy")
        file_path = [
            os.path.join(依赖目录, "boot.py"),
            os.path.join(依赖目录, "boot_run.py"),
        ]
        for file_name in file_path:
            with open(file_name, "rb") as f:
                file_data = f.read()

            # 相对路径
            file_name = file_name.replace(str(依赖目录), "").lstrip("\\/")

            # 写入文件
            with open(os.path.join(ez.pub.选中的项目目录, file_name), "wb") as f:
                f.write(file_data)

    but = QPushButton(ez.pub.mw)
    but.setText("生成boot")
    but.clicked.connect(on_change)

    return but


@head.add
def 控件字体():
    def on_change(index):
        ez.config.头部字体和大小[1] = int(combo.currentText())
        head.set_font_size(QFont(*ez.config.头部字体和大小))

    # 创建下拉框
    combo = QComboBox(ez.pub.mw)
    combo.setMinimumHeight(8)

    # 字体项
    for i in range(8, 45):
        combo.addItem(str(i))

    # 默认选中
    combo.setCurrentText(str(ez.config.头部字体和大小[1]))

    combo.activated.connect(on_change)

    return combo


@head.add
def 日志字体():
    def on_change(index):
        font_size = combo.currentText()
        ez.pub.日志字体大小 = int(font_size)

    # 创建下拉框
    combo = QComboBox(ez.pub.mw)
    combo.setMinimumHeight(8)
    for i in range(6, 67):
        combo.addItem(str(i))

    combo.setCurrentText(str(ez.pub.日志字体大小))

    combo.activated.connect(on_change)

    return combo


@head.add
def 串口显示():

    最新com口 = []
    当前com口 = []

    # def on_change(index):
    #     font_size = combo.currentText()
    #     ez.pub.日志字体默认大小 = int(font_size)

    # 创建下拉框
    combo = QComboBox(ez.pub.mw)
    combo.setMinimumHeight(8)
    # combo.activated.connect(on_change)

    # 创建一个继承自 QThread 的类，并重写 run 方法
    class PortWorker(QThread):
        def __init__(self, parent=None):
            super().__init__(parent)

        def run(self):
            nonlocal 最新com口
            while True:
                try:
                    # 获取串口设备
                    # 运行 PowerShell 命令
                    command = """powershell -Command "Get-WmiObject Win32_PnPEntity | Where-Object {$_.Name -like '*(COM*)'} | Select-Object Name, Description\\ " """
                    result = subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        shell=True,
                        # encoding="utf-8",
                    )

                    # 解析输出结果
                    output_lines = result.stdout.splitlines()
                    serial_ports = []
                    for line in output_lines:
                        match = re.match(r"(.*) \(COM(\d+)\)", line)
                        if match:
                            port_name = f"COM{match.group(2)}"
                            description = match.group(1)
                            if "蓝牙链接上的标准串行" in description:
                                continue
                            # serial_ports.append(port_name + "-->" + description)
                            serial_ports.append(port_name)

                    最新com口 = serial_ports
                except:  # noqa: E722
                    最新com口 = []

        def stop(self):
            self.terminate()  # 终止线程
            self.wait()  # 等待线程结束
            print("com线程结束")

    # 创建线程
    thread = PortWorker(ez.pub.mw)
    thread.start()  # 启动线程
    ez.pub.mw.destroyed.connect(thread.stop)  # 在窗口关闭时停止线程

    # 定时器回调,更新下拉框
    def timer_callback():
        nonlocal 当前com口
        if 最新com口 == 当前com口:
            return
        当前com口 = 最新com口
        combo.clear()
        combo.addItems(当前com口)

    # 创建定时器
    timer = QTimer(ez.pub.mw)
    timer.timeout.connect(timer_callback)
    timer.setInterval(100)  # 设置定时器的间隔，单位为毫秒
    timer.start()  # 启动定时器

    ez.pub.com选择框 = combo
    return combo


# def upload_boot(port):
#     try:

#                 # 读取文件
#         with open("lib/boot.py", "rb") as f:
#             data = f.read()

#         # 打开串口
#         ser = serial.Serial(port, 115200, timeout=1)
#         # time.sleep(1)

#         def exec_raw(cmd):
#             """发送命令并等待OK"""
#             ser.write(cmd + b"\x04")  # Ctrl-D 执行
#             out = b""
#             t0 = time.time()
#             while time.time() - t0 < 2:
#                 out += ser.read_all()
#                 if b"OK" in out or b">>>" in out:
#                     break
#                 time.sleep(0.05)
#             return out
#         # 进入 raw REPL
#         ser.write(b"\r\x03")  # Ctrl-C
#         time.sleep(0.2)
#         ser.write(b"\r\x03")  # Ctrl-C
#         time.sleep(0.2)
#         ser.write(b"\r\x01")  # Ctrl-A
#         time.sleep(0.2)

#         print("开始上传 boot.py ...")
#         exec_raw(b"f=open('boot.py','wb')")

#         chunk = 128
#         for i in range(0, len(data), chunk):
#             part = data[i : i + chunk]
#             cmd = b"f.write(" + repr(part).encode() + b")"
#             exec_raw(cmd)

#         exec_raw(b"f.flush()")
#         exec_raw(b"f.close()")

#         # 回到普通 REPL
#         ser.write(b"\x02")  # Ctrl-B
#         time.sleep(0.2)

#         # 确保写入完成再重启
#         ser.write(b"import machine; machine.reset()\r")
#         time.sleep(0.2)

#         ser.close()
#         print("上传完成，设备已重启。")

#     except Exception as e:
#         print("错误:", e)


@head.add
def 上传boot和依赖():

    上传标志 = False

    def on_change(checked=None):
        nonlocal 上传标志
        上传标志 = True

    but = QPushButton(ez.pub.mw)
    but.setText("上传完整")
    but.clicked.connect(on_change)

    # 创建一个继承自 QThread 的类，并重写 run 方法
    class PortWorker(QThread):
        def __init__(self, parent=None):
            super().__init__(parent)

        def run(self):
            nonlocal 上传标志
            while True:
                time.sleep(0.1)
                if not 上传标志:
                    continue

                try:
                    # 依赖目录
                    path_list = os.path.join(ez.pub.shell项目目录, "mpy")
                    # 依赖目录下的完整文件
                    path_list = tl.dir.get_files_path(path_list, 忽略=None)

                    # 上传到开发板
                    Pyb.增量同步文件(
                        com=ez.pub.com选择框.currentText(),
                        path_list=path_list,
                        分割符="\\mpy",
                    )
                except Exception as e:
                    ez.pub.日志控件.error(f"串口上传文件失败: {e}", ez.pub.日志字体大小)
                else:
                    ez.pub.日志控件.cyan("串口上传文件成功", ez.pub.日志字体大小)
                上传标志 = False

        def stop(self):
            self.terminate()  # 终止线程
            self.wait()  # 等待线程结束
            print("com更新线程结束")

    # 创建线程
    thread = PortWorker(ez.pub.mw)
    thread.start()  # 启动线程
    ez.pub.mw.destroyed.connect(thread.stop)  # 在窗口关闭时停止线程

    return but


@head.add
def 上传boot():

    上传标志 = False

    def on_change(checked=None):
        nonlocal 上传标志
        上传标志 = True

    but = QPushButton(ez.pub.mw)
    but.setText("上传boot")
    but.clicked.connect(on_change)

    # 创建一个继承自 QThread 的类，并重写 run 方法
    class PortWorker(QThread):
        def __init__(self, parent=None):
            super().__init__(parent)

        def run(self):
            nonlocal 上传标志
            while True:
                time.sleep(0.1)
                if not 上传标志:
                    continue

                try:
                    # boot目录
                    path_list_t = os.path.join(ez.pub.shell项目目录, "mpy")
                    # boot目录文件
                    path_list = []
                    path_list.append(os.path.join(path_list_t, "boot.py"))
                    path_list.append(os.path.join(path_list_t, "boot_run.py"))

                    # 上传到开发板
                    Pyb.增量同步文件(
                        com=ez.pub.com选择框.currentText(),
                        path_list=path_list,
                        分割符="\\mpy",
                    )
                except Exception as e:
                    ez.pub.日志控件.error(f"串口上传文件失败: {e}", ez.pub.日志字体大小)
                else:
                    ez.pub.日志控件.cyan("串口上传文件成功", ez.pub.日志字体大小)
                上传标志 = False

        def stop(self):
            self.terminate()  # 终止线程
            self.wait()  # 等待线程结束
            print("com更新boot的线程结束")

    # 创建线程
    thread = PortWorker(ez.pub.mw)
    thread.start()  # 启动线程
    ez.pub.mw.destroyed.connect(thread.stop)  # 在窗口关闭时停止线程

    return but
