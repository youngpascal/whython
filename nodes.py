##################################
# NODES
##################################  
class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'{self.op_tok}, {self.node}'

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        # set pos_start to the first element of the first tuple, which is expression #1
        self.pos_start = self.cases[0][0].pos_start
        # set pos_end to the else_case if there is one, otherwise the last cases' expression
        self.pos_end = self.else_case or self.cases[len(self.cases) - 1][0].pos_end

class ForNode:
    def __init__(self, var_name, start_value, end_value, step_value, body):
        self.var_name = var_name
        self.start_value = start_value
        self.end_value = end_value
        self.step_value = step_value
        self.body = body

        self.pos_start = self.var_name.pos_start

        self.pos_end = self.body.pos_end

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

        self.pos_start = self.condition.pos_start

        self.pos_end = self.body.pos_end

class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_tok, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_tok = arg_name_tok
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_tok) > 0:
            self.pos_start = self.arg_name_tok[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

  