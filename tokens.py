
##################################
# TOKENS
##################################

class Token:
    def __init__(self, type__, value=None, pos_start=None, pos_end=None):
        self.type = type__
        self.value = value

        if pos_start: 
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()
    
    def matches(self, type__, value):
        return self.type == type__ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
