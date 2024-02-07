import json
import os
import re
from js2py import EvalJs

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


def generate_equivalence_partitions(ast_node, current_path=None):
    if current_path is None:
        current_path = []

    if ast_node['type'] == 'Program':
        # 对于最外层的 Program 节点，将其作为一个整体的路径
        for statement in ast_node['body']:
            generate_equivalence_partitions(statement, current_path)
    elif ast_node['type'] == 'IfStatement':
        # 处理条件语句
        condition = ast_node['test']
        left_value = evaluate_expression(condition['left'])
        right_value = evaluate_expression(condition['right'])
        operator = condition['operator']

        # 收集不同的条件取值
        conditions = [(left_value, operator, right_value)]

        # 处理条件为true的分支
        true_path = current_path + conditions
        generate_equivalence_partitions(ast_node['consequent'], true_path)

        # 处理条件为false的分支（如果存在）
        if ast_node['alternate']:
            false_path = current_path + [('not', conditions[0])]
            generate_equivalence_partitions(ast_node['alternate'], false_path)
    elif ast_node['type'] == 'ExpressionStatement':
        # 处理表达式语句，这里可以进一步处理其他类型的语句
        expression = ast_node['expression']
        if expression['type'] == 'CallExpression':
            callee = expression['callee']
            if callee['object']['name'] == 'console' and callee['property']['name'] == 'log':
                argument = expression['arguments'][0]
                if argument['type'] == 'Literal':
                    value = argument['value']
                elif argument['type'] == 'TemplateLiteral':
                    value = argument['quasis'][0]['value']['raw']
                else:
                    value = None

                if value is not None:
                    print(f"路径: {current_path}, 日志语句: {value}")


def evaluate_expression(expression):
    if expression['type'] == 'Identifier':
        return expression['name']
    elif expression['type'] == 'Literal':
        return expression['value']
    else:
        return None


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


def if_logic_input_process(if_ast_node):
    test = if_ast_node['test']
    if test['type'] == 'BinaryExpression':
        left = test['left']
        if left['type'] == 'Identifier':
            left_name = left['name']
        elif left['type'] == 'Literal':
            left_value = left['value']
        right = test['right']

        operator = test['operator']


def find_logic_by_type(ast_node, target_type):
    if isinstance(ast_node, dict):
        if "type" in ast_node and ast_node["type"] == target_type:
            return ast_node

        for key, value in ast_node.items():
            result = find_logic_by_type(value, target_type)
            if result:
                return result

    elif isinstance(ast_node, list):
        for item in ast_node:
            result = find_logic_by_type(item, target_type)
            if result:
                return result

    return None


def find_type_logic(ast_node, target_type):
    result = []

    def recursive_search(node, parent_type=None):
        if isinstance(node, dict):
            if "type" in node:
                current_type = node["type"]
                if current_type == target_type:
                    result.append({"type": current_type, "parent_type": parent_type, "logic": node})
                for key, value in node.items():
                    recursive_search(value, current_type)

        elif isinstance(node, list):
            for item in node:
                recursive_search(item, parent_type)

    recursive_search(ast_node)
    return result


def extract_logical_operators(node, operators=None):
    if operators is None:
        operators = []

    if isinstance(node, dict):
        if 'operator' in node and node['operator'] in ['&&', '||']:
            operators.append(node['operator'])

        for key, value in node.items():
            extract_logical_operators(value, operators)

    elif isinstance(node, list):
        for item in node:
            extract_logical_operators(item, operators)

    return operators


# 示例ATS树
ats_tree = {
    "body": [
        {
            "test": {
                "left": {
                    "name": "$a",
                    "type": "Identifier"
                },
                "operator": "&&",
                "right": {
                    "name": "$b",
                    "type": "Identifier"
                },
                "type": "LogicalExpression"
            },
            "type": "IfStatement"
        },
        {
            "test": {
                "left": {
                    "name": "$c",
                    "type": "Identifier"
                },
                "operator": "||",
                "right": {
                    "name": "$d",
                    "type": "Identifier"
                },
                "type": "LogicalExpression"
            },
            "type": "IfStatement"
        }
    ],
    "type": "Program"
}

logical_operators = extract_logical_operators(ats_tree)
print(logical_operators)


def analyze_nested_parentheses(expression):
    stack = []
    result = []

    for i, char in enumerate(expression):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start_index = stack.pop()
                end_index = i
                result.append((start_index, end_index))

    return result


