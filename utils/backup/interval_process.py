class ValueList:
    def __init__(self, values=None):
        """
        初始化一个值列表对象。

        :param values: 初始值列表，默认为 None。
        """
        self.values = [] if values is None else list(values)

    def add_value(self, value):
        """
        添加一个值到列表中。

        :param value: 要添加的值。
        """
        self.values.append(value)

    def remove_value(self, value):
        """
        从列表中移除一个值（如果存在）。

        :param value: 要移除的值。
        """
        if value in self.values:
            self.values.remove(value)

    def contains(self, value):
        """
        检查列表是否包含指定的值。

        :param value: 要检查的值。
        :return: 如果包含则返回 True，否则返回 False。
        """
        return value in self.values

    def __repr__(self):
        """
        返回表示值列表实例的字符串形式。

        :return: 字符串形式的值列表表示。
        """
        return f"ValueList({self.values})"


class ValueRange:
    def __init__(self, lower=None, upper=None, operator='<'):
        """
        初始化一个值范围对象。

        :param lower: 下限，默认为 None。
        :param upper: 上限，默认为 None。
        :param operator: 比较符，默认为 '<'（表示小于）；也可以是 '>'（表示大于）。
        """
        self.lower = lower
        self.upper = upper

        # 根据比较符自动填充无限大或0
        if operator == '<':
            if self.upper is None:
                self.upper = float('inf')
        elif operator == '>':
            if self.lower is None:
                self.lower = 0
        else:
            raise ValueError("Invalid operator. Only '<' and '>' are allowed.")

    def contains(self, value):
        """
        判断给定的值是否在这个范围内。

        :param value: 要检查的值。
        :return: 如果值在这个范围内则返回 True，否则返回 False。
        """
        if self.operator == '<':
            return self.lower <= value < self.upper
        elif self.operator == '>':
            return self.lower < value <= self.upper
        else:
            raise ValueError("Invalid operator during checking the range.")

    def __repr__(self):
        """
        返回表示值范围实例的字符串形式。

        :return: 字符串形式的值范围表示。
        """
        if self.operator == '<':
            upper_str = f"{self.upper} (if finite)" if self.upper == float('inf') else str(self.upper)
        elif self.operator == '>':
            lower_str = "0" if self.lower == 0 else str(self.lower)
        return f"ValueRange({lower_str}, {upper_str}, operator='{self.operator}')"


class OperatorDict:
    def __init__(self, operator_dict=None):
        """
        初始化一个操作符字典对象。

        :param operator_dict: 初始操作符字典，默认为 None。
        """
        self.operator_dict = {} if operator_dict is None else operator_dict

    def add_operator(self, operator, value):
        """
        添加一个操作符和值到字典中。

        :param operator: 操作符。
        :param value: 操作符对应的值。
        """
        self.operator_dict[operator] = value


class KeyDict:
    def __init__(self, key_dict=None):
        """
        初始化一个操作符字典对象。

        :param operator_dict: 初始操作符字典，默认为 None。
        """
        self.key_dict = {} if key_dict is None else key_dict

    def add_operator(self, key, opertaor_list):
        """
        添加一个操作符和值到字典中。

        :param key:
        :param opertaor_list:
        """
        self.key_dict[key] = opertaor_list

class InputDict:
    def __init__(self, input_dict=None):
        """
        初始化一个输入字典对象。

        :param input_dict: 初始输入字典，默认为 None。
        """
        self.input_dict = {} if input_dict is None else input_dict

    def add_input(self, input_name, input_value):
        """
        添加一个输入和值到字典中。

        :param input_name: 输入名称。
        :param input_value: 输入对应的值。
        """
        self.input_dict[input_name] = input_value

# 假设 get_logical_expressions 方法从语法树中获取所有逻辑表达式节点
def find_type_logic(ast_node, target_type):
    result = []

    def recursive_search(node, parent_type=None, parent_operator=None):
        if isinstance(node, dict):
            if "type" in node:
                # print('----------',node)
                current_type = node["type"]
                if "operator" in node:
                    current_operator = node['operator']
                else:
                    current_operator = None
                if current_type == target_type:
                    result.append({"type": current_type, "parent_type": parent_type, 'parent_operator': parent_operator,
                                   "logic": node})
                for key, value in node.items():
                    recursive_search(value, current_type, current_operator)

        elif isinstance(node, list):
            for item in node:
                recursive_search(item, parent_type)

    recursive_search(ast_node)
    return result


def interpret_expression(node):
    if node['type'] == 'Identifier':
        return node['name']
    elif node['type'] == 'Literal':
        return node['value']


def extract_intervals(logical_expressions):
    intervals = []
    value_list = ValueList()
    for expr in logical_expressions:
        logic = expr['logic']

        operator = logic['operator']
        left_value_name = interpret_expression(logic['left'])
        right_value = interpret_expression(logic['right'])
        if intervals.__contains__(left_value_name):
            print('True')
            value_list.add_value(right_value)
        # else:
        #     value_list.__init__()
        # 只关注 < 和 > 的区间条件
        # if operator not in ['<', '>']:
        #     continue

        if operator == '>':
            intervals.append((left_value_name, operator, value_list))
        elif operator == '<':
            intervals.append((left_value_name, operator, value_list))
        else:  # 包括 '=' 和其他非区间操作符
            intervals.append((left_value_name, operator, value_list))

    return intervals


