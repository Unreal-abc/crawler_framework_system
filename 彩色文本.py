from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor

def insert_colored_text(editor, text, color):
    # 获取当前光标
    cursor = editor.textCursor()

    # 创建一个字符格式对象，并设置颜色
    char_format = QTextCharFormat()
    char_format.setForeground(QColor(color))

    # 将字符格式应用于选定的文本
    cursor.setCharFormat(char_format)

    # 在当前光标位置插入文本
    cursor.insertText(text)

# 创建应用程序和主窗口
app = QApplication([])
window = QMainWindow()

# 创建文本编辑器
editor = QTextEdit()
window.setCentralWidget(editor)

# 在文本编辑器中插入彩色文本
insert_colored_text(editor, "Hello, ", "red")
insert_colored_text(editor, "PySide!", "blue")

# 显示主窗口
window.show()
app.exec_()