def extract_logic_from_expression(expression, nested_parentheses):
    result = []

    for start, end in nested_parentheses:
        if expression[start + 1:end].count('(') == expression[start + 1:end].count(')'):
            result.append(expression[start + 1:end])

    return result


# # 示例用法
# expression = ("if($block_code_valid_alias!=null && $block_code_valid_alias!=\"-2\"&& CommFunction.contains("
#               "$block_code_valid_alias, 'C163') && ($uid>0 && $uid<3000000 || $uid>5000000)&& $cs_kefu_risk_tag !=1)")
# nested_parentheses_logic = analyze_nested_parentheses(expression)
# logic_inside_parentheses = extract_logic_from_expression(expression, nested_parentheses_logic)
#
# for logic in logic_inside_parentheses:
#     print(f"Logic inside parentheses: {logic}")


# if __name__ == "__main__":
#     # 提供的抽象语法树
#     with open('outputData/rule_id:1542029.json', 'r', encoding='utf-8') as f:
#         ast = json.loads(f.read())
#     binary_result = find_type_logic(ast,'BinaryExpression')
#     call_result = find_type_logic(ast,'CallExpression')
#
#     # result = find_logic_by_type(ast, 'LogicalExpression')
#     print(binary_result)
#     print(call_result)
#     # 生成逻辑覆盖的等价划分数据
#     program_logic_ast = get_program_logic_AST(ast)
#     outpit_logic = get_output_logic_AST(program_logic_ast)
#     if outpit_logic['type'] == 'IfStatement':
#         result_list = if_logic_output_process(outpit_logic)
#         print(result_list)
#
#     # def extract_logic_for_field(ast, target_field):
#     #     if isinstance(ast, dict):
#     #         if "type" in ast:
#     #             if ast["type"] == "Program":
#     #                 if "body" in ast:
#     #                     program_body_logic = ""
#     #                     for statement in ast["body"]:
#     #                         statement_logic = extract_logic_for_field(statement, target_field)
#     #                         if statement_logic:
#     #                             program_body_logic += statement_logic + "\n"
#     #
#     #                     return program_body_logic
#     #
#     #             elif ast["type"] == "IfStatement":
#     #                 test_logic = extract_logic_for_field(ast["test"], target_field)
#     #                 consequent_logic = extract_logic_for_field(ast["consequent"], target_field)
#     #                 alternate_logic = extract_logic_for_field(ast["alternate"], target_field)
#     #
#     #                 return f"if {test_logic} {{\n{consequent_logic}\n}} else {{\n{alternate_logic}\n}}"
#     #
#     #             elif ast["type"] == "LogicalExpression":
#     #                 left_logic = extract_logic_for_field(ast["left"], target_field)
#     #                 right_logic = extract_logic_for_field(ast["right"], target_field)
#     #
#     #                 return f"{left_logic} {ast['operator']} {right_logic}"
#     #
#     #             elif ast["type"] == "BinaryExpression":
#     #                 left_logic = extract_logic_for_field(ast["left"], target_field)
#     #                 right_logic = extract_logic_for_field(ast["right"], target_field)
#     #
#     #                 return f"{left_logic} {ast['operator']} {right_logic}"
#     #
#     #             elif ast["type"] == "Identifier":
#     #                 return ast["name"] if ast["name"] == target_field else ""
#     #
#     #             elif ast["type"] == "Literal":
#     #                 return str(ast["value"])
#     #
#     #     return ""
#     #
#     #
#     # ast = {
#     #     "body": [
#     #         {
#     #             "alternate": None,
#     #             "consequent": {
#     #                 "body": [
#     #                     {
#     #                         "expression": {
#     #                             "arguments": [
#     #                                 {
#     #                                     "type": "Literal",
#     #                                     "value": "#oper_decision=\"B30000\";#approval_result=2;"
#     #                                 }
#     #                             ],
#     #                             "callee": {
#     #                                 "computed": False,
#     #                                 "object": {
#     #                                     "name": "console",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "property": {
#     #                                     "name": "log",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "type": "MemberExpression"
#     #                             },
#     #                             "type": "CallExpression"
#     #                         },
#     #                         "type": "ExpressionStatement"
#     #                     }
#     #                 ],
#     #                 "type": "BlockStatement"
#     #             },
#     #             "test": {
#     #                 "left": {
#     #                     "left": {
#     #                         "left": {
#     #                             "left": {
#     #                                 "left": {
#     #                                     "name": "$block_code_valid_alias",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "operator": "!=",
#     #                                 "right": {
#     #                                     "type": "Literal",
#     #                                     "value": None
#     #                                 },
#     #                                 "type": "BinaryExpression"
#     #                             },
#     #                             "operator": "&&",
#     #                             "right": {
#     #                                 "left": {
#     #                                     "name": "$block_code_valid_alias",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "operator": "!=",
#     #                                 "right": {
#     #                                     "type": "Literal",
#     #                                     "value": "-2"
#     #                                 },
#     #                                 "type": "BinaryExpression"
#     #                             },
#     #                             "type": "LogicalExpression"
#     #                         },
#     #                         "operator": "&&",
#     #                         "right": {
#     #                             "arguments": [
#     #                                 {
#     #                                     "name": "$block_code_valid_alias",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 {
#     #                                     "type": "Literal",
#     #                                     "value": "C163"
#     #                                 }
#     #                             ],
#     #                             "callee": {
#     #                                 "computed": False,
#     #                                 "object": {
#     #                                     "name": "CommFunction",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "property": {
#     #                                     "name": "contains",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "type": "MemberExpression"
#     #                             },
#     #                             "type": "CallExpression"
#     #                         },
#     #                         "type": "LogicalExpression"
#     #                     },
#     #                     "operator": "&&",
#     #                     "right": {
#     #                         "left": {
#     #                             "left": {
#     #                                 "left": {
#     #                                     "name": "$uid",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "operator": ">",
#     #                                 "right": {
#     #                                     "type": "Literal",
#     #                                     "value": 0
#     #                                 },
#     #                                 "type": "BinaryExpression"
#     #                             },
#     #                             "operator": "&&",
#     #                             "right": {
#     #                                 "left": {
#     #                                     "name": "$uid",
#     #                                     "type": "Identifier"
#     #                                 },
#     #                                 "operator": "<",
#     #                                 "right": {
#     #                                     "type": "Literal",
#     #                                     "value": 3000000
#     #                                 },
#     #                                 "type": "BinaryExpression"
#     #                             },
#     #                             "type": "LogicalExpression"
#     #                         },
#     #                         "operator": "||",
#     #                         "right": {
#     #                             "left": {
#     #                                 "name": "$uid",
#     #                                 "type": "Identifier"
#     #                             },
#     #                             "operator": ">",
#     #                             "right": {
#     #                                 "type": "Literal",
#     #                                 "value": 5000000
#     #                             },
#     #                             "type": "BinaryExpression"
#     #                         },
#     #                         "type": "LogicalExpression"
#     #                     },
#     #                     "type": "LogicalExpression"
#     #                 },
#     #                 "operator": "&&",
#     #                 "right": {
#     #                     "left": {
#     #                         "name": "$cs_kefu_risk_tag",
#     #                         "type": "Identifier"
#     #                     },
#     #                     "operator": "!=",
#     #                     "right": {
#     #                         "type": "Literal",
#     #                         "value": 1
#     #                     },
#     #                     "type": "BinaryExpression"
#     #                 },
#     #                 "type": "LogicalExpression"
#     #             },
#     #             "type": "IfStatement"
#     #         }
#     #     ],
#     #     "type": "Program"
#     # }
#     # uid_logic = extract_logic_for_field(ast, '$uid')
#     # print(uid_logic)
def print_ast_tree(node, indent=""):
    print(f"{indent}{node['type']}")

    for key in node:
        if isinstance(node[key], dict) and node[key]:  # 如果属性值是字典
            print_ast_tree(node[key], indent + "  ")
        elif isinstance(node[key], list):  # 如果属性值是数组
            for child in node[key]:
                print_ast_tree(child, indent + "  ")
        else:
            print(f"{indent}  {key}: {node[key]}")


