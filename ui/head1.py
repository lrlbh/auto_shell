import os.path
import keyboard
import struct

from PyQt6.QtWidgets import (
    QComboBox,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QCompleter,
)

import tl.all
import tl.dir
import tl.qt
import os
from PyQt6.QtCore import QObject, QTimer, Qt, pyqtSignal
import ez.config
import ez.pub
from PyQt6.QtGui import QFont, QTextCursor


import sys
from PyQt6.QtWidgets import QApplication
from tl.qt import head
import ui.lib


@head.add
def 选择项目目录():
    def on_change():
        directory = QFileDialog.getExistingDirectory(
            None,  # 父窗口对象
            "选择目录",  # 对话框标题
            ez.config.选择项目默认路径,  # 默认打开的路径
            QFileDialog.Option.ShowDirsOnly
            | QFileDialog.Option.DontUseNativeDialog,  # 不卡
            # QFileDialog.Option.ShowDirsOnly,  # 选项：只显示目录 卡
        )

        if directory:
            # 修改按钮名称
            but.setText(os.path.basename(directory))
            ez.pub.选中的项目目录 = directory

    # 创建下拉框
    but = QPushButton(ez.pub.mw)
    but.setText("选择项目")

    # 添加选项
    but.clicked.connect(on_change)

    return but


@head.add
def 运行():

    @ui.lib.选择项目没
    def on_change(checked=None):
        # 获取需要忽略的文件和目录
        try:
            t_mod = tl.dir.import_path(
                os.path.join(ez.pub.选中的项目目录, "boot_run.py")
            )
            忽略列表 = t_mod.忽略的文件和目录
        except:  # noqa: E722
            忽略列表 = []

        local_md5 = tl.dir.get_files_md5(ez.pub.选中的项目目录, 忽略列表)

        新增文件 = [k for k in local_md5 if k not in ez.pub.cli_ip]
        修改文件 = [
            k
            for k in local_md5.keys() & ez.pub.cli_ip.keys()
            if local_md5[k] != ez.pub.cli_ip[k]
        ]

        需要更新文件 = 新增文件 + 修改文件

        # 显示完整文件处理 --> 忽略的、相同的、新增的、修改的
        # for file in [
        #     k for k in tl.dir.get_files_md5(ez.pub.选中的项目目录) if k not in local_md5
        # ]:
        #     ez.pub.日志控件.cyan(f"忽略文件 -> {file}", ez.pub.日志字体默认大小)

        # for file in [k for k in local_md5 if k not in 修改文件]:
        #     ez.pub.日志控件.cyan(f"相同文件 -> {file}", ez.pub.日志字体默认大小)

        # for file in 新增文件:
        #     ez.pub.日志控件.cyan(f"新增文件 -> {file}", ez.pub.日志字体默认大小)

        # for file in 修改文件:
        #     ez.pub.日志控件.cyan(f"修改文件 -> {file}", ez.pub.日志字体默认大小)

        tmep_data = struct.pack(">I", len(需要更新文件))

        for file in 需要更新文件:
            with open(os.path.join(ez.pub.选中的项目目录, file.lstrip("/")), "rb") as f:
                content = f.read()

            item_header = struct.pack(">I", len(file.encode())) + file.encode()
            item_body = struct.pack(">I", len(content)) + content

            tmep_data += item_header + item_body

        # 4. 保存到目标变量
        ez.pub.send_msg = tmep_data

    # 创建按键
    but = QPushButton(ez.pub.mw)
    but.setText("run(f2)")
    but.clicked.connect(on_change)

    # 注册快捷键
    class Bridge(QObject):
        trigger = pyqtSignal()

    bridge = Bridge()
    bridge.trigger.connect(on_change)
    keyboard.add_hotkey("F2", lambda: bridge.trigger.emit())

    return but


@head.add
def 选择文件():
    old_file = None
    old_size = 0

    # 定义统一的事件处理函数
    def on_content_changed(text):

        # 建议优化：如果列表很大，频繁 itemText(i) 会慢，可以考虑从 ez.pub 中直接取列表
        valid_list = [combo.itemText(i) for i in range(combo.count())]

        if text in valid_list:
            # 3. 匹配成功：直接传空字符串，恢复系统原生样式
            combo.setStyleSheet("")
        else:
            # 4. 匹配失败：只设置必要的红色边框和淡红背景
            combo.setStyleSheet("""
                QComboBox {

                    background-color: #804040;
                }
            """)

    def 更新输入框内容():
        nonlocal old_file, old_size
        if old_file == ez.pub.cli_ip and old_size == ez.pub.文件输入框.font():
            return

        # 文件添加到选择框
        ez.pub.文件输入框.clear()
        if ez.pub.cli_ip is None:
            return

        # keys排序 深度优先排序 (按路径层级)
        ret = sorted(ez.pub.cli_ip.keys(), key=lambda x: (x.count("/"), x.lower()))
        ez.pub.文件输入框.addItems(ret)

        # 选择款加入智能提示
        completer = QCompleter(ret)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # MatchContains 表示包含即可匹配，
        # MatchStartsWith 表示必须以输入开头
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.popup().setFont(ez.pub.文件输入框.font())
        ez.pub.文件输入框.setCompleter(completer)
        old_file = ez.pub.cli_ip
        old_size = ez.pub.文件输入框.font()

        # 触发一下重新布局
        ez.config.头部字体和大小[1] += 1
        head.set_font_size(QFont(*ez.config.头部字体和大小))
        ez.config.头部字体和大小[1] -= 1
        head.set_font_size(QFont(*ez.config.头部字体和大小))

    # 1. 创建 QComboBox
    combo = QComboBox(ez.pub.mw)
    ez.pub.文件输入框 = combo
    combo.setEditable(True)
    combo.setMinimumHeight(8)

    # 2. 监控：编辑框文本改变 (打字时触发)
    combo.editTextChanged.connect(on_content_changed)

    # 创建定时器
    timer = QTimer(combo)  # 将 text_edit 设为父对象，随窗口销毁
    timer.timeout.connect(更新输入框内容)
    timer.start(1000)  # 每隔 1000 毫秒（1秒）执行一次

    return combo


@head.add
def 删除():
    def on_change():
        pass

    but = QPushButton(ez.pub.mw)
    but.setText("删除")
    but.clicked.connect(on_change)

    return but


# @head.add
# def 选择设备():
#     def on_change(index):
#         # 1. 直接通过当前索引获取绑定的 Data (即屏幕["index"])
#         current_id = combo.itemData(index)
#         # print(f"id = {current_id}")
#         tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)
#         tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)
#         tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)
#         tl.qt.set_当前屏幕_最下方(current_id, 1, ez.config.ui高度比例)

#     # 创建下拉框
#     combo = QComboBox(ez.pub.mw)

#     # 添加选项
#     for 屏幕 in tl.qt.get_屏幕列表():
#         combo.addItem(屏幕["name"], 屏幕["index"])
#         print(屏幕["index"])
#         print(屏幕["name"])

#     combo.activated.connect(on_change)

#     return combo


# @head.add
# def 单文件运行():
#     def on_change():
#         pass

#     but = QPushButton(ez.pub.mw)
#     but.setText("单文件运行")
#     but.clicked.connect(on_change)

#     return but
