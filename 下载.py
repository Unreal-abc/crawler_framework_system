import queue
import threading

import qdarkstyle
from PySide6.QtCore import *
from PySide6.QtUiTools import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *


class ThreadManager(QObject):
    load_url_signal = Signal(list)

    def __init__(self, num_threads):
        QObject.__init__(self)
        self.status = {}
        self.num_threads = num_threads
        self.threads = []
        self.webviews = []
        self.tasks = []
        self.threadStartFlag = True
        self.isTaskCompleted_Queue = queue.Queue()

    def stopRunning(self):
        self.threadStartFlag = False
        for item in self.threads:
            try:
                with item:
                    item.notify()
            except:
                pass

    def join_threads(self):
        for thread in self.threads:
            thread.join()

    def start_threads(self):
        self.threadStartFlag = True
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.thread_function, args=(i,))
            self.threads.append(thread)
            thread.start()

    def thread_function(self, thread_id):
        webview = self.webviews[thread_id]
        self.status[thread_id] = {
            "targetURL": "",
            "pageNumber": "",
            "status": "",
            "data": "",
            "loadFinished_is_connected": False,  # 判断信号是否连接
            "condition": threading.Condition(),
            # "isTaskCompleted": False  # 是否任务完成
        }
        task = self.tasks[thread_id]
        self.isTaskCompleted_Queue.put(False)
        condition = self.status[thread_id]["condition"]  # 要实现唤醒指定的thread1线程而不唤醒thread2线程，可以使用条件变量（Condition）来实现
        with condition:
            while self.threadStartFlag:
                if not task.empty():
                    item = task.get()
                    self.status[thread_id]["data"] = item  # 复制一份
                    targetURL = item["targetURL"]
                    self.status[thread_id]["targetURL"] = targetURL
                    pageNumber = int(item["pageNumber"])  # 获取页码设置状态
                    self.status[thread_id]["pageNumber"] = pageNumber
                    ClassManager().DetailedDataCollectionForNewDevelopments.TableStatus.updateStatus(row=pageNumber,
                                                                                                     status=2)
                    self.load_url_signal.emit([webview, QUrl(targetURL), thread_id])  # 发送信号
                    condition.wait()
                    # break
                else:
                    break

    def callbackFunction_thread_function(self, thread_id):  # 网站加载完毕后执行
        self.webviews[thread_id].page().runJavaScript(jsCode.GetDetailedInformationCode, 0, lambda
            result: self.callbackFunction_read_the_data_for_this_page(result, thread_id))

    def load_url(self, data):
        webview, url, thread_id = data[0], data[1], data[2]
        webview.load(url)
        if not self.status[thread_id]["loadFinished_is_connected"]:  # 避免重复绑定
            self.status[thread_id]["loadFinished_is_connected"] = True
            webview.loadFinished.connect(lambda: self.callbackFunction_thread_function(thread_id))

    def callbackFunction_read_the_data_for_this_page(self, result, thread_id):  # JS执行完毕后执行
        ui = ClassManager().ui
        pageNumber = int(self.status[thread_id]["pageNumber"])
        try:
            data = json.loads(result)
        except:
            ClassManager().DetailedDataCollectionForNewDevelopments.TableStatus.updateStatus(row=pageNumber,
                                                                                             status=4)  # 更新状态
            with self.status[thread_id]["condition"]:
                self.status[thread_id]["condition"].notify()  # 唤醒线程

            if self.tasks[thread_id].empty():
                # print("线程ID ", thread_id, "DONE++++")
                self.isTaskCompleted_Queue.get()
                if self.isTaskCompleted_Queue.empty():
                    ui = ClassManager().ui
                    QMessageBox.information(ui, '提示', "任务全部完成！")
                    stop_automation_detailedDataModule(False)
                else:
                    return
            return

        # print(data)

        db = SQLiteHelper("db/database.db")
        # print("_________正在写入数据库___________")
        processedDataID = self.status[thread_id]["data"]["dataID"]
        key_list = list(data.keys())
        # print(key_list)
        key_list.remove("周边规划：")
        tempList = []
        detailedDataTableID = str(uuid.uuid4())
        # print(data)
        tempList.append(detailedDataTableID)
        tempList.append(processedDataID)
        tempList.append(data.get("物业类型：", "null"))
        tempList.append(data.get("参考价格：", "null"))

        tempList.append(data.get("项目特色：", "null"))
        tempList.append(data.get("区域位置：", "null"))
        tempList.append(data.get("楼盘地址：", "null"))
        tempList.append(data.get("售楼处地址：", "null"))

        tempList.append(data.get("开发商：", "null"))
        tempList.append(data.get("建筑类型：", "null"))
        tempList.append(data.get("绿化率：", "null"))
        tempList.append(data.get("占地面积：", "null"))
        tempList.append(data.get("容积率：", "null"))
        tempList.append(data.get("建筑面积：", "null"))
        tempList.append(data.get("规划户数：", "null"))
        tempList.append(data.get("产权年限：", "null"))

        tempList.append(data.get("楼盘户型：", "null"))
        tempList.append(data.get("最近交房：", "null"))
        tempList.append(data.get("物业公司：", "null"))
        tempList.append(data.get("车位配比：", "null"))
        tempList.append(data.get("物业费：", "null"))
        tempList.append(data.get("供暖方式：", "null"))
        tempList.append(data.get("供水方式：", "null"))
        tempList.append(data.get("供电方式：", "null"))
        tempList.append(data.get("车位：", "null"))

        surroundingPlanning = data["周边规划："]

        tempList.append(surroundingPlanning.get("地铁", "null"))
        tempList.append(surroundingPlanning.get("教育设施", "null"))
        tempList.append(surroundingPlanning.get("医院", "null"))
        tempList.append(surroundingPlanning.get("购物", "null"))
        tempList.append(surroundingPlanning.get("公园", "null"))
        tempList.append(surroundingPlanning.get("其他", "null"))
        db.insert("detailedDataTable",
                  [
                      "id", "processedDataID", "物业类型", "参考价格", "项目特色", "区域位置", "楼盘地址", "售楼处地址",
                      "开发商", "建筑类型", "绿化率", "占地面积", "容积率", "建筑面积", "规划户数", "产权年限",
                      "楼盘户型", "最近交房", "物业公司", "车位配比", "物业费", "供暖方式", "供水方式", "供电方式",
                      "车位", "地铁", "教育设施", "医院", "购物", "公园", "其他"
                  ], [tuple(tempList)])
        db.update("processedData", {"detailedDataTableID": detailedDataTableID}, {"id": processedDataID})
        db.close()
        ClassManager().DetailedDataCollectionForNewDevelopments.TableStatus.updateStatus(row=pageNumber,
                                                                                         status=3)  # 更新状态
        with self.status[thread_id]["condition"]:
            self.status[thread_id]["condition"].notify()  # 唤醒线程

        if self.tasks[thread_id].empty():
            # print("线程ID ", thread_id, "DONE++++")
            self.isTaskCompleted_Queue.get()
            if self.isTaskCompleted_Queue.empty():
                ui = ClassManager().ui
                QMessageBox.information(ui, '提示', "任务全部完成！")
                stop_automation_detailedDataModule(False)
            else:
                return


