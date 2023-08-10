import qdarkstyle
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *


class main_Form():
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('main.ui')


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    window = main_Form()
    window.ui.show()
    app.exec()
