import json
import xml.etree.ElementTree as ET

def json_to_xml(json_data, root_node=None):
    if root_node is None:
        root_node = ET.Element("root")
    for key, value in json_data.items():
        if isinstance(value, dict):
            sub_node = ET.SubElement(root_node, key)
            json_to_xml(value, sub_node)
        elif isinstance(value, list):
            for item in value:
                sub_node = ET.SubElement(root_node, key)
                json_to_xml(item, sub_node)
        else:
            sub_node = ET.SubElement(root_node, key)
            sub_node.text = str(value)
    return root_node

# 示例 JSON 字符串
json_string = '''
{
  "root": {
    "person": [
      {
        "name": "John",
        "age": 30
      },
      {
        "name": "Jane",
        "age": 25
      }
    ]
  }
}
'''

json_data = json.loads(json_string)
root_node = json_to_xml(json_data)
xml_string = ET.tostring(root_node, encoding="utf-8").decode()
print(xml_string)