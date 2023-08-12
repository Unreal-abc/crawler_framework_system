import json
import xml.etree.ElementTree as ET

def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    json_data = {}
    if root.attrib:
        json_data["@attributes"] = root.attrib
    for child in root:
        if child.tag in json_data:
            if isinstance(json_data[child.tag], list):
                json_data[child.tag].append(xml_to_json(ET.tostring(child).decode()))
            else:
                json_data[child.tag] = [json_data[child.tag], xml_to_json(ET.tostring(child).decode())]
        else:
            json_data[child.tag] = xml_to_json(ET.tostring(child).decode())
    return json_data

# 示例 XML 字符串
xml_string = """
<root>
  <person>
    <name>John</name>
    <age>30</age>
  </person>
  <person>
    <name>Jane</name>
    <age>25</age>
  </person>
</root>
"""

json_data = xml_to_json(xml_string)
json_string = json.dumps(json_data, indent=4)
print(json_string)