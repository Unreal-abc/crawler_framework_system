import xml.etree.ElementTree as ET
tree = ET.parse('task.xml')
root = tree.getroot()
element = root.find('taskName')
if element is not None:
    value = element.text.strip()
    print("Value:", value)
else:
    QApplication.quit()
# 根据标签名查找多个元素并获取其值
elements = root.find('taskURLs').findall("url")
for element in elements:
    value = element.text.strip()
    print("Value:", value)