class MainWindow():
    xml_file_name = "task.xml"
    taskName = ""
    numberOfThreads = 0
    listOfTasksToBeAssigned = []
    taskList = []

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('通用爬虫.ui')
        self.ThreadManager = ThreadManager()
        self.readConfigurationItems()
        self.assignTasks()
        self.initialize_qwebengineview_component()
        self.ui.setWindowTitle("WebEngine Download Example")
        self.ui.resize(800, 600)

    def run_script(self):
        self.web_view.page().runJavaScript(self.text_edit.toPlainText())

    def readConfigurationItems(self):  # 读取配置项
        import xml.etree.ElementTree as ET
        self.tree = ET.parse(self.xml_file_name)
        root = self.tree.getroot()
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
            self.numberOfThreads = int(numberOfThreads.text.strip())
            self.ui.numberOfThreads.setText(str(self.numberOfThreads))
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
        index = 0
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
        self.tree.write(self.xml_file_name)
        print(self.listOfTasksToBeAssigned)

    def assignTasks(self):
        # 分配任务
        for i in range(self.numberOfThreads):
            self.taskList.append(queue.Queue())
        index = 0
        for item in self.listOfTasksToBeAssigned:
            if index % self.numberOfThreads == 0:
                index = 0
            self.taskList[index].put(item)
            index = index + 1

    def updateTaskStatus(self, id, status):
        # 更新任务
        root = self.tree.getroot()
        elements = root.find('taskURLs').findall("url")
        elements[int(id)].set('status', str(status))

    def saveXML(self):
        # 保存文件
        self.tree.write(self.xml_file_name)

    def initialize_qwebengineview_component(self):
        # 初始化QwebengineView组件
        for i in range(self.numberOfThreads):
            webview = QWebEngineView()
            webview.setZoomFactor(0.25)  # 设置浏览器的缩放
            self.ThreadManager.webviews.append(webview)  # 将新建的浏览器组件放入线程管理类中
            row = i // 4  # 计算行数
            col = i % 4  # 计算列数
            self.ui.gridLayout.addWidget(webview, row, col)
        pass


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
    window = MainWindow()
    window.ui.show()
    app.exec()
