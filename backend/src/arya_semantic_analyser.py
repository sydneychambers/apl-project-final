class SemanticAnalyzer:

    def __init__(self):
        self.function_registry = {}
        self.symbol_table = {}
        self.output = ""

    def analyze(self, ast):
        try:
            self.visit(ast)
            return self.output, None
        except Exception as e:
            return self.output, str(e)

    def visit(self, node):
        method_name = 'visit_' + node[0]
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(*node[1:])
        else:
            raise NotImplementedError(f"Method {method_name} not implemented")

    # def visit_program(self, function_list, main_func):
    #     # Process the function definitions
    #     self.visit(function_list)
    #     # Process the main function
    #     self.visit(main_func)

    def visit_main_func(self, statement_list):
        self.visit(statement_list)

    # def visit_function_list(self, function_list):
    #     if function_list is not None:
    #         for function in function_list:
    #             self.visit(function)

    def visit_statement_list(self, *statement_list):
        for statement in statement_list:
            self.visit(statement)

    # def visit_f(self, node):
    #     print("Node:", node)
    #     for i, element in enumerate(node):
    #         print(f"Position {i}: {element}")
    #
    # def visit_function(self, identifier, statement_list, datatype=None, datavalue=None):
    #     # Handle function with no arguments
    #     if datatype is None:
    #         self.function_registry[identifier] = {
    #             'datatype': None,
    #             'default_value': None,
    #             'statement_list': statement_list
    #         }
    #         print(f"Function '{identifier}' with no arguments added to registry")
    #
    #     else:
    #         if datatype not in ['integer', 'boolean', 'float', 'string']:
    #             raise TypeError(f"Data type '{datatype}' does not exist")
    #
    #         # Process the argument value
    #         if isinstance(datavalue, tuple) and datavalue[0] == 'expression':
    #             datavalue = self.visit_expression(*datavalue[1:])
    #         elif isinstance(datavalue, (int, float, str, bool)):
    #             pass  # No further processing needed for literal values
    #         elif isinstance(datavalue, str) and datavalue.lower() in ['true', 'false']:
    #             datavalue = datavalue.lower() == 'true'
    #         else:
    #             raise ValueError("Invalid argument value type")
    #
    #         # Add the function with its argument to the function registry
    #         self.function_registry[identifier] = {
    #             'datatype': datatype,
    #             'default_value': datavalue,
    #             'statement_list': statement_list
    #         }
    #         print(
    #             f"Function '{identifier}' with argument '{datatype}' and default value '{datavalue}' added to registry")
    #
    #     # Process the statements within the function
    #     if statement_list is not None:
    #         self.visit(statement_list)

    def visit_variable_declaration(self, datatype, identifier, expression=None):
        if expression is not None:
            if isinstance(expression, tuple) and expression[0] == 'expression':
                value = self.visit_expression(*expression[1:])
            elif isinstance(expression, (int, float, str, bool)) or expression == 'nil':
                if expression == 'nil':
                    value = None
                else:
                    value = expression
            elif isinstance(expression, str) and expression.lower() in ['true', 'false']:
                value = expression.lower() == 'true'
            else:
                raise ValueError("Invalid value type")
        else:
            value = None

        valid_types = ['integer', 'boolean', 'float', 'string']
        if datatype not in valid_types:
            raise TypeError(f"Data type '{datatype}' does not exist")

        if datatype == 'integer' and not isinstance(value, int) and value is not None:
            raise TypeError(f"Cannot assign {value} to an integer variable")
        elif datatype == 'boolean':
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                else:
                    raise TypeError(f"Cannot assign {value} to a boolean variable")
            elif not isinstance(value, bool) and value is not None:
                raise TypeError(f"Cannot assign {value} to a boolean variable")
        elif datatype == 'float' and not isinstance(value, float) and value is not None:
            raise TypeError(f"Cannot assign {value} to a float variable")
        elif datatype == 'string' and not isinstance(value, str) and value is not None:
            raise TypeError(f"Cannot assign {value} to a string variable")

        if identifier in self.symbol_table:
            raise NameError(f"Variable '{identifier}' is already defined")

        self.symbol_table[identifier] = {'type': datatype, 'value': value}

    def visit_variable_assignment(self, identifier, value):
        if isinstance(value, tuple) and value[0] == 'expression':
            value = self.visit_expression(*value[1:])
        elif isinstance(value, (int, float, str, bool)):
            pass
        else:
            raise ValueError("Invalid value type")

        if isinstance(identifier, tuple) and identifier[0] == 'array_index_access':
            array_name = identifier[1]
            index = identifier[2]

            if isinstance(index, str) and index in self.symbol_table:
                index = self.symbol_table[index]['value']
            elif isinstance(index, tuple):
                index = self.visit_expression(*index[1:])
            # Now resolve the index value by calling the relevant visit function and assign it from the symbol table
            index_value = self.visit_array_index_access(array_name, index)
            if array_name in self.symbol_table:
                array = self.symbol_table[array_name]['value']
                if 0 <= index < len(array):
                    array[index] = value
                else:
                    raise IndexError(f"Index {index} out of bounds for array '{array_name}'")
            else:
                raise NameError(f"Array '{array_name}' is not defined")

        else:
            if identifier not in self.symbol_table:
                raise NameError(f"Variable '{identifier}' is not defined")

            expected_type = self.symbol_table[identifier]['type']
            value_type = self.get_value_type(value)

            if value_type != expected_type:
                raise TypeError(
                    f"Variable '{identifier}' must be assigned a value of type '{expected_type}', got '{value_type}'")

            self.symbol_table[identifier]['value'] = value

    def visit_expression(self, operator, left_operand=None, right_operand=None):
        def resolve_operand(operand):
            if isinstance(operand, tuple):
                if operand[0] == 'array_index_access':
                    array_name = operand[1]
                    index = operand[2]
                    if isinstance(index, str) and index in self.symbol_table:
                        index = self.symbol_table[index]['value']
                    elif isinstance(index, tuple):
                        index = self.visit_expression(*index[1:])
                    return self.visit_array_index_access(array_name, index)
                elif operand[0] == 'expression':
                    return self.visit_expression(*operand[1:])
            elif isinstance(operand, str):
                if operand in self.symbol_table:
                    operand_value = self.symbol_table[operand]['value']
                    if operand_value is not None:
                        return operand_value
                    else:
                        raise ValueError(f"Variable '{operand}' has no assigned value")
                elif operand.lower() == 'true':
                    return True
                elif operand.lower() == 'false':
                    return False
                else:
                    raise NameError(f"Variable '{operand}' is not defined")
            return operand

        if operator in ['+', '-', '*', '^', '/', ',']:
            if isinstance(left_operand, tuple) and left_operand[0] == 'expression':
                left_operand = self.visit_expression(*left_operand[1:])
            else:
                left_operand = resolve_operand(left_operand)

            if isinstance(right_operand, tuple) and right_operand[0] == 'expression':
                right_operand = self.visit_expression(*right_operand[1:])
            else:
                right_operand = resolve_operand(right_operand)

            # Perform the arithmetic operation based on the operator
            if operator == '+':
                return left_operand + right_operand
            elif operator == '-':
                return left_operand - right_operand
            elif operator == '*':
                return left_operand * right_operand
            elif operator == '/':
                if right_operand == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_operand / right_operand
            elif operator == '^':
                return pow(left_operand, right_operand)
            elif operator == ',':
                return str(left_operand) + str(right_operand)
            else:
                raise ValueError(f"Unknown operator: {operator}")
        elif operator == '++':
            if isinstance(left_operand, str) and left_operand in self.symbol_table:
                current_value = self.symbol_table[left_operand]['value']
                if isinstance(current_value, int):
                    new_value = current_value + 1
                    self.symbol_table[left_operand]['value'] = new_value
                    return new_value
                else:
                    raise ValueError(f"Variable '{left_operand}' is not an integer")
            else:
                raise ValueError(f"Variable '{left_operand}' is not defined or is not a string")

        elif operator == '--':
            if isinstance(left_operand, str) and left_operand in self.symbol_table:
                current_value = self.symbol_table[left_operand]['value']
                if isinstance(current_value, int):
                    new_value = current_value - 1
                    self.symbol_table[left_operand]['value'] = new_value
                    return new_value
                else:
                    raise ValueError(f"Variable '{left_operand}' is not an integer")
            else:
                raise ValueError(f"Variable '{left_operand}' is not defined or is not a string")

        else:
            raise ValueError(f"Unknown operator: {operator}")

    def visit_condition_expression(self, operator, left_operand, right_operand=None):
        # Handle negation
        if operator == '!':
            if isinstance(left_operand, tuple):
                left_operand = self.visit_condition_expression(*left_operand[1:])
            elif isinstance(left_operand, str):
                if left_operand in self.symbol_table:
                    left_operand = self.symbol_table[left_operand]['value']
                else:
                    raise NameError(f"Variable '{left_operand}' is not defined")
            print(f"Debug: After negation, left_operand={left_operand}")
            return not left_operand

        # Handle logical and comparison operations
        if isinstance(left_operand, tuple) and left_operand[0] == 'condition_expression':
            left_operand = self.visit_condition_expression(*left_operand[1:])
        elif isinstance(left_operand, tuple):
            left_operand = self.visit_expression(*left_operand[1:])
        elif isinstance(left_operand, str):
            if left_operand in self.symbol_table:
                left_operand = self.symbol_table[left_operand]['value']
            else:
                raise NameError(f"Variable '{left_operand}' is not defined")

        if isinstance(right_operand, tuple) and right_operand[0] == 'condition_expression':
            right_operand = self.visit_condition_expression(*right_operand[1:])
        elif isinstance(right_operand, tuple):
            right_operand = self.visit_expression(*right_operand[1:])
        elif isinstance(right_operand, str):
            if right_operand in self.symbol_table:
                right_operand = self.symbol_table[right_operand]['value']
            else:
                raise NameError(f"Variable '{right_operand}' is not defined")

        # Apply comparison operators
        if operator == '==':
            return left_operand == right_operand
        elif operator == '<':
            return left_operand < right_operand
        elif operator == '>':
            return left_operand > right_operand
        elif operator == '<=':
            return left_operand <= right_operand
        elif operator == '>=':
            return left_operand >= right_operand
        elif operator == '!=':
            return left_operand != right_operand
        elif operator == '&&':
            return left_operand and right_operand
        elif operator == '||':
            return left_operand or right_operand
        else:
            raise ValueError(f"Unknown comparison operator: {operator}")

    def visit_array_declaration(self, datatype, identifier, size, values=None):
        if identifier in self.symbol_table:
            raise NameError(f"Variable '{identifier}' is already defined")

        if datatype not in ['integer', 'boolean', 'float', 'string']:
            raise TypeError(f"Data type '{datatype}' does not exist")

        # Handle the case where no initial values are provided
        if values is None:
            self.symbol_table[identifier] = {'type': datatype, 'value': [None] * size}
        else:
            # Process and validate array values
            array_values = self.visit_array_value_list(values)

            # Ensure the number of values matches the specified size
            if len(array_values) != size:
                raise ValueError(
                    f"Number of values ({len(array_values)}) does not match the size of the array ({size})")

            # Validate each value against the expected data type
            for value in array_values:
                if datatype == 'integer' and not isinstance(value, int):
                    raise TypeError(f"Cannot assign {value} to an integer array element")
                elif datatype == 'boolean' and not isinstance(value, bool):
                    raise TypeError(f"Cannot assign {value} to a boolean array element")
                elif datatype == 'float' and not isinstance(value, float):
                    raise TypeError(f"Cannot assign {value} to a float array element")
                elif datatype == 'string' and not isinstance(value, str):
                    raise TypeError(f"Cannot assign {value} to a string array element")

            self.symbol_table[identifier] = {'type': datatype, 'value': array_values}

    def visit_array_value_list(self, array_values):
        values = []
        current_value = array_values

        while isinstance(current_value, tuple):
            values.append(current_value[1])  # Extract the value from the tuple
            current_value = current_value[2] if len(current_value) == 3 else None  # Move to the next tuple

        if isinstance(current_value, int):
            values.append(current_value)
        return values

    def visit_array_index_access(self, identifier, index):
        if identifier not in self.symbol_table:
            raise NameError(f"Variable '{identifier}' is not defined")

        array_info = self.symbol_table[identifier]

        if 'value' not in array_info:
            raise ValueError(f"Variable '{identifier}' is not an array")

        if isinstance(index, str):
            try:
                index = int(index)
            except ValueError:
                raise TypeError(f"Array index '{index}' must be an integer, got 'str'")

        if not isinstance(index, int):
            raise TypeError(f"Array index must be an integer, got '{type(index).__name__}'")

        if not (0 <= index < len(array_info['value'])):
            raise IndexError(f"Index {index} is out of bounds for array '{identifier}'")

        return array_info['value'][index]

    def visit_if_statement(self, condition, statements, otherwise_condition=None,
                           otherwise_statements=None):

        original_symbol_table = self.symbol_table.copy()
        local_symbol_table = self.symbol_table.copy()

        # Process the comparison
        condition_result = self.visit_condition_expression(condition[1], condition[2], condition[3])

        if condition_result:
            self.symbol_table = local_symbol_table  # Replace the symbol table with the local one
            self.visit(statements)
        elif otherwise_statements:
            # If there are otherwise statements, execute them with the original symbol table
            self.symbol_table = original_symbol_table
            self.visit(otherwise_statements)
        elif otherwise_condition:
            # If the condition is met, execute the statements within the if statement
            self.symbol_table = original_symbol_table
            self.visit(otherwise_condition)

        self.symbol_table = original_symbol_table

    def visit_for_statement(self, variable_declaration, limit_value, step_tag, step_value, statement_list):
        variable_declaration_type = variable_declaration[1]
        variable_name = variable_declaration[2]
        start_value = variable_declaration[3]

        # Ensure start_value and step_value are integers
        try:
            start_value = int(start_value)
            step_value = int(step_value)
        except ValueError:
            raise ValueError("Start value and step value must be integers")

        # Validate step size and limit values
        if step_tag == "ascend":
            if start_value > limit_value:
                raise ValueError("Start value cannot be greater than the limit value in an incrementing loop")
            step_size = step_value
        elif step_tag == "descend":
            if start_value < limit_value:
                raise ValueError("Start value cannot be less than the limit value in a decrementing loop")
            step_size = -step_value
        else:
            raise ValueError(f"Invalid step tag '{step_tag}'")

        # Reject step size if it's zero
        if step_size == 0:
            raise ValueError("Step size cannot be zero")

        try:
            for i in range(start_value, limit_value, step_size):
                self.symbol_table[variable_name] = i
                self.visit_statement_list(statement_list)
        except Exception as e:
            print(f"Error during for loop execution: {e}")
            raise

    def visit_while_statement(self, condition, statements):
        original_symbol_table = self.symbol_table.copy()

        while True:
            local_symbol_table = original_symbol_table.copy()
            self.symbol_table = local_symbol_table

            # Evaluate the loop condition
            condition_result = self.visit_condition_expression(condition[1], condition[2], condition[3])

            if condition_result:
                self.visit(statements)
            else:
                break

            # Restore the original symbol table for the next iteration
            self.symbol_table = original_symbol_table

        # Restore the original symbol table after loop exits
        self.symbol_table = original_symbol_table

    def visit_print_statement(self, node):
        if node[0] == 'print_list':
            self.visit_print_list(node)
        else:
            _, print_list = node
            self.visit_print_list(print_list)
        self.output += "\n"

    def visit_print_list(self, node):
        if isinstance(node, tuple) and node[0] == 'print_list':
            items = node[1:]
        else:
            items = [node]

        for item in items:
            if isinstance(item, str) and item.startswith('"') and item.endswith('"'):
                # For a string literal
                self.output += item[1:-1]  # Remove the quotes
            elif isinstance(item, tuple) and item[0] == 'expression':
                # For an expression
                result = self.visit_expression(*item[1:])
                self.output += str(result)
            elif isinstance(item, tuple) and item[0] == 'array_index_access':
                # For an array index access
                array_name = item[1]
                index = item[2]
                if isinstance(index, str) and index in self.symbol_table:
                    index = self.symbol_table[index]['value']
                elif isinstance(index, tuple):
                    index = self.visit_expression(*index[1:])

                if array_name in self.symbol_table:
                    array = self.symbol_table[array_name]['value']
                    if isinstance(array, list) and 0 <= index < len(array):
                        self.output += str(array[index])
                    else:
                        raise IndexError(f"Index {index} is out of bounds for array '{array_name}'")
                else:
                    raise ValueError(f"Array '{array_name}' not found in symbol table")
            elif isinstance(item, str):
                if item in self.symbol_table:
                    value = self.symbol_table[item]['value']
                    if value is not None:
                        self.output += str(value)
                    else:
                        raise ValueError(f"Variable '{item}' has no assigned value")
                else:
                    self.output += item
            elif isinstance(item, tuple) and item[0] == 'print_list':
                self.visit_print_list(item)
            else:
                self.output += str(item)

            if item != items[-1]:
                self.output += " "

    def visit_return_statement(self, statement):
        print(f"Debug: Handling return statement: {statement}")

        if isinstance(statement, tuple):
            if statement[0] == 'condition_expression':
                print(f"Debug: Passing to visit_condition_expression: {statement[1:]}")
                self.return_value = self.visit_condition_expression(*statement[1:])
            elif statement[0] == 'expression':
                print(f"Debug: Passing to visit_expression: {statement[1:]}")
                self.return_value = self.visit_expression(*statement[1:])
            else:
                raise ValueError(f"Unsupported statement type: {statement[0]}")
        elif isinstance(statement, str):
            if statement in self.symbol_table:
                self.return_value = self.symbol_table[statement]['value']
            elif statement.lower() == 'true':
                self.return_value = True
            elif statement.lower() == 'false':
                self.return_value = False
            else:
                raise NameError(f"Variable '{statement}' is not defined")
        else:
            self.return_value = statement

        print(f"Debug: Return value computed: {self.return_value}")

        # Print the return value only if it's not part of a print statement
        if not isinstance(statement, tuple) or statement[0] != 'print_statement':
            print(self.return_value)

        return self.return_value

    def visit_empty(self):
        pass

    @staticmethod
    def get_value_type(value):
        if isinstance(value, int):
            return 'integer'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, float):
            return 'float'
        else:
            return None
