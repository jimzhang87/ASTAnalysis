import json
import os
import logging
import pandas as pd

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


# json_data = pd.read_json('outputData/packageDetailInfo.json', encoding='utf-8')
# print(json_data.keys())


def find_keys(json_obj, path=""):
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            new_path = f"{path}.{k}" if path else k
            print(new_path)
            find_keys(v, new_path)
    elif isinstance(json_obj, list):
        for i, v in enumerate(json_obj):
            new_path = f"{path}[{i}]"
            find_keys(v, new_path)


# with open('outputData/packageDetailInfo.json', 'r', encoding='utf-8') as f:
#     json_data = json.load(f)

# find_keys(json_data)


def find_value(json_obj, target_key):
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == target_key:
                return v
            if isinstance(v, (dict, list)):
                result = find_value(v, target_key)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_value(item, target_key)
            if result is not None:
                return result
    return None


def find_values(json_obj, target_key):
    results = []
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == target_key:
                results.append(v)
            if isinstance(v, (dict, list)):
                results.extend(find_values(v, target_key))
    elif isinstance(json_obj, list):
        for item in json_obj:
            results.extend(find_values(item, target_key))
    return results


def find_parent_values(json_obj, target_key):
    results = []
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == target_key:
                results.append(json_obj)
            elif isinstance(v, (dict, list)):
                results.extend(find_parent_values(v, target_key))
    elif isinstance(json_obj, list):
        for item in json_obj:
            results.extend(find_parent_values(item, target_key))
    return results

def find_and_print(data, target_key, target_value):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key and value == target_value:
                # 如果找到符合条件的键值对，则打印整个键所在的层级的数据
                print("Found matching key-value pair:")
                print(data)
                break
            else:
                # 递归处理嵌套的字典
                find_and_print(value, target_key, target_value)
    elif isinstance(data, list):
        # 递归处理嵌套的列表
        for item in data:
            find_and_print(item, target_key, target_value)
# 使用方法
# import json
if __name__ == '__main__':
    with open('outputData/rule_id:1542029.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # print(data)

    find_and_print(data, 'type','LogicalExpression')
    # value_list = find_parent_values(data, 'type')
# value = find_value(data, 'strategy_node_flow_rule_list')
# parent_value_list = find_parent_values(data, 'rule_content')
#     print(value_list)

# class GetJsonInfo:
#     def __init__(self):
#         pass
#
#     def open_json_file(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             package_data = json.load(f)
#         return package_data
#
#     def get_package_edition_list(package_detail_info):
#         if package_detail_info:
#             try:
#                 package_edition_list = package_detail_info['package_edition_list']
#                 return package_edition_list
#             except KeyError as e:
#                 logging.error(f'package_detail_info has no package_edition_list key {e}')
#         else:
#             logging.error('package_detail_info is None')
#
#     def get_online_edition_detail_info(package_edition_list):
#         if package_edition_list:
#             for edition in package_edition_list:
#                 if edition['edition_type'] == 2:
#                     return edition
#         else:
#             logging.error('package_edition_list is None')
#
#     def get_edition_strategy_node_info_list(edition_detail_info):
#         if edition_detail_info:
#             try:
#                 edition_strategy_node_info_list = edition_detail_info['edition_strategy_node_info_list']
#                 return edition_strategy_node_info_list
#             except KeyError as e:
#                 logging.error(f'edition_detail_info has no edition_strategy_node_info_list key {e}')
#
#     def get_edition_strategy_edge_info_list(edition_detail_info):
#         if edition_detail_info:
#             try:
#                 edition_strategy_edge_info_list = edition_detail_info['edition_strategy_edge_info_list']
#                 return edition_strategy_edge_info_list
#             except KeyError as e:
#                 logging.error(f'edition_detail_info has no edition_strategy_edge_info_list key {e}')
#
#     def get_strategy_node_flowchart_policy_node_list(strategy_node_info_list):
#         if strategy_node_info_list:
#             try:
#                 strategy_node_flow_list = strategy_node_info_list['strategy_node_flow_list']
#                 return strategy_node_flow_list
#             except KeyError as e:
#                 logging.error(f'edition_detail_info has no edition_strategy_edge_info_list key {e}')
#         else:
#             return 'strategy_node_flow_list is None'
#
#     def get_strategy_node_input_field_list(strategy_node_flow_list):
#         if strategy_node_flow_list:
#             return strategy_node_flow_list['strategy_node_input_field_list']
#         else:
#             return 'strategy_node_input_field_list is None'
#
#     def get_strategy_node_output_field_list(strategy_node_flow_list):
#         if strategy_node_flow_list:
#             return strategy_node_flow_list['strategy_node_output_field_list']
#         else:
#             return 'strategy_node_output_field_list is None'
#
#     def get_strategy_node_medium_field_list(strategy_node_flow_list):
#         if strategy_node_flow_list:
#             return strategy_node_flow_list['strategy_node_medium_field_list']
#         else:
#             return 'strategy_node_medium_field_list is None'
#
#     def get_strategy_node_flow_rule_list(strategy_node_flow_list):
#         if strategy_node_flow_list:
#             return strategy_node_flow_list['strategy_node_flow_rule_list']
#         else:
#             return 'strategy_node_flow_rule_list is None'


# data = open_json_file('outputData/packageDetailInfo.json')

# print(data)
# rule_content = get_package_edition_list(data)
# print(rule_content)
