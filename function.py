from value import Value
from runtime_result import RTResult
import interpreter as inter
from symbols import SymbolTable
from context import Context
from errors import RTError

class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or "anonymous"
        self.body_node = body_node
        self.arg_names = arg_names
    
    def execute(self, args):
        res = RTResult()
        interpreter = inter.Interpreter()

        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) < len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"'{len(self.arg_names) - len(args)}' less args than expected passed into '{self.name}",
                self.context
            ))

        if len(args) > len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"'{len(args) - len(self.arg_names)}' more args than expected passed into '{self.name}",
                self.context
            ))
        
        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)
        
        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error: return res
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)

        return copy

    def __repr__(self):
        return f'<function {self.name}>'