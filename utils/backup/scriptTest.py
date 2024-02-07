import io
import itertools
import os.path
import re
import difflib
from difflib import SequenceMatcher

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)

filename = 'outputData/packageDetailInfo.json'


# script = "!UnFunction.includes($uid_mark_codes.split(\",\"),\"UTB27\")"

# 使用正则表达式匹配需要替换的部分
# pattern = r"!UnFunction.includes\(\$uid_mark_codes\.split\(\"(.*?)\"\),\"(.*?)\"\)"
# match = re.search(pattern, script)
def read_rule_content(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        content_dict = eval(content.replace('false', 'False'))
    return content_dict
    # print(content.replace('false', 'False'))
    # print('a', eval(content.replace('false', 'False')))
    # print(type(content_dict))
    # print(content_dict)


def find_key_first(dictionary, target_key):
    # 遍历字典的每一层
    for key, value in dictionary.items():
        # 如果当前层的键与目标键匹配，则返回对应的值
        if key == target_key:
            return value
        # 如果当前层的值是列表类型，则遍历列表并递归调用该函数继续查找
        elif isinstance(value, list):
            for item in value:
                result = find_key_first(item, target_key)
                if result is not None:
                    return result
        # 如果当前层的值是字典类型，则递归调用该函数继续查找
        elif isinstance(value, dict):
            result = find_key_first(value, target_key)
            if result is not None:
                return result
    # 如果没有找到目标键，则返回None
    return None


def find_key_list(dictionary, target_key):
    results = []  # 存储匹配结果的列表

    if isinstance(dictionary, dict):
        # 遍历字典的每一层
        for key, value in dictionary.items():
            # 如果当前层的键与目标键匹配，则将对应的值添加到结果列表中
            if key == target_key:
                results.append(value)
            # 如果当前层的值是列表类型，则遍历列表并递归调用该函数继续查找
            elif isinstance(value, list):
                for item in value:
                    sub_results = find_key_list(item, target_key)
                    results.extend(sub_results)  # 将子结果添加到结果列表中
            # 如果当前层的值是字典类型，则递归调用该函数继续查找
            elif isinstance(value, dict):
                sub_results = find_key_list(value, target_key)
                results.extend(sub_results)  # 将子结果添加到结果列表中

    return results


target_key = "rule_content"
# result = find_key_first(content_dict, target_key)
content_dict = read_rule_content(filename)
result = find_key_list(content_dict, target_key)
for i in result:
    # print('a', i)

    uid_mark_codes = set()
    for line in i.split('\n'):
        # print(line)
        if '$uid_mark_codes' in line:
            # 提取取值
            # print(line.split('='))
            value = line.split('=')[0].strip().strip('"').strip("'")
            # print('-------------------', value)
            # print(type(value))
            # 分割取值
            for item in value.split(','):
                # print('==============', item)
                # print('==============', item.strip())
                # print(type(item))
                uid_mark_codes.add(item.strip())
        # print('--------------', uid_mark_codes)

    # 生成所有可能的uid_mark_codes取值
    # all_combinations = [','.join(x) for x in itertools.product(sorted(uid_mark_codes), repeat=len(uid_mark_codes))]

    # 打印所有可能的取值
    # print(all_combinations)

    # if match:
    #     if_content = match.group(1)
    #     conditions = re.split(r"\s+&&\s+|\s+\|\|\s+", if_content)
    #     print(conditions)
    # else:
    #     print("No match found.")


# print(result)


# if match:
#     # 提取匹配的参数
#     split_arg = match.group(1)
#     value = match.group(2)
#
#     # 构造替换字符串
#     replacement = f"$uid_mark_codes:{{'not_includes':'{value}'}}"
#
#     # 进行替换
#     new_script = re.sub(pattern, replacement, script)
#     print(new_script)
# else:
#     print("No match found.")


# def compare_codes(code1, code2):
#     """
#   比较两段代码。
#
#   Args:
#     code1: 第一段代码。
#     code2: 第二段代码。
#
#   Returns:
#     两段代码之间的差异。
#   """
#
#     diff = difflib.Differ()
#     lines = diff.compare(code1.splitlines(), code2.splitlines())
#     return difflib.unified_diff(code1.splitlines(), code2.splitlines())
#
#
# def convert_diff_to_string(diff):
#     """
#     将diff对象转换成字符串。
#
#     Args:
#     diff: diff对象。
#
#     Returns:
#     diff对象转换成的字符串。
#   """
#
#     output = io.StringIO()
#     for line in diff:
#         output.write(line)
#     return output.getvalue()
#
#
# def get_diff_fields(code1, code2):
#     """
#     获取两段代码之间的差异字段。
#
#     Args:
#         code1: 第一段代码。
#         code2: 第二段代码。
#
#     Returns:
#         差异字段列表。
#     """
#     diff = difflib.SequenceMatcher(None, code1, code2)
#     diff_fields = []
#     for tag, i1, i2, j1, j2 in diff.get_opcodes():
#         if tag == 'replace':
#             diff_fields.append(code2[j1:j2])
#     return diff_fields
#
#
# def compare_strings(s1, s2):
#     # 创建SequenceMatcher对象
#     matcher = SequenceMatcher(None, s1, s2)
#     print(matcher)
#
#     # 获取匹配结果
#     result = matcher.get_opcodes()
#     print(result)
#
#     # 打印匹配结果
#     for opcode, a_start, a_end, b_start, b_end in result:
#         if opcode == 'equal':
#             print('euqal=', s1[a_start:a_end])
#         elif opcode == 'insert':
#             print(f'+ {s2[b_start:b_end]}')
#         elif opcode == 'delete':
#             print(f'- {s1[a_start:a_end]}')
#         elif opcode == 'replace':
#             print(f'- {s1[a_start:a_end]}')
#             print(f'+ {s2[b_start:b_end]}')
#
#
# # 示例
# def find_variables(code):
#     """Finds all variables in the given code.
#
#   Args:
#     code: The code to search for variables in.
#
#   Returns:
#     A list of all variables found in the code.
#   """
#
#     variables = set()
#     for match in re.finditer(r"\$[a-zA-Z_][a-zA-Z0-9_]*", code):
#         variables.add(match.group(0))
#     for match in re.finditer(r"#[a-zA-Z_][a-zA-Z0-9_]*", code):
#         variables.add(match.group(0))
#     return variables
#
#
# def get_field_values(code, field_name):
#     """Finds all values of the given field in the given code.
#
#   Args:
#     code: The code to search for values in.
#     field_name: The name of the field to search for.
#
#   Returns:
#     A list of all values of the given field found in the code.
#   """
#
#     values = []
#     for match in re.finditer(r"\$%s\s*=\s*([^;]*)" % field_name, code):
#         print('1', match)
#         values.append(match.group(1))
#     return values


# if __name__ == "__main__":
# code = '''if(!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&($lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0 &&
# UnFunction.includes($uid_mark_codes.split(","),"UAB51") || UnFunction.includes($uid_mark_codes.split(","),
# "UTB60") || UnFunction.includes($uid_mark_codes.split(","),"UTB61") || UnFunction.includes($uid_mark_codes.split(
# ","),"UAB52") || $lx_willzhou_black_cuishou_list=='cuishou_list')){#oper_decision="B30000";#approval_result=2;}'''
# # a = find_variables(code)
# string = "This is a string (with some (text) inside) it."
#
# start_index = code.find('(')
# end_index = code.rfind(')')
# # print(start_index)
# # print(end_index)
# logic_str = code[start_index:end_index]
# # print(logic_str.replace('\n', '').replace(' ', '').split('&&'))
# # my_string = "This is a (sample) string with (multiple) parentheses"
# positions_start = []
# positions_end = []
# start = 0
# end = 0
# while True:
#     start = code.find("(", start)
#     end = code.find(')',end)
#     if start == -1:
#         break
#     if end == -1:
#         break
#     positions_end.append(end)
#     positions_start.append(start)
#     start += 1
#     end += 1
# print("The positions of ( are:", positions_start)
# print("The positions of ) are:", positions_end)


# def find_shortest_match(s, open_positions, close_positions, start, end):
#     stack = []
#     for i in range(len(open_positions)):
#         if start <= open_positions[i] < end:
#             stack.append(i)
#             # print(stack)
#         elif close_positions[i] < end:
#             stack.pop()
#             # print(stack)
#         elif close_positions[i] >= start:
#             j = stack.pop()
#             sub_string = s[open_positions[j]:close_positions[i] + 1]
#             print(f"The shortest match between {open_positions[j]} and {close_positions[i]} is: {sub_string[1:-1]}")
#
#
# def find_positions_more_than_value(nums, target):
#     positions = []
#     for i in range(len(nums)):
#         if nums[i] > target:
#             positions.append(i)
#             print(positions)
#             break
#     return positions
#
#
# def is_valid(s):
#     pattern = r'^[a-zA-Z]+.+()'
#     return bool(re.match(pattern, s))
#
#
# def if_split(s):
#     pattern = r'if'
#     return s.split(pattern)
#
#
# def find_result_between(s, first, last, include_brackets=False):
#     try:
#         start = s.index(first) + len(first)
#         end = s.index(last, start)
#         if include_brackets:
#             return s[start - 1:end + 1]
#         else:
#             return s[start:end]
#     except ValueError:
#         return ""
#
#
# if __name__ == '__main__':
#     code = '''if(!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&($lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0 &&
#     UnFunction.includes($uid_mark_codes.split(","),"UAB51") || UnFunction.includes($uid_mark_codes.split(","),
#     "UTB60") || UnFunction.includes($uid_mark_codes.split(","),"UTB61") || UnFunction.includes($uid_mark_codes.split(
#     ","),"UAB52") || $lx_willzhou_black_cuishou_list=='cuishou_list')){#oper_decision="B30000";#approval_result=2;}'''
#     # my_string = "This is a (sample) string with (multiple) parentheses"
#     result = find_result_between(code, '{', '}', include_brackets=True)
#     condition = code.replace(result, '')
#     print(result)
#     print(condition)
#     # open_positions = [2, 23, 45, 61, 127, 149, 186, 208, 250, 272, 309, 331]
#     # close_positions = [49, 58, 153, 162, 212, 226, 276, 285, 340, 349, 401, 402]
#     logic_str_list = condition.replace('\n', '').replace(' ', '').split('&&')
#     print(logic_str_list)
#     logic_list = []
#     for i in logic_str_list:
#         print(i)
#         if '||' in i:
#             i_logic = i.split('||')
#             for j in i_logic:
#                 logic_list.append(j)
#                 a = is_valid(j)
#                 if not a:
#                     print('|| -----', j)
#                 # print(a)
#         if '||' not in i:
#             logic_list.append(i)
#             a = is_valid(i)
#             if a:
#                 print('not || ------', i)
#             if not a:
#                 print(i)
#     print(logic_list)
        # if '||' not in i:
        #     a = is_valid(i)
        #     print(a)
        # if '||' in i:
        #     i_logic = i.split('||')
        #     for j in i_logic:
        #         b = is_valid(j)
        #         print(b)