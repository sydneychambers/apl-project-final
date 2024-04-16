import ply.yacc as yacc
import ply.lex as lex
from backend.src.tokens import *

# Defines the START symbol for the grammar
start = 'main_func'

# Precedence rules for the operators
precedence = (
    ("left", "ADDITION", "SUBTRACTION", "MULTIPLICATION", "DIVISION", "MODULUS"),
    ("left", "EXPONENTIAL"),
)


def p_main_func(p):
    """
    main_func : MAIN_FUNCTION EXECUTE COLON LBRACE statement_list RBRACE FUNCTION_END
    """
    p[0] = ('main_func', p[5])


def p_statement_list(p):
    """
    statement_list : statement statement_list
                   | statement
    """
    if len(p) == 3:
        p[0] = ('statement_list', p[1], p[2])
    elif len(p) == 2:
        p[0] = ('statement_list', p[1])


def p_statement(p):
    """
    statement : expression
              | variable_declaration
              | variable_assignment
              | array_declaration
              | array_index_access
              | while_statement
              | do_while_statement
              | for_statement
              | if_statement
              | print_statement
              | empty
    """
    p[0] = p[1]


def p_if_statement(p):
    """
    if_statement : IF LPAREN condition_expression RPAREN EXECUTE COLON LBRACE statement_list RBRACE END_IF
                 | IF LPAREN condition_expression RPAREN EXECUTE COLON LBRACE statement_list RBRACE OTHERWISE IF LPAREN condition_expression RPAREN EXECUTE COLON LBRACE statement_list RBRACE END_IF
    """
    if len(p) == 11:
        p[0] = ('if_statement', p[3], p[8])
    elif len(p) == 21:
        p[0] = ('if_statement', p[3], p[8], p[13], p[18])


def p_for_statement(p):
    """
    for_statement : FOR variable_declaration WITH LIMIT INTEGER_VALUE ASCEND INTEGER_VALUE EXECUTE COLON LBRACE statement_list RBRACE END_FOR
                  | FOR variable_declaration WITH LIMIT INTEGER_VALUE DESCEND INTEGER_VALUE EXECUTE COLON LBRACE statement_list RBRACE END_FOR
    """
    p[0] = ('for_statement', p[2], p[5], p[6], p[7], p[11])


def p_print_statement(p):
    """
    print_statement : PRINT LPAREN STRING_VALUE RPAREN SEMICOLON
                    | PRINT LPAREN STRING_VALUE ADDITION expression RPAREN SEMICOLON
    """
    if len(p) == 8:
        p[0] = ('print_statement', p[3], p[5])
    elif len(p) == 6:
        p[0] = ('print_statement', p[3])


def p_do_while_statement(p):
    """
    do_while_statement : EXECUTE COLON LBRACE statement_list RBRACE WHILE LPAREN condition_expression RPAREN
    """
    p[0] = ('do_while_statement', p[4], p[8])


def p_while_statement(p):
    """
    while_statement : WHILE LPAREN condition_expression RPAREN EXECUTE COLON LBRACE statement_list RBRACE END_WHILE
    """
    p[0] = ('while_statement', p[3], p[8])


def p_variable_declaration(p):
    """
    variable_declaration : datatype variable_assignment
    """
    p[0] = ('variable_declaration', p[1], p[2])


def p_variable_assignment(p):
    """
    variable_assignment : identifier SEMICOLON
                        | identifier ASSIGNMENT expression SEMICOLON
    """
    if len(p) == 5:
        p[0] = ('variable_assignment', p[1], p[3])
    elif len(p) == 3:
        p[0] = p[1]


def p_array_declaration(p):
    """
    array_declaration : datatype identifier LBRACKET INTEGER_VALUE RBRACKET SEMICOLON
                      | datatype identifier LBRACKET INTEGER_VALUE RBRACKET ASSIGNMENT LBRACKET array_value_list RBRACKET SEMICOLON
    """
    if len(p) == 7:
        p[0] = ('array_declaration', p[1], p[2], p[4])
    elif len(p) == 11:
        p[0] = ('array_declaration', p[1], p[2], p[4], p[8])


def p_array_value_list(p):
    """
    array_value_list : datavalue COMMA array_value_list
                     | datavalue
    """
    if len(p) == 4:
        p[0] = ('array_value_list', p[1], p[3])
    if len(p) == 2:
        p[0] = ('array_value_list', p[1])


def p_array_index_access(p):
    """
    array_index_access : identifier LBRACKET INTEGER_VALUE RBRACKET
    """
    p[0] = ('array_index_access', p[1], p[3])


def p_expression(p):
    """
    expression : condition_expression
                | expression ADDITION expression
                | expression SUBTRACTION expression
                | expression MULTIPLICATION expression
                | expression DIVISION expression
                | expression EXPONENTIAL expression
                | expression MODULUS expression
                | datavalue INCREMENT
                | datavalue DECREMENT
                | datavalue
                | array_index_access
    """
    if len(p) == 4:
        p[0] = ('expression', p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ('expression', p[2], p[1])
    else:
        p[0] = p[1]


def p_condition_expression(p):
    """
    condition_expression  : expression EQUAL_TO expression
                        | expression LESS_THAN expression
                        | expression GREATER_THAN expression
                        | expression LESS_THAN_OR_EQUAL_TO expression
                        | expression GREATER_THAN_OR_EQUAL_TO expression
                        | expression NOT_EQUAL_TO expression
    """
    p[0] = ('condition_expression ', p[2], p[1], p[3])


def p_datatype(p):
    """
    datatype : FLOAT
             | INTEGER
             | STRING
    """
    p[0] = p[1]


def p_datavalue(p):
    """
    datavalue : FLOAT_VALUE
             | INTEGER_VALUE
             | STRING_VALUE
             | identifier
    """
    p[0] = p[1]


def p_indentifier(p):
    """
    identifier : IDENTIFIER
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    pass


def p_error(p):
    if p:
        pos = p.lexpos  # Get the position of the token in the input string
        # Find the position of the nearest preceding newline character
        line_start = p.lexer.lexdata.rfind('\n', 0, pos) + 1
        # Find the position of the next newline character
        line_end = p.lexer.lexdata.find('\n', pos)
        # If there's no newline character after the token, set line_end to the end of the input string
        if line_end == -1:
            line_end = len(p.lexer.lexdata)
        # Calculate the line number by counting the number of newline characters before the token
        line_number = p.lexer.lexdata.count('\n', 0, line_start) + 1
        raise SyntaxError(f"Illegal character '{p.value}' at line {line_number}")
    else:
        raise SyntaxError("Syntax Error: Unexpected end of file")


# Build the parser
parser = yacc.yacc()
