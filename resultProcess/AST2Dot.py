import json
import os

from graphviz import Digraph

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


def json_to_dot(json_data:dict, graph=None, parent=None, key_node_mapping=None):
    if graph is None:
        graph = Digraph()

    if key_node_mapping is None:
        key_node_mapping = {}

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key not in key_node_mapping:
                child_node_name = f"{key}_{id(value)}"
                graph.node(child_node_name, label=f'"{key}"', shape='box')
                key_node_mapping[key] = child_node_name
            else:
                child_node_name = key_node_mapping[key]
            if parent is not None:
                graph.edge(parent, child_node_name)
            json_to_dot(value, graph, child_node_name, key_node_mapping)
    elif isinstance(json_data, list):
        for index, value in enumerate(json_data):
            child_node_name = f"{index}_{id(value)}"
            graph.node(child_node_name, label=f'"{index}"', shape='ellipse')
            if parent is not None:
                graph.edge(parent, child_node_name)
            json_to_dot(value, graph, child_node_name, key_node_mapping)
    else:
        child_node_name = f"{json_data}_{id(json_data)}"
        graph.node(child_node_name, label=f'"{json_data}"', shape='plaintext')
        if parent is not None:
            graph.edge(parent, child_node_name)

    return graph


if __name__ == '__main__':
    with open('outputData/package_id:2077:rule_id:1542029_test.json', 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())
        # print(json_data)
    graph = json_to_dot(json_data)
    graph.render('output_graph', format='png', cleanup=True)
    dot_content = graph.source
    with open('output_graph.dot', 'w') as dot_file:
        dot_file.write(dot_content)
