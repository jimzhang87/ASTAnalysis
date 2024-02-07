import json
import os
import random
from utils.getFieldType import get_filed_type, get_key_type

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


# print(project_root)

def find_key_value(dictionary, target_key):

    # results = ''  # 存储匹配结果的列表
    result = None

    if isinstance(dictionary, dict):
        # 遍历字典的每一层
        for key, value in dictionary.items():
            # 如果当前层的键与目标键匹配，则将对应的值添加到结果列表中
            if key == target_key:
                result = value
                return result
            # 如果当前层的值是列表类型，则遍历列表并递归调用该函数继续查找
            elif isinstance(value, list):
                for item in value:
                    sub_results = find_key_value(item, target_key)
                    if sub_results is not None:
                        result = sub_results
                        return result
            # 如果当前层的值是字典类型，则递归调用该函数继续查找
            elif isinstance(value, dict):
                sub_results = find_key_value(value, target_key)
                if sub_results is not None:
                    result = sub_results
                    return result

    return result

def find_field_name_type(dictionary,target_value):
    if isinstance(dictionary, list):
        # 遍历字典的每一层
        for item in dictionary:
            # 如果当前层的键与目标键匹配，则将对应的值添加到结果列表中
            if isinstance(item, dict):
                for key,value in item.items():
                    if value == target_value:
                        return item['field_data_type']
            # 如果当前层的值是列表类型，则遍历列表并递归调用该函数继续查找

def find_key_in_complex_dict(target_key):
    """
    在给定的复杂结构（嵌套字典和字典列表）中查找指定key的内容。

    参数:
    dictionary (dict): 需要在其中查找的复杂结构字典
    target_key (any): 要查找的key

    返回:
    若找到key，则返回对应的value列表；否则返回None
    """
    file_path = '../outputData/packageDetailInfo.json'
    with open(file_path, "r", encoding="utf-8") as f:
        package_detail_info = f.read()
        # package_detail_info = json.loads(package_detail_info)
        package_detail_dict = json.loads(package_detail_info)

    def _find_in_dict_or_list(item):
        print(item)
        if isinstance(item, dict) and target_key in item:
            return item[target_key]
        elif isinstance(item, list):
            found_values = []
            for sub_item in item:
                result = _find_in_dict_or_list(sub_item)
                if result is not None:
                    found_values.append(result)
            if found_values:
                return found_values
        return None

    result = _find_in_dict_or_list(package_detail_dict)
    print(result)
    if isinstance(result, list) and result:
        # 如果找到了多个匹配项，则返回包含所有匹配值的列表
        return result
    elif result is not None:
        # 只找到一个匹配项或没在列表中找到任何匹配项但在字典中找到了
        return [result]
    else:
        # 没有找到任何匹配项
        return None


def generate_data(conditions: dict) -> dict:
    result = {}

    # 处理$block_code_valid_alias
    block_conditions = conditions.get("$block_code_valid_alias")
    if block_conditions:
        # 假设这里我们随机生成一个包含'C163'且不等于'-2'的代码
        valid_codes = ['C163' + str(random.randint(100, 999))]
        filtered_code = next((code for code in valid_codes if '-2' not in code), None)
        result["$block_code_valid_alias"] = filtered_code

    # 处理$cs_kefu_risk_tag
    risk_tag_conditions = conditions.get("$cs_kefu_risk_tag")
    if risk_tag_conditions:
        # 随机生成一个不等于1的整数风险标签
        result["$cs_kefu_risk_tag"] = random.randint(0, 9) if risk_tag_conditions[0]["!="] == [1] else random.randint(0,
                                                                                                                      2)  # 示例中简化为0-2范围

    # 处理$uid
    uid_conditions = conditions.get("$uid")
    if uid_conditions:
        # 确保生成的用户ID在指定范围内
        min_uid = min(uid_conditions[0][">"])  # 获取大于的最小值
        max_uid = max(uid_conditions[1]["<"])  # 获取小于的最大值
        result["$uid"] = random.randint(min_uid, max_uid - 1)  # 随机生成一个在区间内的ID

    return result


def evaluate_condition(condition):
    if isinstance(condition, dict) and len(condition) == 1:
        operator = list(condition.keys())[0]
        values = condition[operator]

        if operator == '!=':
            return random.choice([v for v in range(100) if v not in values])
        elif operator == 'contains':
            value_to_contain = values[0]
            # 对字符串类型字段的操作
            possible_values = [str(random.randint(100, 999)) + value_to_contain for _ in range(10)]
            return next((value for value in possible_values if value_to_contain in value), None)
        elif operator in ['>', '<']:
            # 对于数字类型的字段和范围操作
            min_value, max_value = sorted(values)
            return random.randint(min_value, max_value - 1) if operator == '>' else random.randint(max_value + 1,
                                                                                                   min_value * 2)
        # 其他操作符的处理...

    raise ValueError(f"Unsupported condition: {condition}")


def generate_data_for_field(field_name, conditions):
    result = {}
    print(field_name)
    field_type = get_key_type(field_name)
    if field_type == "string":
        for condition in conditions:
            evaluated_value = evaluate_condition(condition)
            if evaluated_value is not None:
                result[field_name] = evaluated_value
                break  # 假设我们只需要满足一个条件即可，如果有多个条件则可以进行相应修改
    elif field_type == 'list':
        result_list = []
        for condition in conditions:
            evaluated_value = evaluate_condition(condition)
            if evaluated_value is not None:
                result_list.append(evaluated_value)
                break  # 假设我们只需要满足一个条件即可，如果有多个条件则可以进行相应修改
        result[field_name] = result_list

    return result


# 示例使用
with open('../outputData/ruleContent/rule_param_rule_id_1542029.json', "r", encoding="utf-8") as f:
    conditions = json.loads(f.read())
    print(conditions)
# conditions = {
#     "$block_code_valid_alias": [{"!=": [None, "-2"]}, {"contains": "C163"}],
#     "$cs_kefu_risk_tag": [{"!=": [1]}],
#     "$uid": [{">": [0, 5000000]}, {"<": [3000000]}]
# }
# conditions1 = [
#     {"!=": [None, "-2"]},
#     {"contains": "C163"}
# ]
# conditions2 = [{"!=": [1]}]
# uid_conditions = [{">": [0, 5000000]}, {"<": [3000000]}]
# generated_uid_data = generate_data_for_field("$uid", uid_conditions)
# print(generated_uid_data)
# generated_data = generate_data_for_field("$block_code_valid_alias", conditions1)
# generated_data2 = generate_data_for_field("$cs_kefu_risk_tag", conditions2)
# # generated_data = generate_data(conditions)
# print(generated_data)
# print(generated_data2)

if __name__ == '__main__':
    with open('../outputData/ruleContent/rule_param_rule_id_1542029.json', "r", encoding="utf-8") as f:
        conditions = json.loads(f.read())
        print(conditions)
    file_path = '../outputData/packageDetailInfo.json'
    with open(file_path, "r", encoding="utf-8") as f:
        package_detail_info = f.read()
        # package_detail_info = json.loads(package_detail_info)
        package_detail_dict = json.loads(package_detail_info)
        # print(package_detail_dict)
    key = find_key_value(package_detail_dict,'strategy_node_input_field_list')
    field_type = find_field_name_type(key,'uid')
    print(field_type)
