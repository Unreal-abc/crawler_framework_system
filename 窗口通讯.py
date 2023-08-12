from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# 创建一个信号类
class Communicate(QObject):
    signal = Signal(str)

# 第一个窗口
class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 1")
        self.button = QPushButton("Send Message", self)
        self.button.clicked.connect(self.send_message)
        self.communicate = Communicate()

    def send_message(self):
        # 发送信号
        window2.communicate.signal.emit("Hello from Window 1!")

# 第二个窗口
class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 2")
        self.communicate = Communicate()
        self.communicate.signal.connect(self.receive_message)

    def receive_message(self, message):
        print("Received message:", message)

# 创建应用程序并显示窗口
app = QApplication([])
window1 = Window1()
window2 = Window2()
window1.show()
window2.show()
app.exec()