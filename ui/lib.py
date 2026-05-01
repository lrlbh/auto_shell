import time

from PyQt6.QtWidgets import QLabel, QMessageBox

from functools import wraps
import ez.config
import ez.pub

from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap, QColor, QIcon

from PyQt6.QtCore import QThread, QTimer, Qt


def 选择项目没(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检查项目目录是否为空
        if ez.pub.选中的项目目录 == "":
            ez.pub.日志控件.error("没有选择项目", ez.pub.日志字体大小)
            # QMessageBox.information(None, "提示", "没有选择项目，请先选择项目目录")
            return

        return func(*args, **kwargs)

    return wrapper


class 标题更新:
    def __init__(self):

        pixmap = QPixmap(1, 1)
        pixmap.fill(QColor("#00ff00"))
        self.img_ok = QIcon(pixmap)

        pixmap = QPixmap(1, 1)
        pixmap.fill(QColor("#ff0000"))
        self.img_err = QIcon(pixmap)

        pixmap = QPixmap(1, 1)
        pixmap.fill(QColor("#ffff00"))
        self.img_war = QIcon(pixmap)

        # 创建定时器
        timer = QTimer(ez.pub.mw)
        timer.timeout.connect(self.timer_callback)
        timer.setInterval(1000)  # 设置定时器的间隔，单位为毫秒
        timer.start()  # 启动定时器

    # 定时器回调,更新下拉框
    def timer_callback(self):
        if time.time() - ez.pub.单片机心跳 < ez.config.多少秒算掉线:
            ez.pub.mw.setWindowIcon(self.img_ok)
        elif time.time() - ez.pub.最后一次日志时间 < ez.config.多少秒算掉线:
            ez.pub.mw.setWindowIcon(self.img_war)
        else:
            ez.pub.mw.setWindowIcon(self.img_err)

        if ez.pub.单片机心跳 == 0:
            ez.pub.mw.setWindowTitle("更新线程没有连接过")
        else:
            ez.pub.mw.setWindowTitle(
                f"来自: {ez.pub.单片机ip}@{ez.pub.单片机端口}\t"
                f"更新线程上次活跃时间 --> {time.time() - ez.pub.单片机心跳:.2f}秒"
            )
