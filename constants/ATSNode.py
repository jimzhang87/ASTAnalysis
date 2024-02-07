import json


class ASTNode:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f"{self.type} Node"


class Identifier(ASTNode):
    def __init__(self, name):
        super().__init__("Identifier")
        self.name = name

    def __repr__(self):
        return f"Identifier Node: {self.name}"


class Literal(ASTNode):
    def __init__(self, value, raw):
        super().__init__("Literal")
        self.value = value
        self.raw = raw

    def __repr__(self):
        return f"Literal Node: {self.value} (raw: {self.raw})"


class BinaryExpression(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("BinaryExpression")
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryExpression Node: {self.left} {self.operator} {self.right}"


class LogicalExpression(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("LogicalExpression")
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"LogicalExpression Node: ({self.left} {self.operator} {self.right})"


class CallExpression(ASTNode):
    def __init__(self, callee, arguments):
        super().__init__("CallExpression")
        self.callee = callee
        self.arguments = arguments

    def __repr__(self):
        return f"CallExpression Node: {self.callee}({', '.join(map(repr, self.arguments))})"


class MemberExpression(ASTNode):
    def __init__(self, object, property, computed=False):
        super().__init__("MemberExpression")
        self.object = object
        self.property = property
        self.computed = computed

    def __repr__(self):
        access_str = f"[{self.property}]" if self.computed else f".{self.property}"
        return f"MemberExpression Node: {self.object}{access_str}"


class IfStatement(ASTNode):
    def __init__(self, test, consequent, alternate=None):
        super().__init__("IfStatement")
        self.test = test
        self.consequent = consequent
        self.alternate = alternate

    def __repr__(self):
        alt_repr = f", alternate={self.alternate}" if self.alternate is not None else ""
        return f"IfStatement Node: test={self.test}, consequent={self.consequent}{alt_repr}"


class BlockStatement(ASTNode):
    def __init__(self, body):
        super().__init__("BlockStatement")
        self.body = body

    def __repr__(self):
        return f"BlockStatement Node: body=[{', '.join(map(repr, self.body))}]"


class Program(ASTNode):
    def __init__(self, sourceType, body):
        super().__init__("Program")
        self.sourceType = sourceType
        self.body = body


# 示例：解析并构建AST节点
json_ast_data = {"type": "Program", "sourceType": "script", "body": [{"type": "IfStatement",
                                                                      "test": {"type": "LogicalExpression",
                                                                               "operator": "&&",
                                                                               "left": {"type": "LogicalExpression",
                                                                                        "operator": "&&", "left": {
                                                                                       "type": "LogicalExpression",
                                                                                       "operator": "&&", "left": {
                                                                                           "type": "LogicalExpression",
                                                                                           "operator": "&&", "left": {
                                                                                               "type": "BinaryExpression",
                                                                                               "operator": "!=",
                                                                                               "left": {
                                                                                                   "type": "Identifier",
                                                                                                   "name": "$block_code_valid_alias"},
                                                                                               "right": {
                                                                                                   "type": "Literal",
                                                                                                   "value": None,
                                                                                                   "raw": "null"}},
                                                                                           "right": {
                                                                                               "type": "BinaryExpression",
                                                                                               "operator": "!=",
                                                                                               "left": {
                                                                                                   "type": "Identifier",
                                                                                                   "name": "$block_code_valid_alias"},
                                                                                               "right": {
                                                                                                   "type": "Literal",
                                                                                                   "value": "-2",
                                                                                                   "raw": "\"-2\""}}},
                                                                                       "right": {
                                                                                           "type": "CallExpression",
                                                                                           "callee": {
                                                                                               "type": "MemberExpression",
                                                                                               "computed": False,
                                                                                               "object": {
                                                                                                   "type": "Identifier",
                                                                                                   "name": "CommFunction"},
                                                                                               "property": {
                                                                                                   "type": "Identifier",
                                                                                                   "name": "contains"}},
                                                                                           "arguments": [
                                                                                               {"type": "Identifier",
                                                                                                "name": "$block_code_valid_alias"},
                                                                                               {"type": "Literal",
                                                                                                "value": "C163",
                                                                                                "raw": "'C163'"}]}},
                                                                                        "right": {
                                                                                            "type": "LogicalExpression",
                                                                                            "operator": "||", "left": {
                                                                                                "type": "LogicalExpression",
                                                                                                "operator": "&&",
                                                                                                "left": {
                                                                                                    "type": "BinaryExpression",
                                                                                                    "operator": ">",
                                                                                                    "left": {
                                                                                                        "type": "Identifier",
                                                                                                        "name": "$uid"},
                                                                                                    "right": {
                                                                                                        "type": "Literal",
                                                                                                        "value": 0,
                                                                                                        "raw": "0"}},
                                                                                                "right": {
                                                                                                    "type": "BinaryExpression",
                                                                                                    "operator": "<",
                                                                                                    "left": {
                                                                                                        "type": "Identifier",
                                                                                                        "name": "$uid"},
                                                                                                    "right": {
                                                                                                        "type": "Literal",
                                                                                                        "value": 3000000,
                                                                                                        "raw": "3000000"}}},
                                                                                            "right": {
                                                                                                "type": "BinaryExpression",
                                                                                                "operator": ">",
                                                                                                "left": {
                                                                                                    "type": "Identifier",
                                                                                                    "name": "$uid"},
                                                                                                "right": {
                                                                                                    "type": "Literal",
                                                                                                    "value": 5000000,
                                                                                                    "raw": "5000000"}}}},
                                                                               "right": {"type": "BinaryExpression",
                                                                                         "operator": "!=",
                                                                                         "left": {"type": "Identifier",
                                                                                                  "name": "$cs_kefu_risk_tag"},
                                                                                         "right": {"type": "Literal",
                                                                                                   "value": 1,
                                                                                                   "raw": "1"}}},
                                                                      "consequent": {"type": "BlockStatement", "body": [
                                                                          {"type": "ExpressionStatement",
                                                                           "expression": {"type": "CallExpression",
                                                                                          "callee": {
                                                                                              "type": "MemberExpression",
                                                                                              "computed": False,
                                                                                              "object": {
                                                                                                  "type": "Identifier",
                                                                                                  "name": "console"},
                                                                                              "property": {
                                                                                                  "type": "Identifier",
                                                                                                  "name": "log"}},
                                                                                          "arguments": [
                                                                                              {"type": "Literal",
                                                                                               "value": "#oper_decision=\"B30000\";#approval_result=2;",
                                                                                               "raw": "'#oper_decision=\"B30000\";#approval_result=2;'"}]}}]},
                                                                      "alternate": None}]}  # 提供的JSON数据


# ast_json = json.loads(json_ast_data)

def build_ast_node(node_data):
    node_type = node_data["type"]

    if node_type == "Identifier":
        return Identifier(name=node_data["name"])
    elif node_type == "Literal":
        return Literal(value=node_data["value"], raw=node_data["raw"])
    elif node_type == "BinaryExpression":
        return BinaryExpression(operator=node_data["operator"],
                                left=build_ast_node(node_data["left"]),
                                right=build_ast_node(node_data["right"]))
    elif node_type == "MemberExpression":
        return MemberExpression(object=node_data["object"],
                                property=node_data["property"],
                                computed=node_data.get("computed", False))
    elif node_type == "CallExpression":
        return CallExpression(callee=node_data["callee"],
                              arguments=node_data["arguments"])
    elif node_type == "LogicalExpression":
        return LogicalExpression(operator=node_data["operator"],
                                 left=build_ast_node(node_data["left"]),
                                 right=build_ast_node(node_data["right"]))
    elif node_type == "IfStatement":
        return IfStatement(test=node_data["test"],
                           consequent=node_data["consequent"],
                           alternate=node_data.get("alternate"))
    elif node_type == "BlockStatement":
        return BlockStatement(body=node_data["body"])
    # ... 其他复合节点的构造函数类似 ...


def build_ast_tree(json_ast):
    if json_ast["type"] == "Program":
        return Program(sourceType=json_ast["sourceType"], body=json_ast["body"])
    else:
        raise ValueError("Provided AST does not start with a Program node.")


# 构建整个AST
root_node = build_ast_tree(json_ast_data)
# print(root_node.body)
for i in root_node.body:
    a = build_ast_node(i)
    print(a)
