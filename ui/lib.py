
from PyQt6.QtWidgets import QMessageBox

from functools import wraps
import ez.pub


def 选择项目没(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检查项目目录是否为空
        if ez.pub.选中的项目目录 == "":
            QMessageBox.information(None, "提示", "没有选择项目，请先选择项目目录")
            return

        return func(*args, **kwargs)

    return wrapper
