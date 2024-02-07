import json
import os

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)

with open('outputData/ruleContent/rule_param_rule_id_1542029.json', 'r', encoding='utf-8') as f1:
    rule_content = f1.read()
    # print(rule_content)
with open('outputData/package_id:2077:rule_id:1542029_field_dict.json', 'r', encoding='utf-8') as f2:
    rule_field_list = f2.read()
    # print(rule_field_list)


def data_rebuild(rule_content, rule_field_list):
    rule_content_dict = json.loads(rule_content)
    rule_field_list = json.loads(rule_field_list)
    # print(rule_content_dict)
    input_data_dict = rule_content_dict['input']
    input_field_dict = {}

    for j in rule_field_list:
        # print(j)
        if j['field_type'] == 0:
            field_name = '$' + j['field_name']
            # print(field_name)
            input_field_dict[field_name] = input_data_dict[field_name]
            # print(input_field_dict)
    return input_field_dict


if __name__ == '__main__':
    input_field_dict = data_rebuild(rule_content, rule_field_list)
    print(input_field_dict)
