from lxml import etree

# 解析XML文档
tree = etree.parse('task.xml')
root = tree.getroot()

# 使用XPath定位元素
elements = tree.xpath('/task/taskURLs')

# 遍历匹配的元素
for element in elements:
    # 处理匹配的元素
    print("-------")
    print(element.text)