def merge_intervals(intervals):
    variable_intervals = {}

    for var_name, lower_bound, upper_bound in intervals:
        if var_name not in variable_intervals:
            variable_intervals[var_name] = []

        # 添加新的边界到对应变量的区间列表中
        if lower_bound is not None:
            variable_intervals[var_name].append((lower_bound, True))
        if upper_bound is not None:
            variable_intervals[var_name].append((upper_bound, False))

    # 合并每个变量的区间
    for var_name, bounds in variable_intervals.items():
        merged_bounds = []
        current_lower = float('-inf')

        for bound, is_lower in sorted(bounds):
            if is_lower:
                # 更新当前下限
                current_lower = bound
            else:
                # 如果遇到上限并且与当前下限不连续，则添加区间
                if bound > current_lower:
                    merged_bounds.append((current_lower, bound))
                # 更新当前下限为新的上限（如果有连续区间）
                current_lower = bound

        # 处理最后一个区间（如果有的话）
        if current_lower != float('-inf'):
            merged_bounds.append((current_lower, float('inf')))

        # 将区间转换为 (lower, upper) 形式
        variable_intervals[var_name] = [(interval[0], interval[1]) for interval in merged_bounds]

    return variable_intervals


# 使用您的AST数据
ast_data = [{
    'type': 'BinaryExpression',
    'parent_type': 'LogicalExpression',
    'parent_operatpr': '&&',
    'logic': {
        'type': 'BinaryExpression',
        'operator': '!=',
        'left': {
            'type': 'Identifier',
            'name': '$block_code_valid_alias'
        },
        'right': {
            'type': 'Literal',
            'value': None,
            'raw': 'null'
        }
    }
}, {
    'type': 'BinaryExpression',
    'parent_type': 'LogicalExpression',
    'parent_operatpr': '&&',
    'logic': {
        'type': 'BinaryExpression',
        'operator': '!=',
        'left': {
            'type': 'Identifier',
            'name': '$block_code_valid_alias'
        },
        'right': {
            'type': 'Literal',
            'value': '-2',
            'raw': '"-2"'
        }
    }
}, {
    'type': 'BinaryExpression',
    'parent_type': 'LogicalExpression',
    'parent_operatpr': '&&',
    'logic': {
        'type': 'BinaryExpression',
        'operator': '>',
        'left': {
            'type': 'Identifier',
            'name': '$uid'
        },
        'right': {
            'type': 'Literal',
            'value': 0,
            'raw': '0'
        }
    }
}, {
    'type': 'BinaryExpression',
    'parent_type': 'LogicalExpression',
    'parent_operatpr': '&&',
    'logic': {
        'type': 'BinaryExpression',
        'operator': '<',
        'left': {
            'type': 'Identifier',
            'name': '$uid'
        },
        'right': {
            'type': 'Literal',
            'value': 3000000,
            'raw': '3000000'
        }
    }
}, {
    'type': 'BinaryExpression',
    'parent_type': 'LogicalExpression',
    'parent_operatpr': '||',
    'logic': {
        'type': 'BinaryExpression',
        'operator': '>',
        'left': {
            'type': 'Identifier',
            'name': '$uid'
        },
        'right': {
            'type': 'Literal',
            'value': 5000000,
            'raw': '5000000'
        }
    }
}, {
    'type': 'BinaryExpression',
    'parent_type': 'LogicalExpression',
    'parent_operatpr': '&&',
    'logic': {
        'type': 'BinaryExpression',
        'operator': '!=',
        'left': {
            'type': 'Identifier',
            'name': '$cs_kefu_risk_tag'
        },
        'right': {
            'type': 'Literal',
            'value': 1,
            'raw': '1'
        }
    }
}]

intervals = extract_intervals(ast_data)
# merged_variable_intervals = merge_intervals(intervals)
print(intervals)


# print(merged_variable_intervals)
# formatted_result = {var: list(map(tuple, merged)) for var, merged in merged_variable_intervals.items()}
# print(formatted_result)
# 示例使用：
class InnerClass:
    def __init__(self, inner_value):
        self.inner_value = inner_value

    def display_inner(self):
        return f"Inner value: {self.inner_value}"


class OuterClass:
    def __init__(self, outer_value, inner_instance=None):
        self.outer_value = outer_value
        self.inner = inner_instance if inner_instance is not None else InnerClass(0)

    def set_inner(self, new_inner):
        self.inner = new_inner

    def display_outer_and_inner(self):
        return f"Outer value: {self.outer_value}, Inner: {self.inner.display_inner()}"


# 示例用法：
inner_obj = InnerClass("Hello")
outer_obj = OuterClass("World", inner_instance=inner_obj)

print(outer_obj.display_outer_and_inner())

new_inner = InnerClass("New Inner Value")
outer_obj.set_inner(new_inner)
print(outer_obj.display_outer_and_inner())
