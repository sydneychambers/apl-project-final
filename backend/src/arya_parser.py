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

# def p_program(p):
#     """
#     program : function_list main_func
#     """
#     p[0] = ('program', p[1], p[2])
#
# def p_function_list(p):
#     """
#     function_list : function function_list
#                   | function
#                   | empty
#     """
#     if len(p) == 3:
#         p[0] = ('function_list', p[1], p[2])
#     elif len(p) == 2:
#         p[0] = ('function_list', p[1])

def p_main_func(p):
    """
    main_func : MAIN_FUNCTION EXECUTE COLON statement_list FUNCTION_END
    """
    p[0] = ('main_func', p[4])


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
              | for_statement
              | if_statement
              | print_statement
              | return_statement
              | empty
    """
    p[0] = p[1]

# def p_function(p):
#     """
#     function : FUNCTION_DEFINITION IDENTIFIER EXECUTE COLON statement_list FUNCTION_END
#             | FUNCTION_DEFINITION IDENTIFIER LPAREN datatype datavalue RPAREN EXECUTE COLON statement_list FUNCTION_END
#     """
#     if len(p) == 7:
#         p[0] = ('function', p[2], p[5])
#     elif len(p) == 11:
#         p[0] = ('function', p[2], p[4], p[5], p[9])
#
# def p_function_call(p):
#     """
#     function_call : IDENTIFIER LPAREN datavalue RPAREN
#     """
#     p[0] = ('function_call', p[1], p[3])

def p_if_statement(p):
    """
    if_statement : IF LPAREN condition_expression RPAREN EXECUTE COLON statement_list END_IF
                | IF LPAREN condition_expression RPAREN EXECUTE COLON statement_list OTHERWISE COLON statement_list END_IF
                | IF LPAREN condition_expression RPAREN EXECUTE COLON statement_list OTHERWISE IF LPAREN condition_expression RPAREN EXECUTE COLON statement_list END_IF
    """
    if len(p) == 9:
        p[0] = ('if_statement', p[3], p[7])
    elif len(p) == 12:
        p[0] = ('if_statement', p[3], p[7], p[10])
    elif len(p) == 17:
        p[0] = ('if_statement', p[3], p[7], p[11], p[15])


def p_for_statement(p):
    """
    for_statement : FOR variable_declaration WITH LIMIT datavalue ASCEND INTEGER_VALUE EXECUTE COLON statement_list END_FOR
                  | FOR variable_declaration WITH LIMIT datavalue DESCEND INTEGER_VALUE EXECUTE COLON statement_list END_FOR
    """
    p[0] = ('for_statement', p[2], p[5], p[6], p[7], p[10])


def p_print_statement(p):
    """
    print_statement : PRINT LPAREN print_list RPAREN SEMICOLON
    """
    p[0] = ('print_statement', p[3])

def p_print_list(p):
    """
    print_list : expression
               | STRING_VALUE
               | expression COMMA print_list
               | STRING_VALUE COMMA expression
               | STRING_VALUE COMMA print_list
               | STRING_VALUE COMMA expression COMMA print_list
    """
    if len(p) == 2:
        p[0] = ('print_list', p[1])
    elif len(p) == 4:
        p[0] = ('print_list', p[1], p[3])
    elif len(p) == 6:
        p[0] = ('print_list', p[1], p[3], p[5])

def p_while_statement(p):
    """
    while_statement : WHILE LPAREN condition_expression RPAREN EXECUTE COLON statement_list END_WHILE
    """
    p[0] = ('while_statement', p[3], p[7])

def p_return_statement(p):
    """
    return_statement : RETURN statement SEMICOLON
    """
    p[0] = ('return_statement', p[2])


def p_variable_declaration(p):
    """
    variable_declaration : datatype IDENTIFIER SEMICOLON
                         | datatype IDENTIFIER ASSIGNMENT expression SEMICOLON
    """
    if len(p) == 4:
        p[0] = ('variable_declaration', p[1], p[2])
    elif len(p) == 6:
        p[0] = ('variable_declaration', p[1], p[2], p[4])


def p_variable_assignment(p):
    """
    variable_assignment : IDENTIFIER ASSIGNMENT expression SEMICOLON
                        | array_index_access ASSIGNMENT expression SEMICOLON
    """
    p[0] = ('variable_assignment', p[1], p[3])



def p_array_declaration(p):
    """
    array_declaration : datatype IDENTIFIER LBRACKET INTEGER_VALUE RBRACKET SEMICOLON
                      | datatype IDENTIFIER LBRACKET INTEGER_VALUE RBRACKET ASSIGNMENT LBRACKET array_value_list RBRACKET SEMICOLON
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
    array_index_access : IDENTIFIER LBRACKET INTEGER_VALUE RBRACKET
                       | IDENTIFIER LBRACKET IDENTIFIER RBRACKET
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
    condition_expression  : condition_expression AND condition_expression
                         | condition_expression OR condition_expression
                         | NOT expression
                         | expression EQ expression
                         | expression LT expression
                         | expression GT expression
                         | expression LE expression
                         | expression GE expression
                         | expression NE expression
    """
    if len(p) == 4:
        p[0] = ('condition_expression', p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ('condition_expression', p[1], p[2])
    else:
        p[0] = p[1]


def p_datatype(p):
    """
    datatype : FLOAT
             | INTEGER
             | STRING
             | BOOLEAN
    """
    p[0] = p[1]


def p_datavalue(p):
    """
    datavalue : FLOAT_VALUE
             | INTEGER_VALUE
             | STRING_VALUE
             | NULL_VALUE
             | IDENTIFIER
             | TRUE
             | FALSE
             | array_index_access
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