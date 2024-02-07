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

# code = 'if(!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&($lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0 && UnFunction.includes($uid_mark_codes.split(","),"UAB51") || UnFunction.includes($uid_mark_codes.split(","),"UTB60") || UnFunction.includes($uid_mark_codes.split(","),"UTB61") || UnFunction.includes($uid_mark_codes.split(","),"UAB52") || $lx_willzhou_black_cuishou_list==\'cuishou_list\')){console.log(\'#oper_decision="B30000";#approval_result=2;\');}'
# code2 = 'if ($dxm_lxa_v3_seg123_score < 369 && $dxm_lxa_v3_seg123_score >= 0) {console.log(\'~dxm_lxa_v3_seg123_score_tag = -49.25;\')} else if ($dxm_lxa_v3_seg123_score < 397 && $dxm_lxa_v3_seg123_score >= 0) {console.log(\'~dxm_lxa_v3_seg123_score_tag = -12.35;\')} else if ($dxm_lxa_v3_seg123_score < 400 && $dxm_lxa_v3_seg123_score >= 0) {console.log(\'~dxm_lxa_v3_seg123_score_tag = 7.3;\')}'
code3 = 'if(!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&$lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0&&(UnFunction.includes($uid_mark_codes.split(","),"UAB30")||UnFunction.includes($uid_mark_codes.split(","),"UAB31")||UnFunction.includes($uid_mark_codes.split(","),"UAB32")||UnFunction.includes($uid_mark_codes.split(","),"UAB40")||UnFunction.includes($uid_mark_codes.split(","),"UAB41")||UnFunction.includes($uid_mark_codes.split(","),"UAB42")||UnFunction.includes($uid_mark_codes.split(","),"UAB43")||UnFunction.includes($uid_mark_codes.split(","),"UTB10")||UnFunction.includes($uid_mark_codes.split(","),"UTB11")||UnFunction.includes($uid_mark_codes.split(","),"UTB12")||UnFunction.includes($uid_mark_codes.split(","),"UTB20")||UnFunction.includes($uid_mark_codes.split(","),"UTB21")||UnFunction.includes($uid_mark_codes.split(","),"UTB22")||UnFunction.includes($uid_mark_codes.split(","),"UTB23")||UnFunction.includes($uid_mark_codes.split(","),"UTB24")||UnFunction.includes($uid_mark_codes.split(","),"UTB25")||UnFunction.includes($uid_mark_codes.split(","),"UTB26")||$lx_willzhou_black_qizha_list==\'qizha_list\')){console.log(\'#oper_decision="B10000";#approval_result=2;\')}'

# esprima = js2py.require('esprima')
# escodegen = js2py.require('escodegen')


# def js_translate_AST(code):
#     tree = esprima.parse(code)
#     tree_dict = json.dumps(tree.to_dict(), indent=4)
#     return tree_dict


tree = esprima.parse(code3)


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
            rule_data = rule_content.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace(
                '\t', '"')
            # rule_data = i.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\t', '"')
            matches = re.findall(r'\{(.*?)}', rule_data)
            # print(matches[0])
            new_rule_data = re.sub(r'\{(.*?)}', '{console.log(\'%s\')}' % matches[0], rule_data)
            tree_json = esprima.parseScript(new_rule_data, {'loc': False})
            tree_dict = node_to_dict(tree_json)
            with open('outputData/package_id:%s:rule_id:%s_test.json' % (package_id, rule_id), 'w', encoding='utf-8') as f:
                for k in json.dumps(tree_dict):
                    f.write(k)


# tree_dict = node_to_dict(tree)
# print(tree_dict)
# tree_dict = json.dumps(tree.to_dict(), indent=4)
# print(tree_dict)
# with open('outputData/ruleDetailInfo.json', 'w', encoding='utf-8') as f:
#     f.write(tree_dict)
if __name__ == '__main__':
    crawl_rule_from_package_detail_info('outputData/packageDetailInfo.json')
    # tree = esprima.parse(code3)
    # tree_dict = json.dumps(tree.to_dict(), indent=4)
    # print(tree_dict)
    # with open('outputData/packageDetailInfo.json', 'r', encoding='utf-8') as f:
    #     package_detail_json = json.load(f)
    #     # print(package_detail_json)
    #     strategy_node_flow_rule_list = find_values(package_detail_json, 'strategy_node_flow_rule_list')
    #     # print(strategy_node_flow_rule_list[0])
    #     for i in strategy_node_flow_rule_list[0]:
    #         print(i)
    #         rule_id = i['rule_id']
    #         rule_data = i['rule_data']
    #         rule_content = rule_data['rule_content']
    #         # rule_content_list = find_values(package_detail_json, 'rule_content')
    #         # print(rule_content_list)
    #         # for i in rule_content_list:
    #         rule_data = rule_content.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace(
    #             '\t', '"')
    #         # rule_data = i.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\t', '"')
    #         matches = re.findall(r'\{(.*?)}', rule_data)
    #         # print(matches[0])
    #         new_rule_data = re.sub(r'\{(.*?)}', '{console.log(\'%s\')}' % matches[0], rule_data)
    #         # print('----------', new_rule_data)
    #         tree_json = esprima.parseScript(new_rule_data, {'loc': False})
    #
    #         # tree_json = js_translate_AST(new_rule_data)
    #         # tree_json = js_translate_AST(new_rule_data)
    #         # print(tree_json)
    #         tree_dict = node_to_dict(tree_json)
    #         print(tree_dict)
    #         # tree_dict = json.loads(tree_json)
    #         key = tree_dict.keys()
    #         value = tree_dict.values()
    #         # print(key)
    #         # print(value)
    #         # plt.bar(key, value)
    #         # plt.show()
    #         with open('outputData/rule_id:%s_test.json' % rule_id, 'w', encoding='utf-8') as f:
    #             for k in json.dumps(tree_dict):
    #                 f.write(k)

            # tree_json_list.append(tree_json)
    # print(tree_json_list)
    # with open('outputData/rule_id:%s.json' % rule_id, 'w', encoding='utf-8') as f:
    #     for k in tree_json_list:
    #         f.write(k)
    # with open("output_3.json", "w") as f:
    #     f.write(tree_dict)
