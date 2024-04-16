reserved = {
    'main_func': 'MAIN_FUNCTION',
    'end_func': 'FUNCTION_END',
    'nil': 'NULL',
    'float': 'FLOAT',
    'integer': 'INTEGER',
    'string': 'STRING',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'otherwise': 'OTHERWISE',
    'end_if': 'END_IF',
    'for': 'FOR',
    'with': 'WITH',
    'limit': 'LIMIT',
    'end_for': 'END_FOR',
    'in': 'IN',
    'while': 'WHILE',
    'end_while': 'END_WHILE',
    'break': 'BREAK',
    'execute': 'EXECUTE',
    'print': 'PRINT',
    'ascend': 'ASCEND',
    'descend': 'DESCEND',
}

tokens = [
             'FLOAT_VALUE',
             'INTEGER_VALUE',
             'STRING_VALUE',
             'NULL_VALUE',
             'COMMENT',
             'OPEN_COMMENT',
             'CLOSED_COMMENT',
             'ADDITION',
             'SUBTRACTION',
             'MULTIPLICATION',
             'DIVISION',
             'EXPONENTIAL',
             'MODULUS',
             'INCREMENT',
             'DECREMENT',
             'EQUAL_TO',
             'LESS_THAN',
             'GREATER_THAN',
             'LESS_THAN_OR_EQUAL_TO',
             'GREATER_THAN_OR_EQUAL_TO',
             'NOT_EQUAL_TO',
             'AND',
             'OR',
             'NOT',
             'IDENTIFIER',
             'ASSIGNMENT',
             'LPAREN',
             'RPAREN',
             'LBRACKET',
             'RBRACKET',
             'LBRACE',
             'RBRACE',
             'QUOTE',
             'DOUBLE_QUOTE',
             'SEMICOLON',
             'COLON',
             'COMMA',
             'PERIOD',
         ] + list(reserved.values())

# Regular expression rules for other tokens within the language

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_QUOTE = r'\''
t_DOUBLE_QUOTE = r'\"'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_PERIOD = r'\.'
t_LESS_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_LESS_THAN_OR_EQUAL_TO = r'\<\='
t_GREATER_THAN_OR_EQUAL_TO = r'\>\='
t_NOT_EQUAL_TO = r'\!\='
t_EQUAL_TO = r'\=\='
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'\!'
t_ASSIGNMENT = r'\='
t_ADDITION = r'\+'
t_SUBTRACTION = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'\/'
t_EXPONENTIAL = r'\^'
t_MODULUS = r'\%'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'
t_OPEN_COMMENT = r'\!\-'
t_CLOSED_COMMENT = r'\-\!'


# -----------Regular Expressions----------- #
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


def t_STRING_VALUE(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_MULTI_LINE_COMMENT(t):
    r'\!\-.*?\-\!'
    pass


def t_SINGLE_LINE_COMMENT(t):
    r'!-.*?'
    pass


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


# Error handling rule
def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lineno}")
