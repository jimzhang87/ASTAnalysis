import ast
import os

current_file = os.path.abspath(__file__)
# print(current_file)
current_directory = os.path.dirname(current_file)
# print(current_directory)
project_root = os.path.dirname(current_directory)
# print(project_root)
os.chdir(project_root)
def read_ast_file(file_path):
   with open(file_path, 'r') as file:
        source_code = file.read()
        # print(source_code)
        return ast.parse(str(source_code))


# ast_obj = read_ast_file('example.py':
# 定义一个访问者类，用于遍历抽象语法树并打印逻辑关系
class LogicVisitor(ast.NodeVisitor):
    def visit_If(self, node):
        print(f"Found an 'if' statement with test: {ast.dump(node.test)}")
        self.generic_visit(node)

# 创建访问者实例并应用于抽象语法树
# logic_visitor = LogicVisitor()
# logic_visitor.visit(ast_obj)

if __name__ == '__main__':
    a = read_ast_file('outputData/rule_id:1542040.json')
    print(a)
    logic_visitor = LogicVisitor()
    logic_visitor.visit(a)