# except FileExistsError:
#     print("File already exists.")
# print(tree_dict)
# print(a)
# 将JS代码转换为AST
# tree = astor.parse_file('outputData/ruleDetailInfo.txt')

# print(tree.body[0])
# source_code = astor.to_source(tree)

# print(source_code)
# print(tree_dict)
# print(tree_dict)
# print
# print(esprima)
# tree = esprima.parse('!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&($lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0 && UnFunction.includes($uid_mark_codes.split(","),"UAB51") || UnFunction.includes($uid_mark_codes.split(","),"UTB60") || UnFunction.includes($uid_mark_codes.split(","),"UTB61") || UnFunction.includes($uid_mark_codes.split(","),"UAB52") || $lx_willzhou_black_cuishou_list=="cuishou_list")')
# tree = esprima.parse(
#     'if(!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&($lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0 && UnFunction.includes($uid_mark_codes.split(","),"UAB51") || UnFunction.includes($uid_mark_codes.split(","),"UTB60") || UnFunction.includes($uid_mark_codes.split(","),"UTB61") || UnFunction.includes($uid_mark_codes.split(","),"UAB52") || $lx_willzhou_black_cuishou_list==\'cuishou_list\')) {console.log(\'#oper_decision="B30000";#approval_result=2;\');}')
# js_ast = ast.parse(source=code3)
# for node in ast.walk(js_ast):
#     print(node)
# a = js2py.eval_js(code3)
# print(a)
# tree = esprima.parse(code3)
# tree_dict = json.dumps(tree.to_dict(), indent=4)
# with open('outputData/ruleDetailInfo.json', 'w', encoding='utf-8') as f:
#     f.write(tree_dict)
# try:
#     with open("output_3.json", "a") as f:
#         f.write(tree_dict)
# except FileExistsError:
#     print("File already exists.")
# print(tree_dict)
# print(a)
# 将JS代码转换为AST
# tree = astor.parse_file('outputData/ruleDetailInfo.txt')

# print(tree.body[0])
# source_code = astor.to_source(tree)

# print(source_code)
# print(tree_dict)
# print(tree_dict)
# print(tree_dict['type'])
# print(tree_dict['

# parser = Lark(code)
# js_grammar = r"""
# ?start: if_statement
#
# if_statement: "if" "!" expression "&&" expression "&&" expression "&&" expression "&&" expression "&&" expression "&&" expression
#
# expression: term (() term)*
#
# or_expression: and_expression ("&&" and_expression)*
#
# and_expression: not_expression ("in" not_expression)*
#
# not_expression: "!" not_expression | comparison
#
# comparison: arithmetic_expression ("==" | "!=" | "<" | ">" | "<=" | ">=") arithmetic_expression
#
# arithmetic_expression: term ("+" | "-")* term
#
# term: factor ("*" | "/" | "%")* factor
#
# factor: "(" expression ")" | atom
#
# atom: NAME | NUMBER | STRING | "true" | "false" | "null"
#
# NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
# NUMBER: /\d+/
# STRING: /"([^"\\\\]*(\\\\.[^"\\\\]*)*)"/
# """
#
#
# class TreeToDict(Transformer):
#     def start(self, items):
#         return {"if_statement": items[0]}
#
#     def if_statement(self, items):
#         return items[0]
#
#     def expression(self, items):
#         return {"expression": items[0]}
#
#     def or_expression(self, items):
#         return {"or_expression": items[0]}
#
#     def and_expression(self, items):
#         return {"and_expression": items[0]}
#
#     def not_expression(self, items):
#         return {"not_expression": items[0]}
#
#     def comparison(self, items):
#         return {"comparison": items[0]}
#
#     def arithmetic_expression(self, items):
#         return {"arithmetic_expression": items[0]}
#
#     def term(self, items):
#         return {"term": items[0]}
#
#     def factor(self, items):
#         return {"factor": items[0]}
#
#     def atom(self, items):
#         return {"atom": items[0]}
#
#
# parser = Lark(js_grammar)
# lark_tree = parser.parse(code)
# result = TreeToDict().transform(tree=lark_tree)
# print(result)
