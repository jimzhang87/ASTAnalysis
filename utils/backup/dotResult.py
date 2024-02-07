import json
import os
import random

from graphviz import Digraph

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def json_to_dot_pdf(json_data, graph=None, parent=None):
    if graph is None:
        graph = Digraph()

    current_color = parent.get('color', generate_random_color()) if parent else generate_random_color()

    if isinstance(json_data, dict):
        print(json_data,'is dict')
        for key, value in json_data.items():
            print(key)
            print(value)
            child_node_name = f"{key}_{id(value)}"
            graph.node(child_node_name, label=f'"{key}"', shape='box', style='filled')
            if parent is not None:
                # current_color = generate_random_color()
                graph.edge(parent['name'], child_node_name, color=current_color)
            # if parent is None:
            #     current_color = generate_random_color()
            json_to_dot(value, graph, {'name': child_node_name, 'color': current_color})
    elif isinstance(json_data, list):
        print(json_data,'is list')
        for index, value in enumerate(json_data):
            child_node_name = f"{index}_{id(value)}"
            graph.node(child_node_name, label=f'"{index}"', shape='ellipse', style='filled')
            if parent is not None:
                graph.edge(parent['name'], child_node_name, color=current_color)
            json_to_dot(value, graph, {'name': child_node_name, 'color': current_color})
    else:
        child_node_name = f"{json_data}_{id(json_data)}"
        graph.node(child_node_name, label=f'"{json_data}"', shape='plaintext', style='filled')
        if parent is not None:
            graph.edge(parent['name'], child_node_name, color=current_color)

    return graph


def json_to_dot(json_data, graph=None, parent=None, key_node_mapping=None, current_color=None):
    if graph is None:
        graph = Digraph()

    # if current_color is None:
    #     current_color = generate_random_color()

    if key_node_mapping is None:
        key_node_mapping = {}

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key not in key_node_mapping:
                child_node_name = f"{key}_{id(value)}"
                graph.node(child_node_name, label=f'"{key}"', shape='box', style='filled')
                key_node_mapping[key] = child_node_name
            else:
                child_node_name = key_node_mapping[key]

            if parent is None:
                current_color = generate_random_color()
            if parent is not None:
                graph.edge(parent, child_node_name, label=f'"{key}"', color=current_color)
            json_to_dot(value, graph, child_node_name, key_node_mapping, current_color)
    elif isinstance(json_data, list):
        for index, value in enumerate(json_data):
            child_node_name = f"{index}_{id(value)}"
            graph.node(child_node_name, label=f'"{index}"', shape='ellipse', style='filled')
            if parent is not None:
                graph.edge(parent, child_node_name, label=f'"{index}"', color=current_color)
            json_to_dot(value, graph, child_node_name, key_node_mapping, current_color)
    else:
        child_node_name = f"{json_data}_{id(json_data)}"
        graph.node(child_node_name, label=f'"{json_data}"', shape='plaintext', style='filled')
        if parent is not None:
            graph.edge(parent, child_node_name, color=current_color)

    return graph


def json_to_dot2(json_data, graph=None, parent=None, current_color=None, edge_label=None):
    if graph is None:
        graph = Digraph()

    # if current_color is None:
    #     current_color = generate_random_color()

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == 'input':
                edge_label = str(value).replace(',',',\n')
                continue
                # json_to_dot2(value, graph, child_node_name, current_color,edge_label)
            if key != 'input' and key == 'output':
                child_node_name = f"{key}_{id(value)}"
                graph.node(child_node_name, label=f'"{value}"', shape='box', style='filled')
                if parent is None:
                    current_color = generate_random_color()
                if parent is not None:
                    if edge_label is None:
                        graph.edge(parent, child_node_name, color=current_color)
                    else:
                        graph.edge(parent, child_node_name, label=edge_label, color=current_color)
                        edge_label = None
                continue
            else:
                child_node_name = f"{key}_{id(value)}"
                graph.node(child_node_name, label=f'"{key}"', shape='box', style='filled')
                current_color = generate_random_color()
                if parent is not None:
                    graph.edge(parent, child_node_name, color=current_color)
                json_to_dot2(value, graph, child_node_name, current_color)
    elif isinstance(json_data, list):
        for index, value in enumerate(json_data):
            child_node_name = f"{index}_{id(value)}"
            graph.node(child_node_name, label=f'"{index}"', shape='ellipse', style='filled')
            if parent is not None:
                graph.edge(parent, child_node_name, label=f'"{index}"', color=current_color)
            json_to_dot2(value, graph, child_node_name, current_color)
    else:
        child_node_name = f"{json_data}_{id(json_data)}"
        graph.node(child_node_name, label=f'"{json_data}"', shape='plaintext', style='filled')
        if parent is not None:
            graph.edge(parent, child_node_name, color=current_color)

    return graph


# 示例用法
json_data = {"rule_id": {
    "logic1": {
        "input": {
            "block_code_valid_alias": {
                "!=": "-2"
            },
            "uid": {
                ">": 0,
                "<": 3000000
            },
            "cs_kefu_risk_tag": {
                "!=": 1
            }},
        "output": {
            "#oper_decision": "\"B30000\"",
            "#approval_result": "2"
        }
    },
    "logic2": {
        "input": {
            "block_code_valid_alias": {
                "!=": "None"
            },
            "uid": {
                ">": 0,
                "<": 3000000
            },
            "cs_kefu_risk_tag": {
                "!=": 1
            }},
        "output": {
            "#oper_decision": "\"B30000\"",
            "#approval_result": "2"
        }
    }
}
}
json_data2 = {
    "logic1": {
        "input": [{
            "a": "red"
        }],
        "output1": "1"
    },
    "logic2": {
        "input": {
            "b": "green"
        },
        "output2": "2"
    }
}

# graph = json_to_dot(json_data)
# graph.render('output_graph', format='png', cleanup=True)
# dot_content = graph.source
# with open('output_graph.dot', 'w') as dot_file:
#     dot_file.write(dot_content)

# 示例用法
json_data3 = {"a": {"b": {"c": 1}}, "d": [2, 3, 4]}
graph = json_to_dot_pdf(json_data2)
graph.render('output_graph', format='png', cleanup=True)
