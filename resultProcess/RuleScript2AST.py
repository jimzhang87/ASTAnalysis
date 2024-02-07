import os
import re

import js2py, json
import matplotlib.pyplot as plt
import esprima
from utils.GetJsonInfo import find_values

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


def node_to_dict(node):
    result = {}
    for key, value in vars(node).items():
        if isinstance(value, list):
            # 对于列表类型的属性（如子节点），递归处理每个元素
            result[key] = [node_to_dict(child) for child in value]
        elif isinstance(value, esprima.nodes.Node):
            # 对于其他 Node 类型的属性，继续递归
            result[key] = node_to_dict(value)
        else:
            # 其他类型（字符串、数字等）直接添加到结果字典中
            result[key] = value
    return result


def crawl_rule_from_package_detail_info(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        package_detail_json = json.load(f)
        # print(package_detail_json)
        package_id = package_detail_json['package_id']
        strategy_node_flow_rule_list = find_values(package_detail_json, 'strategy_node_flow_rule_list')
        # print(strategy_node_flow_rule_list[0])
        for i in strategy_node_flow_rule_list[0]:
            # print(i)
            rule_id = i['rule_id']
            rule_data = i['rule_data']
            rule_content = rule_data['rule_content']
            denpendent_variables_list = rule_data['denpendent_variables']
            rule_field_dict_list = []
            for j in denpendent_variables_list:
                rule_field_dict_list.append(j)
            rule_data = rule_content.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace(
                '\t', '"')
            # rule_data = i.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\t', '"')
            matches = re.findall(r'\{(.*?)}', rule_data)
            # print(matches[0])
            new_rule_data = re.sub(r'\{(.*?)}', '{console.log(\'%s\')}' % matches[0], rule_data)
            tree_json = esprima.parseScript(new_rule_data, {'loc': False})
            tree_dict = node_to_dict(tree_json)
            with open('outputData/package_id:%s:rule_id:%s_test.json' % (package_id, rule_id), 'w',
                      encoding='utf-8') as f:
                for k in json.dumps(tree_dict):
                    f.write(k)
            with open('outputData/package_id:%s:rule_id:%s_field_dict.json' % (package_id, rule_id), 'w',
                      encoding='utf-8') as f:
                for k in json.dumps(rule_field_dict_list):
                    f.write(k)


if __name__ == '__main__':
    crawl_rule_from_package_detail_info('JSDemo.json')
