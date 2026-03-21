
import os.path

from PyQt6.QtWidgets import (
    QComboBox, QMessageBox, QVBoxLayout, QWidget,
    QTextEdit, QPushButton, QFileDialog, QCompleter,
)

import tl.all
import tl.dir
import tl.qt
import os
from PyQt6.QtCore import QTimer, Qt
import ez.config
import ez.pub
from PyQt6.QtGui import QFont, QTextCursor

from tl.qt import head
import sys
from PyQt6.QtWidgets import QApplication
from pathlib import Path
import ui.lib


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
            依赖目录, ["__pycache__", "boot.py", "boot_run.py"])
        # print(file_path)
        for file_name in file_path:
            with open(file_name, "rb") as f:
                file_data = f.read()

            # 相对路径
            file_name = file_name.replace(
                str(依赖目录), "").lstrip("\\/")

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
        file_path = [os.path.join(依赖目录, "boot.py"),
                     os.path.join(依赖目录, "boot_run.py")]
        for file_name in file_path:
            with open(file_name, "rb") as f:
                file_data = f.read()

            # 相对路径
            file_name = file_name.replace(
                str(依赖目录), "").lstrip("\\/")

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
        ez.pub.日志字体默认大小 = int(font_size)

    # 创建下拉框
    combo = QComboBox(ez.pub.mw)
    combo.setMinimumHeight(8)
    for i in range(6, 67):
        combo.addItem(str(i))

    combo.setCurrentText(str(ez.pub.日志字体默认大小))

    combo.activated.connect(on_change)

    return combo
