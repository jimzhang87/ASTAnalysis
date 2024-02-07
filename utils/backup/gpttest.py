import json
import networkx as nx
import pygraphviz as pgv
from networkx.drawing.nx_agraph import write_dot
import random,string


def add_edges(graph, node, parent=None):
    if isinstance(node, dict):
        for k, v in node.items():
            if parent is not None:
                graph.add_edge(parent, k)
            add_edges(graph, v, parent=k)
    elif isinstance(node, list):
        for i in node:
            add_edges(graph, i, parent=parent)


# 读取JSON数据
def  read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        G = nx.DiGraph()
        add_edges(G, data)
        write_dot(G, 'graph.dot')


def generate_random_string(length=len):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == '__main__':
    for i in range(10):
        str = generate_random_string(12)
        print(str)
    # data = json.loads(
    # '{"alternate": null,"consequent": {"body": [{"expression": {"arguments": [{"type": "Literal",'
    # '"value": "#oper_decision=\\"B10000\\";#approval_result=2;"}],"callee": {"computed": false,"object": {"name": '
    # '"console","type": "Identifier"},"property": {"name": "log","type": "Identifier"},"type": "MemberExpression"},'
    # '"type": "CallExpression"},"type": "ExpressionStatement"}],"type": "BlockStatement"}}')

# 创建一个有向图
# G = nx.DiGraph()

# 添加边
# add_edges(G, data)

# 将图形保存为DOT文件
# write_dot(G, 'graph.dot')
