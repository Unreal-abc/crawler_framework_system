from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建文本编辑框和执行按钮
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('在这里输入JavaScript...')
        self.run_button = QPushButton("Run Script")
        self.run_button.clicked.connect(self.run_script)

        # 创建布局并添加部件
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.run_button)

        # 创建主窗口部件，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 创建QWebEngineView并加载网页
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.web_view.load(QUrl("https://www.thepaper.cn/channel_25950"))

        # 连接下载请求信号
        self.web_view.page().profile().downloadRequested.connect(self.on_download_requested)

        # 设置主窗口标题和尺寸
        self.setWindowTitle("WebEngine Download Example")
        self.resize(800, 600)

    def run_script(self):
        # 获取文本编辑器的内容
        script = self.text_edit.toPlainText()

        # 在QWebEngineView中执行JavaScript代码
        self.web_view.page().runJavaScript(script)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
