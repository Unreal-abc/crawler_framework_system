# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.labels = []  # 存储标签的数组
#         self.text_edits = []  # 存储长文本编辑框的数组
#
#         self.setWindowTitle("动态创建控件示例")
#         self.create_button = QPushButton("创建")
#         self.create_button.clicked.connect(self.create_label_and_text_edit)
#
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.create_button)
#
#         self.central_widget = QWidget()
#         self.central_widget.setLayout(self.layout)
#         self.setCentralWidget(self.central_widget)
#
#     def create_label_and_text_edit(self):
#         label = QLabel("名称:")
#         text_edit = QTextEdit()
#
#         self.labels.append(label)
#         self.text_edits.append(text_edit)
#
#         self.layout.addWidget(label)
#         self.layout.addWidget(text_edit)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, \
    QWidget, QMessageBox

import xml.etree.ElementTree as ET
import base64


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.line_edits = []  # 存储行编辑框的数组
        self.text_edits = []  # 存储长文本编辑框的数组

        self.setWindowTitle("动态创建控件示例")
        label = QLabel(f"设置名称")
        self.setName = QLineEdit()
        self.create_button = QPushButton("新建脚本")
        self.save = QPushButton("保存脚本")

        self.save.clicked.connect(self.save_to_xml)
        self.create_button.clicked.connect(self.create_label_and_edit)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(self.setName)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.save)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def create_label_and_edit(self):
        SerialNumber = str(len(self.line_edits) + 1)
        label = QLabel(f"设置脚本{SerialNumber}名称:")
        line_edit = QLineEdit()
        text_edit = QTextEdit()

        self.line_edits.append(line_edit)
        self.text_edits.append(text_edit)

        self.layout.addWidget(label)
        self.layout.addWidget(line_edit)
        self.layout.addWidget(text_edit)

    def save_to_xml(self):
        root = ET.Element("data")
        if self.setName.text() == "":
            QMessageBox.information(self,"","请输入内容！")
            return
        for line_edit, text_edit in zip(self.line_edits, self.text_edits):
            title = line_edit.text()
            script = text_edit.toPlainText()
            if title == "" or script == "" or self.setName.text() == "":
                QMessageBox.information(self, "", "请输入内容！")
                return
            script_base64 = base64.b64encode(script.encode()).decode()
            item = ET.SubElement(root, "item")
            title_elem = ET.SubElement(item, "title")
            title_elem.text = title
            script_elem = ET.SubElement(item, "script")
            script_elem.text = script_base64

        tree = ET.ElementTree(root)
        tree.write(self.setName.text() + ".xml")

        print("数据已保存为XML文件。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
