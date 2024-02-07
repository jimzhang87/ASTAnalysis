import json
import esprima


def extract_nodes_by_type(node, target_type):
    result = []

    if isinstance(node, dict):
        if 'type' in node and node['type'] == target_type:
            result.append(node)

        for key, value in node.items():
            if isinstance(value, (dict, list)):
                result.extend(extract_nodes_by_type(value, target_type))

    elif isinstance(node, list):
        for item in node:
            result.extend(extract_nodes_by_type(item, target_type))

    return result


def traverse_ast(node, depth=0):
    print('enter')
    print(type(node))
    if isinstance(node, dict):
        print('node is dict')
        for key, value in node.items():
            if key == 'type':
                print('  ' * depth + f'Type: {value}')
            else:
                print('  ' * depth + f'{key}:')
                traverse_ast(value, depth + 1)
    elif isinstance(node, list):
        print('node is list')
        for item in node:
            traverse_ast(item, depth + 1)


# 示例 JavaScript 代码
code3 = ('if(!UnFunction.includes($uid_mark_codes.split(","),"UTB27")&&$lx_dp_fk_cm_mart_yiwang_oa_01_uid<=0&&('
         'UnFunction.includes($uid_mark_codes.split(","),"UAB30")||UnFunction.includes($uid_mark_codes.split(","),'
         '"UAB31")||UnFunction.includes($uid_mark_codes.split(","),"UAB32")||UnFunction.includes('
         '$uid_mark_codes.split(","),"UAB40")||UnFunction.includes($uid_mark_codes.split(","),'
         '"UAB41")||UnFunction.includes($uid_mark_codes.split(","),"UAB42")||UnFunction.includes('
         '$uid_mark_codes.split(","),"UAB43")||UnFunction.includes($uid_mark_codes.split(","),'
         '"UTB10")||UnFunction.includes($uid_mark_codes.split(","),"UTB11")||UnFunction.includes('
         '$uid_mark_codes.split(","),"UTB12")||UnFunction.includes($uid_mark_codes.split(","),'
         '"UTB20")||UnFunction.includes($uid_mark_codes.split(","),"UTB21")||UnFunction.includes('
         '$uid_mark_codes.split(","),"UTB22")||UnFunction.includes($uid_mark_codes.split(","),'
         '"UTB23")||UnFunction.includes($uid_mark_codes.split(","),"UTB24")||UnFunction.includes('
         '$uid_mark_codes.split(","),"UTB25")||UnFunction.includes($uid_mark_codes.split(","),'
         '"UTB26")||$lx_willzhou_black_qizha_list==\'qizha_list\')){console.log('
         '\'#oper_decision="B10000";#approval_result=2;\')}')

js_code = """
if (x > 0) {
    console.log("Positive");
} else {
    console.log("Non-positive");
}
"""

# 使用 esprima 解析 JavaScript 代码
ast_tree = esprima.parseScript(code3, {'loc': False})
print(type(ast_tree))
script_node = ast_tree.body
print(script_node)
# traverse_ast(ast_tree)

# 提取所有的 'IfStatement' 类型节点
# if_nodes = extract_nodes_by_type(ast_tree, 'IfStatement')
# print(if_nodes)
# 打印结果
# for node in if_nodes:
#     print(json.dumps(node, indent=2))