def interpret_ast(node):
    node_type = node['type']

    if node_type == 'IfStatement':
        test_result = interpret_expression(node['test'])
        if test_result:
            for statement in node['consequent']['body']:
                interpret_statement(statement)
        elif 'alternate' in node and node['alternate'] is not None:
            interpret_statement(node['alternate'])

    elif node_type == 'LogicalExpression':
        left_value = interpret_expression(node['left'])
        right_value = interpret_expression(node['right'])

        if node['operator'] == '&&':
            return left_value and right_value
        elif node['operator'] == '||':
            return left_value or right_value

    elif node_type == 'BinaryExpression':
        left_expr_value = interpret_expression(node['left'])
        right_expr_value = interpret_expression(node['right'])

        if node['operator'] == '!=':
            return left_expr_value != right_expr_value
        # 添加其他二元运算符的处理...

    elif node_type == 'CallExpression':
        callee_value = interpret_expression(node['callee'])
        args_values = [interpret_expression(arg) for arg in node['arguments']]

        # 这里假设函数调用已经存在于全局作用域中
        if callable(callee_value):  # 注意：在Python中判断是否是可调用对象
            callee_value(*args_values)
    elif node_type == 'Program':
        for statement in node['body']:
            interpret_statement(statement)

    # 其他节点类型的处理...

    else:
        print(f"Unsupported node type: {node_type}")
        return None


