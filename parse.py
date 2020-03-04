from constants import *
from tokens import Token
from errors import *
from nodes import *
##################################
# PARSING
##################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node


    def register_advancement(self):
        self.advance_count += 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected +, -, *, or /'
            ))
        return res

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT): 
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Expected )'
            ))
        
        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'FUN'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(IllegalSyntaxError(
            tok.pos_start, tok.pos_end,
            'Excepted IF, FOR, WHILE, FUN, int, float, indentifier, +, -, ('
        ))

    def func_def(self):
        res = ParseResult()

        # check for FUN in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'FUN'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted FUN \n'
            ))

        #advance one index in tokens
        res.register_advancement()
        self.advance()

        # check if a function name as given
        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            
            #advance one index in tokens
            res.register_advancement()
            self.advance()

            # check for ( in tokens, raise error if not found
            if self.current_tok.type != TT_LPAREN:
                return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Excepted ( \n'
                ))  

        else:

            # set function name to None
            var_name_tok = None

            # check for (
            if self.current_tok.type != TT_LPAREN:
                return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Excepted ( \n'
                ))   
           
        #advance one index in tokens
        res.register_advancement()
        self.advance()  

        arg_name_toks = []
        
        # check for identifier
        if self.current_tok.type == TT_IDENTIFIER:
            
            # add to arguments
            arg_name_toks.append(self.current_tok)
            
            #advance one index in tokens
            res.register_advancement()
            self.advance()          

            # while current token is a comma
            while self.current_tok.type == TT_COMMA:
                
                #advance one index in tokens
                res.register_advancement()
                self.advance()  
                
                # check for identifier
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(IllegalSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        'Excepted Identifier \n'
                    ))  
                
                # append argument token
                arg_name_toks.append(self.current_tok)
                #advance one index in tokens
                res.register_advancement()
                self.advance()     
            
            # check for )
            if self.current_tok.type != TT_RPAREN:
                return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Excepted , or ) \n'
                ))   
        else:
            
            # check for ) if empty arguments
            if self.current_tok.type != TT_RPAREN:
                return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Excepted Identifier or ) \n'
                ))         

        #advance one index in tokens
        res.register_advancement()
        self.advance()   

        # check for ->
        if self.current_tok.type != TT_ARROW:
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted -> \n'
            ))  
        
        #advance one index in tokens
        res.register_advancement()
        self.advance()   

        # pass function body into node_to_return
        node_to_return = res.register(self.expr())
        if res.error: return res

        # return sucessful FuncDefNode
        return res.success(FuncDefNode(var_name_tok, arg_name_toks, node_to_return))   

    def call (self):
        res = ParseResult()

        # check for an atom
        atom = res.register(self.atom())
        if res.error: return res

        # check for ( in tokens
        if self.current_tok.type == TT_LPAREN:

            #advance one index in tokens
            res.register_advancement()
            self.advance()
            
            arg_nodes = []

            # check for an empty body
            if self.current_tok.type == TT_RPAREN:
                    
                #advance one index in tokens
                res.register_advancement()
                self.advance()  
            else:

                # add the expression to arg_nodes
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(IllegalSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        'Excepted ), or the beginnig of an expression (i.e. VAR/IF int/float) \n'
                    ))                   

                # while there is a comma
                while self.current_tok.type == TT_COMMA:
                    #advance one index in tokens
                    res.register_advancement()
                    self.advance()  

                    # add expression to arg_nodes
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
                
                if self.current_tok.type != TT_RPAREN:
                    return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Excepted ) \n'
                    ))                   

                #advance one index in tokens
                res.register_advancement()
                self.advance()  

            # return either a sucessfull CallNode or atom
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def power(self):
        return self.bin_op(self.call, (TT_POWER, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()
        
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE) ))

        if res.error:
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted int, float, indentifier, +, -, (, NOT'
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        # check for IF in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted IF'
            ))

        #advance one index in tokens
        res.register_advancement()
        self.advance()

        #check if the expression is valid
        condition = res.register(self.expr())
        if res.error: return res

        # check for THEN in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted THEN'
            ))     

        #advance one index in tokens
        res.register_advancement()
        self.advance()

        # check for THEN in tokens, raise error if not found
        # append the condition and expression to cases
        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        # if the next token is ELIF, loop the above code again 
        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Excepted THEN'
                ))     

            res.register_advancement()
            self.advance()
        
            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))
        
        # if the next token is ELSE, set the else_case to the expression
        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()         
        
            expr = res.register(self.expr())
            if res.error: return res
            else_case = expr 

        # return a successfull IfNode object
        return res.success(IfNode(cases, else_case))

    def for_expr(self):
        res = ParseResult()

        # check for FOR in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted FOR \n'
            ))

        # advance one index in tokens
        res.register_advancement()
        self.advance()

        # check if current token is an IDENTIFIER, raise error if not 
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted Identifier \n'
            ))     

        # set var_name to current token
        # advance one index in tokens
        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        # check if current token is '=', raise error if not 
        if self.current_tok.type != TT_EQ:
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Excepted '=' \n"
            ))     

        # advance one index in tokens
        res.register_advancement()
        self.advance()

        # check if the expression is valid
        # set start_value to the expression
        start_value = res.register(self.expr())
        if res.error: return res

        # check for TO in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted TO \n'
            ))     

        # advance one index in tokens
        res.register_advancement()
        self.advance()

        # check if the expression is valid
        # set end_value to the expression
        end_value = res.register(self.expr())
        if res.error: return res

        # check for STEP in tokens, evaluate expression if found
        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            # advance one index in tokens
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None  
        # check for THEN in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted THEN \n'
            ))     
        
        # advance one index in tokens
        res.register_advancement()
        self.advance()

        # set expr to the expression if no errors
        body = res.register(self.expr())
        if res.error: return res

        # return a successfull ForNode object
        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParseResult()

        # check for WHILE in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted WHILE \n'
            ))
        
         # advance one index in tokens
        res.register_advancement()
        self.advance()

        # check if the expression is valid
        # set condition to the expression
        condition = res.register(self.expr())
        if res.error: return res             

        # check for THEN in tokens, raise error if not found
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(IllegalSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                'Excepted THEN \n'
            ))
        
        # advance one index in tokens
        res.register_advancement()
        self.advance()

        # check if the expression is valid
        # set condition to the expression
        body = res.register(self.expr())
        if res.error: return res            

        # return a successfull ForNode object
        return res.success(WhileNode(condition, body))

    def expr(self):
        res = ParseResult()

        # Check if the token is VAR
        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            
            # Advance one token
            res.register_advancement()
            self.advance()

            # Check if the token is an IDENTIFIER
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Exepected identifier'
                ))
            
            # Set the variable name to the IDENTIFIER token and advance
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            # check if the token is '='
            if self.current_tok.type != TT_EQ:
                 return res.failure(IllegalSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Exepected equals'
                ))     

            # Advance one token and evaluate the expression
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())

            # Return a new VarAssignNode if there are no errors
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        # If the Token is REPL_EXIT then exit the REPL 
        if self.current_tok.matches(TT_KEYWORD, 'REPL_EXIT'):
            exit()

        # The token must be either AND or OR
        node =  res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR') )))

        # Return successful node if no errors
        if res.error:
            return res.failure(IllegalSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            'Exepected IF, FOR, WHILE, FUN, VAR, int, float, indentifier, +, -, or ( \n'
        ))     

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        
        # If func_b is None, set it to func_a
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        
        # Run func_a and check for error
        left = res.register(func_a())
        if res.error: return res

        # Loop while there are still tokens to parse
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops: #not fast
            # Store current token
            op_tok = self.current_tok
            
            # Advance one token
            res.register_advancement()
            self.advance()
            
            # Run func_b and check for error
            # Set the result to right
            right = res.register(func_b())
            if res.error: return res
            
            # Set left to a new BinOpNode
            left = BinOpNode(left, op_tok, right)    
        
        return res.success(left)
