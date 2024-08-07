reserved = {
    'main_func': 'MAIN_FUNCTION',
    'func': 'FUNCTION_DEFINITION',
    'end_func': 'FUNCTION_END',
    'nil': 'NULL_VALUE',
    'float': 'FLOAT',
    'integer': 'INTEGER',
    'string': 'STRING',
    'if': 'IF',
    'otherwise': 'OTHERWISE',
    'end_if': 'END_IF',
    'for': 'FOR',
    'with': 'WITH',
    'limit': 'LIMIT',
    'end_for': 'END_FOR',
    'while': 'WHILE',
    'end_while': 'END_WHILE',
    'execute': 'EXECUTE',
    'print': 'PRINT',
    'ascend': 'ASCEND',
    'descend': 'DESCEND',
    'boolean': 'BOOLEAN',
    'True': 'TRUE',
    'False': 'FALSE',
    'return': 'RETURN'
}

tokens = [
    'FLOAT_VALUE',
    'INTEGER_VALUE',
    'STRING_VALUE',
    'ADDITION',
    'SUBTRACTION',
    'MULTIPLICATION',
    'DIVISION',
    'EXPONENTIAL',
    'MODULUS',
    'INCREMENT',
    'DECREMENT',
    'EQ',
    'LT',
    'GT',
    'LE',
    'GE',
    'NE',
    'AND',
    'OR',
    'NOT',
    'IDENTIFIER',
    'ASSIGNMENT',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'QUOTE',
    'DOUBLE_QUOTE',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'PERIOD',
] + list(reserved.values())

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore spaces and tabs that are not part of any token
t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_FLOAT_VALUE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER_VALUE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NULL_VALUE(t):
    r'nil'
    return t

def t_STRING_VALUE(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

def t_SINGLE_LINE_COMMENT(t):
    r'!-.*'
    pass

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t

def t_QUOTE(t):
    r'\''
    return t

def t_DOUBLE_QUOTE(t):
    r'\"'
    return t

def t_SEMICOLON(t):
    r'\;'
    return t

def t_COLON(t):
    r'\:'
    return t

def t_COMMA(t):
    r'\,'
    return t

def t_PERIOD(t):
    r'\.'
    return t

def t_LT(t):
    r'\<'
    return t

def t_GT(t):
    r'\>'
    return t

def t_LE(t):
    r'\<\='
    return t

def t_GE(t):
    r'\>\='
    return t

def t_NE(t):
    r'\!\='
    return t

def t_EQ(t):
    r'\=\='
    return t

def t_AND(t):
    r'\&\&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NOT(t):
    r'\!'
    return t

def t_ASSIGNMENT(t):
    r'\='
    return t

def t_ADDITION(t):
    r'\+'
    return t

def t_SUBTRACTION(t):
    r'\-'
    return t

def t_MULTIPLICATION(t):
    r'\*'
    return t

def t_DIVISION(t):
    r'\/'
    return t

def t_EXPONENTIAL(t):
    r'\^'
    return t

def t_MODULUS(t):
    r'\%'
    return t

def t_INCREMENT(t):
    r'\+\+'
    return t

def t_DECREMENT(t):
    r'\-\-'
    return t

# Error handling rule
def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lineno}")