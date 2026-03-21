import sys
import pprint
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QGuiApplication, QColor, QFont
from PySide6.QtCore import Qt, QTimer

# --- 你提供的核心逻辑 (已适配 PySide6 导入) ---

def get_逻辑像素(index):
    screens = QApplication.screens()
    if 0 <= index < len(screens):
        target_screen = screens[index]
        rect = target_screen.geometry()
        return rect.width(), rect.height()
    return None

def get_屏幕列表():
    screens = QGuiApplication.screens()
    monitor_list = []
    for index, screen in enumerate(screens):
        info = {
            "index": index,
            "name": screen.name(),
            "resolution": f"{screen.size().width()}x{screen.size().height()}",
            "is_primary": screen == QGuiApplication.primaryScreen(),
            "device_pixel_ratio": screen.devicePixelRatio()
        }
        monitor_list.append(info)
    return monitor_list

def set_当前屏幕_最下方(screen_index, w_ratio, h_ratio):
    """
    w_ratio, h_ratio: 屏幕宽高的比例 (0.0 到 1.0)
    """
    main_widget = None
    for widget in QApplication.topLevelWidgets():
        if widget.isWindow() and widget.isVisible():
            main_widget = widget
            break

    if not main_widget:
        return

    screens = QGuiApplication.screens()
    if 0 <= screen_index < len(screens):
        screen = screens[screen_index]
        rect = screen.availableGeometry()

        # 计算目标大小 (基于逻辑像素)
        tw, th = get_逻辑像素(screen_index)
        target_w = int(w_ratio * tw)
        target_h = int(h_ratio * th)

        # 核心修正步骤
        main_widget.resize(target_w, target_h)
        main_widget.move(rect.topLeft())
        
        QApplication.processEvents()

        x = rect.left() + (rect.width() - main_widget.frameSize().width()) // 2 # 居中对齐
        y = rect.bottom() - main_widget.frameSize().height() + 1

        main_widget.move(x, y)
        main_widget.show()
        main_widget.raise_()
        print(f"已将窗口移动到屏幕 [{screen_index}]: {screen.name()}")

# --- 测试 UI 类 ---

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 屏幕测试")
        self.setStyleSheet("background-color: #2c3e50; border: 2px solid #3498db;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.label = QLabel("正在检测屏幕...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        layout.addWidget(self.label)

# --- 主程序 ---

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. 打印屏幕信息
    print("--- 当前检测到的屏幕列表 ---")
    monitors = get_屏幕列表()
    pprint.pprint(monitors)
    
    # 2. 创建并显示窗口
    window = TestWindow()
    window.show()
    
    # 3. 动态测试：循环切换屏幕
    # 我们用一个计时器，每 3 秒换一个屏幕显示
    current_test_index = 0
    
    def auto_move():
        global current_test_index
        if not monitors: return
        
        idx = current_test_index % len(monitors)
        window.label.setText(f"当前屏幕: {monitors[idx]['name']}\n缩放倍率: {monitors[idx]['device_pixel_ratio']}")
        
        # 调用你的核心函数 (设置为屏幕宽度的 80%，高度的 15%)
        set_当前屏幕_最下方(idx, 0.8, 0.15)
        
        current_test_index += 1

    timer = QTimer()
    timer.timeout.connect(auto_move)
    timer.start(3000) # 每 3 秒切换一次屏幕
    
    auto_move() # 立即执行第一次
    
    sys.exit(app.exec())