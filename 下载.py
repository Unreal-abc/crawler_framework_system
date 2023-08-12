import qdarkstyle
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtWebEngineWidgets import *


class MainWindow():
    taskName = ""
    numberOfThreads = 0
    listOfTasksToBeAssigned = []
    taskList = []

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('通用爬虫.ui')
        self.readConfigurationItems()
        self.ui.setWindowTitle("WebEngine Download Example")
        self.ui.resize(800, 600)

    def run_script(self):
        self.web_view.page().runJavaScript(self.text_edit.toPlainText())

    def readConfigurationItems(self):
        import xml.etree.ElementTree as ET
        tree = ET.parse('task.xml')
        root = tree.getroot()
        ############################
        taskName = root.find('taskName')
        if taskName is not None:
            self.taskName = taskName.text.strip()
            self.ui.taskName.setText(self.taskName)
        else:
            QApplication.quit()
        ############################
        numberOfThreads = root.find('numberOfThreads')
        if numberOfThreads is not None:
            self.numberOfThreads = numberOfThreads.text.strip()
            self.ui.numberOfThreads.setText(self.numberOfThreads)
        else:
            QApplication.quit()
        ############################
        taskScript = root.find('taskScript')
        if taskScript is not None:
            self.taskScript = taskScript.text.strip()
            self.ui.script.setText(self.taskScript)
        else:
            QApplication.quit()
        ############################
        elements = root.find('taskURLs').findall("url")
        if elements is None:
            QApplication.quit()
        index = 1
        for element in elements:
            if 'status' not in element.attrib:
                # 如果不存在status属性，则添加
                element.set('status', "1")
            if element.get('status') == "1":
                self.listOfTasksToBeAssigned.append({
                    "id": index,
                    "url": element.text.strip()
                })
            index = index + 1
        tree.write('task.xml')
        print(self.listOfTasksToBeAssigned)

    def assignTasks(self):
        for i in range(self.numberOfThreads):
            self.taskList.append(set())


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    window = MainWindow()
    window.ui.show()
    app.exec()