def interpret_expression(node):
    return interpret_ast(node)


def interpret_statement(node):
    node_type = node['type']

    if node_type == 'ExpressionStatement':
        interpret_expression(node['expression'])

    # 其他语句类型的处理...

    else:
        print(f"Unsupported statement type: {node_type}")


# 开始模拟执行


# 给定的 AST JSON 数据
# with
ast_data = {
    "type": "Program",
    "sourceType": "script",
    "body": [{
        "type": "IfStatement",
        "test": {
            "type": "LogicalExpression",
            "operator": "&&",
            "left": {
                "type": "LogicalExpression",
                "operator": "&&",
                "left": {
                    "type": "LogicalExpression",
                    "operator": "&&",
                    "left": {
                        "type": "LogicalExpression",
                        "operator": "&&",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": "!=",
                            "left": {
                                "type": "Identifier",
                                "name": "$block_code_valid_alias"
                            },
                            "right": {
                                "type": "Literal",
                                "value": None,
                                "raw": "null"
                            }
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "!=",
                            "left": {
                                "type": "Identifier",
                                "name": "$block_code_valid_alias"
                            },
                            "right": {
                                "type": "Literal",
                                "value": "-2",
                                "raw": "\"-2\""
                            }
                        }
                    },
                    "right": {
                        "type": "CallExpression",
                        "callee": {
                            "type": "MemberExpression",
                            "computed": False,
                            "object": {
                                "type": "Identifier",
                                "name": "CommFunction"
                            },
                            "property": {
                                "type": "Identifier",
                                "name": "contains"
                            }
                        },
                        "arguments": [{
                            "type": "Identifier",
                            "name": "$block_code_valid_alias"
                        }, {
                            "type": "Literal",
                            "value": "C163",
                            "raw": "'C163'"
                        }]
                    }
                },
                "right": {
                    "type": "LogicalExpression",
                    "operator": "||",
                    "left": {
                        "type": "LogicalExpression",
                        "operator": "&&",
                        "left": {
                            "type": "BinaryExpression",
                            "operator": ">",
                            "left": {
                                "type": "Identifier",
                                "name": "$uid"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 0,
                                "raw": "0"
                            }
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": "<",
                            "left": {
                                "type": "Identifier",
                                "name": "$uid"
                            },
                            "right": {
                                "type": "Literal",
                                "value": 3000000,
                                "raw": "3000000"
                            }
                        }
                    },
                    "right": {
                        "type": "BinaryExpression",
                        "operator": ">",
                        "left": {
                            "type": "Identifier",
                            "name": "$uid"
                        },
                        "right": {
                            "type": "Literal",
                            "value": 5000000,
                            "raw": "5000000"
                        }
                    }
                }
            },
            "right": {
                "type": "BinaryExpression",
                "operator": "!=",
                "left": {
                    "type": "Identifier",
                    "name": "$cs_kefu_risk_tag"
                },
                "right": {
                    "type": "Literal",
                    "value": 1,
                    "raw": "1"
                }
            }
        },
        "consequent": {
            "type": "BlockStatement",
            "body": [{
                "type": "ExpressionStatement",
                "expression": {
                    "type": "CallExpression",
                    "callee": {
                        "type": "MemberExpression",
                        "computed": False,
                        "object": {
                            "type": "Identifier",
                            "name": "console"
                        },
                        "property": {
                            "type": "Identifier",
                            "name": "log"
                        }
                    },
                    "arguments": [{
                        "type": "Literal",
                        "value": "#oper_decision=\"B30000\";#approval_result=2;",
                        "raw": "'#oper_decision=\"B30000\";#approval_result=2;'"
                    }]
                }
            }]
        },
        "alternate": None
    }]
}
if __name__ == '__main__':
    interpret_ast(ast_data)
