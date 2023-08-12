import qdarkstyle
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit


class mainForm():
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('removingElements.ui')
        self.line_edits = []  # 用于存储创建的LineEdit

        self.ui.add_button.clicked.connect(self.add_line_edit)
        self.ui.generate_button.clicked.connect(self.generate_script)

        self.ui.copy.clicked.connect(self.copy_clicked)

    def add_line_edit(self):
        line_edit = QLineEdit()
        self.line_edits.append(line_edit)
        # self.ui.widget.setMinimumHeight(200)
        self.ui.verticalLayout_2.addWidget(line_edit)

    def generate_script(self):
        script_ = ""
        for line_edit in self.line_edits:
            line_edit_text = line_edit.text()
            if line_edit_text:
                script_ += f'if (className.includes("{line_edit_text}")) {{\n'
                script_ += '    element.remove();\n'
                script_ += '    continue;\n'
                script_ += '}'
        script = """
function traverseToRemoveElements(element) {
// 检查类名是否包含 "index_content"
    for (const className of element.classList) {
""" + script_ + """
    }
    const children = element.children;
    for (let i = 0; i < children.length; i++) {
        traverseToRemoveElements(children[i]);
    }
}

// 启动遍历，从根元素开始
traverseToRemoveElements(document.documentElement);
        """
        self.ui.script_text_edit.setPlainText(script)

    def copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.script_text_edit.toPlainText())
        pass


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
window = mainForm()
window.ui.show()
app.exec()
