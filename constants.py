from string import ascii_letters

TT_INT      = "INT"
TT_FLOAT    = "FLOAT"
TT_PLUS     = "PLUS"
TT_MINUS    = "MINUS"
TT_MUL      = "MUL"
TT_DIV      = "DIV"
TT_LPAREN   = "LPAREN"
TT_RPAREN   = "RPAREN"
TT_EOF      = "EOF"
TT_POWER    = "POWER"
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_EQ = 'EQ'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'

DIGITS = '0123456789'
LETTERS = ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

KEYWORDS = [
    'VAR',
    'AND',
    'OR',
    'NOT',
    'IF',
    'THEN',
    'ELIF',
    'ELSE',
    'REPL_EXIT',
    'FOR',
    'TO',
    'STEP',
    'THEN',
    'WHILE',
    'THEN'
]
