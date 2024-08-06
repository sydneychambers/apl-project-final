import backend.src.arya_parser
import backend.src.tokens
from backend.src import tokens, arya_parser
from backend.src.arya_semantic_analyser import SemanticAnalyzer
from ply import lex

try:
    with open('backend/src/test_code.txt', 'r') as file:
        # Read the contents of the file
        file_contents = file.read()
except FileNotFoundError:
    print("Error: The file 'test_code.txt' was not found.")


def arya_compiler(source_code):
    # Build the lexer and pass it the source code
    lexer = lex.lex(module=tokens)
    lexer.input(str(source_code))

    # Print tokens generated by the lexer
    # for token in lexer:
    #     token_str = f"Token({token.type}, '{token.value}', line {token.lineno}, column {token.lexpos})"
    #     print(token_str)

    # Reset lexer for parser
    # lexer.input(source_code)

    # Parse the input
    parse_tree = arya_parser.parser.parse(lexer=lexer)
    print(parse_tree)

    # Create an instance of the semantic analyzer
    semantic_analyzer = SemanticAnalyzer()

    # Analyze the generated AST
    try:
        X = semantic_analyzer.analyze(parse_tree)
        # print(f"Semantic analysis successful.\n {X}")
        if X[1] is None:  # X[1] will only be !None if there are errors
            print(X[0])
            return X[0]
        else:  # return errors
            print(X[1])
            return X[1]
    except Exception as e:
        return f"Semantic analysis failed: \n {e}"

    # Pass the file contents to the compile function

# arya_compiler(file_contents)