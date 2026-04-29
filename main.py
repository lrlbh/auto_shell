import ui.log
import 独立任务.init_lr
import ui
import ui.head1
import ui.head2
import ez.pub
import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,

)
from pathlib import Path

import ez.config
import tl.qt as qt
import tl.qt


class MyWindow(QWidget):
    pass
    # def __init__(self):
    #     super().__init__()
    #     # self.setWindowTitle("自动缩放 & UI分离示例")
    #     # self.resize(500, 400)

    # def resizeEvent(self, event):
    #     # 1. 基础字号计算
    #     # 使用窗口高度或宽度的加权平均值通常比单一维度更平滑
    #     base_size = (self.width() + self.height()) // 80
    #     new_font_size = max(12, base_size)  # 稍微调大一点基准，方便观察

    #     for widget in self.findChildren(QWidget):
    #         if widget == self:
    #             continue

    #         # 针对不同控件采取不同的缩放策略
    #         font = widget.font()

    #         # 检查是否为有高度限制的按钮/下拉框
    #         if widget.maximumHeight() < 1000:
    #             # 允许字体稍微“撑满”一点，尝试用 0.6 的比例
    #             limit_size = int(widget.height() * 0.6)
    #             final_size = min(new_font_size, limit_size)
    #             font.setPointSize(max(10, final_size))
    #         else:
    #             # 文本框等控件直接使用计算出的字号
    #             font.setPointSize(new_font_size)

    #         widget.setFont(font)

    #     print(f"窗口当前尺寸: {self.width()}x{self.height()}, 计算字号: {new_font_size}")
    #     super().resizeEvent(event)

# --- 3. 运行部分 ---


if __name__ == "__main__":

    ez.pub.shell项目目录 = Path(__file__).resolve().parent

    独立任务.init_lr.run()

    app = QApplication(sys.argv)

    # 创建主窗口
    ez.pub.mw = MyWindow()

    # 加载头部控件
    tl.qt.head.load()

    # 头部布局
    第一行数 = 4
    head_layout = QHBoxLayout()
    for widget in tl.qt.head.widgets[:第一行数]:
        head_layout.addWidget(widget)
    tl.qt.head.set_font_size(QFont(*ez.config.头部字体和大小))

    head_layout1 = QHBoxLayout()
    for widget in tl.qt.head.widgets[第一行数:]:
        head_layout1.addWidget(widget)
    tl.qt.head.set_font_size(QFont(*ez.config.头部字体和大小))

    # 创建主垂直布局
    main_layout = QVBoxLayout()

    main_layout.addLayout(head_layout, 1)
    main_layout.addLayout(head_layout1, 1)
    main_layout.addWidget(ui.log.日志框(), 20)

    # 加入布局
    ez.pub.mw.setLayout(main_layout)

    # 默认屏幕
    ez.pub.mw.show()
    qt.set_当前屏幕_最下方(ez.config.默认显示器, 1, ez.config.ui高度比例)

    sys.exit(app.exec())


# git branch -M main
# git remote add origin git@github.com:lrlbh/auto_shell.git
# git push -u origin main
# esptool  --port COM14  erase-flash
# esptool --chip ESP32S3 --port COM36 write_flash -z 0x0 c:\Users\82542\code\py\MicroPython\mod\camera_lr\res\00ee9e2--2\ESP32_GENERIC_S3-SPIRAM_OCT-v1.27.0-00ee9e3.bin

# python.analysis.typeCheckingMode