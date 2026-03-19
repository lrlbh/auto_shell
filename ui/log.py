
from PyQt6.QtWidgets import (
    QComboBox, QVBoxLayout, QWidget,
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


import sys
from PyQt6.QtWidgets import QApplication


# def 日志框():
#     # 假设 ez.pub.mw 是你的主窗口实例
#     text_edit = QTextEdit(ez.pub.mw)
#     text_edit.setText("日志已启动...\n")

#     # --- 定时器逻辑开始 ---

#     def 更新日志():
#         # 将列表 z 中的所有内容合并为字符串显示
#         # 如果你只想显示新增内容，可以根据索引处理
#         while len(ez.pub.log):
#             msg = ez.pub.log.pop(0)
#             if msg.startswith("warning_lr"):
#                 _, msg = msg.split(" ", 1)
#                 msg = f"<span style='color: orange;'>⚠️ {tl.all.time_str()+msg}</span>"
#             elif msg.startswith("error_lr"):
#                 _, msg = msg.split(" ", 1)
#                 msg = f"<span style='color: red;'>❌ {tl.all.time_str()+msg}</span>"
#             else:
#                 msg = f"<span style='color: white;'> {tl.all.time_str()+msg}</span>"

#             text_edit.append(msg)

#             # if text_edit.verticalScrollBar().value() == text_edit.verticalScrollBar().maximum():
#             #     text_edit.moveCursor(QTextCursor.MoveOperation.End)

#     # 创建定时器
#     timer = QTimer(text_edit)  # 将 text_edit 设为父对象，随窗口销毁
#     timer.timeout.connect(更新日志)
#     timer.start(1000)  # 每隔 1000 毫秒（1秒）执行一次

#     return text_edit


def 日志框():
    ez.pub.日志控件 = tl.qt.log_widget(ez.pub.mw)

    return ez.pub.日志控件
