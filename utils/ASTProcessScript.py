import json
import os
from collections import defaultdict
from utils.backup.interval_process import find_type_logic, extract_intervals, merge_intervals

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


def append_or_create_dict(key, value, my_dict):
    if key in my_dict:
        # 如果key已经存在并且其value不是列表类型，先将其转换为列表
        if not isinstance(my_dict[key], list):
            my_dict[key] = [my_dict[key]]
        # 将新的value添加到列表中
        my_dict[key].append(value)
    else:
        # 如果key不存在，则直接作为普通值添加
        my_dict[key] = value


def get_program_logic_AST(ast_node):
    if ast_node['type'] == 'Program':
        # 对于最外层的 Program 节点，将其作为一个整体的路径
        return ast_node['body']
        # for statement in ast_node['body']:
        #     print(statement)


def get_output_logic_AST(ast_body):
    for statement in ast_body:
        if statement['type'] == 'IfStatement':
            # 对于 if 语句，将其作为一个独立的路径
            # print(statement)
            return statement


def find_type_logic(ast_node, target_type):
    result = []

    def recursive_search(node, parent_type=None, parent_operator=None):
        if isinstance(node, dict):
            if "type" in node:
                # print('----------',node)
                current_type = node["type"]
                if "operator" in node:
                    current_operator = node['operator']
                else:
                    current_operator = None
                if current_type == target_type:
                    result.append({"type": current_type, "parent_type": parent_type,'parent_operator':parent_operator,"logic": node})
                for key, value in node.items():
                    recursive_search(value, current_type,current_operator)

        elif isinstance(node, list):
            for item in node:
                recursive_search(item, parent_type)

    recursive_search(ast_node)
    return result


def if_logic_output_process(if_ast_node):
    consequent = if_ast_node['consequent']
    # print(consequent)
    consequent_body = consequent['body']
    # print(consequent_body)
    for statement in consequent_body:
        if statement['type'] == 'ExpressionStatement':
            expression = statement['expression']
            if expression['type'] == 'CallExpression':
                result_data = expression['arguments'][0]
                if result_data['type'] == 'Literal':
                    value = result_data['value']
            # print(result)
    return value


def binary_process_script(binary_result_list):
    if isinstance(binary_result_list, list):
        logic_dict = {}
        # operator_value_list = []
        for i in binary_result_list:
            # print(i)
            binary_logic = i['logic']
            # logic_dict['parnet_operator'] = i['operator']
            if i['parent_operator'] == '&&':
                operator_value_list = ()
            elif i['parent_operator'] == '||':
                operator_value_list = []
            binary_input_key = binary_logic['left']['name']
            if binary_input_key not in logic_dict:
                operator_value_dict = {}
                # operator_value_list = []
            binary_logic_operator = binary_logic['operator']
            binary_output_value = binary_logic['right']['value']
            if binary_logic_operator in operator_value_dict:
                operator_value_dict[binary_logic_operator].append(binary_output_value)
            else:
                operator_value_dict[binary_logic_operator] = [binary_output_value]

            if binary_input_key in logic_dict:
                # operator_value_list.append(operator_value_dict)
                logic_dict[binary_input_key] = operator_value_dict
            else:
                logic_dict[binary_input_key] = binary_logic_operator
                # operator_value_list.append(operator_value_dict)
                logic_dict[binary_input_key] = operator_value_dict
            print(operator_value_dict)
            # logic_dict[binary_input_key]['value'] = binary_output_key
    print(logic_dict)
    return logic_dict
    # print(logic_dict)
    # print(binary_logic_operator)
    # print(binary_output_key)


def call_process_script(cell_result_list):
    if isinstance(cell_result_list, list):
        logic_dict = {}
        operator_value_list = []
        for i in cell_result_list:
            # print(i)
            if i['parent_type'] == 'LogicalExpression':
                operator_value_dict = {}
                call_logic = i['logic']
                call_input_key = call_logic['arguments'][0]['name']
                if call_input_key not in logic_dict:
                    operator_value_list = []
                call_logic_operator = call_logic['callee']['property']['name']
                call_output_value = call_logic['arguments'][1]['value']
                operator_value_dict[call_logic_operator] = call_output_value
                if call_input_key in logic_dict:
                    operator_value_list.append(operator_value_dict)
                    logic_dict[call_input_key] = operator_value_list
                else:
                    logic_dict[call_input_key] = call_logic_operator
                    operator_value_list.append(operator_value_dict)
                    logic_dict[call_input_key] = operator_value_list
    return logic_dict
    # print(logic_dict)


def merge_dicts(dict1, dict2):
    result_dict = defaultdict(list)

    # 将 dict1 的键值对添加到 result_dict
    for key, value in dict1.items():
        # print(key)
        # print(value)
        if isinstance(value, list):
            result_dict[key] = value
        else:
            result_dict[key].append(value)

    # 将 dict2 的键值对添加到 result_dict
    for key, value in dict2.items():
        # print(key)
        # print(value)
        if isinstance(value, list):
            if key in result_dict:
                result_dict[key].extend(value)
            else:
                result_dict[key] = value
        else:
            result_dict[key].append(value)
    # 将 defaultdict 转换为普通的字典
    final_dict = dict(result_dict)

    return final_dict


if __name__ == '__main__':
    with open('outputData/package_id:2077:rule_id:1542029_test.json', 'r', encoding='utf-8') as f:
        ast = json.loads(f.read())
    logic_result_list = find_type_logic(ast, 'LogicalExpression')
    binary_result_list = find_type_logic(ast, 'BinaryExpression')
    call_result_list = find_type_logic(ast, 'CallExpression')
    binary_logic_dict = binary_process_script(binary_result_list)
    call_logic_dict = call_process_script(call_result_list)
    # print(logic_result_list)
    print(binary_logic_dict)
    # print(call_logic_dict)
    rule_input_logic = merge_dicts(binary_logic_dict, call_logic_dict)
    print(rule_input_logic)
    program_logic_ast = get_program_logic_AST(ast)
    outpit_logic = get_output_logic_AST(program_logic_ast)
    if outpit_logic['type'] == 'IfStatement':
        result_list = if_logic_output_process(outpit_logic)
    with open('outputData/ruleContent/rule_param_rule_id_1542029.json', 'w', encoding='utf-8') as f1:
        data_dict = {}
        data_dict['input'] = rule_input_logic
        data_dict['output'] = result_list
        data = "{'input':%s,'output':'%s'}" % (rule_input_logic, result_list)
        # print(json.dumps(data_dict))
        f1.write(json.dumps(data_dict))
    # print(result_list)
    # print(binary_logic_dict)
    # print(call_logic_dict)
    # print(rule_input_logic)

dict_a = {"logic": {"a": "A", "b": "B"}}
