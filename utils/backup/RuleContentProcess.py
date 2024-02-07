import json
import os
import re
current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)
from packageProcessScirpt import strategy_node_flow_rule_info_data

pattern = r'"([^"]*)"'


def rule_content_process(rule_content):
    for line in rule_content:
        # print(eval(line))
        # print(rule_content['rule_content'])
        matches = re.findall(pattern, line)
        # print(type(matches))
        # print(matches)
        for match in matches:
            if match.strip(','):
                print(match)
                return match


if __name__ == '__main__':
    with open('outputData/ruleDetailInfo.json', 'r', encoding='utf-8') as f:
        rule_content = json.load(f)
    for i in strategy_node_flow_rule_info_data.find_strategy_node_flow_rule_info():
        rule_data = i['rule_data']
        print(type(rule_data))
        rule_content = rule_data['rule_content']
        print(type(rule_content))
        print(rule_content)
        a = rule_content_process(rule_content)
        print(a)
