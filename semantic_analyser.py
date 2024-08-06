class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = {}
        self.output = ""

    def analyze(self, ast):
        try:
            self.visit(ast)
            return self.output, None  # Return the output and None as there are no exceptions
        except Exception as e:
            return self.output, str(e)  # Return the output along with the exception message

    def visit(self, node):
        method_name = 'visit_' + node[0]  # Whatever tag this gets, append that tag to the visit_
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(*node[1:])
        else:
            raise NotImplementedError(f"Method {method_name} not implemented")

    def visit_main_func(self, statement_list):
        # Process the statements within the main function
        self.visit(statement_list)

    def visit_statement_list(self, *statement_list):
        for statement in statement_list:
            self.visit(statement)

    def visit_variable_declaration(self, datatype, variable_assignment=None):
        print(f"Datatype in visit_variable_declaration: {datatype}")
        print(f"Variable Assignment in visit_variable_declaration: {variable_assignment}")

        # If variable_assignment is None, it means no assignment was provided
        if variable_assignment is None:
            var_name = datatype  # Assuming the datatype itself is the variable name
            if var_name in self.symbol_table:
                raise NameError(f"Variable '{var_name}' is already defined")

            print(f"Variable name at Line 40 in visit_variable_declaration: {var_name}")
            self.symbol_table[var_name] = {'type': datatype, 'value': None}
        else:
            # Check if the variable assignment is a tuple
            if isinstance(variable_assignment, tuple):
                # Extracting the identifier and expression from the variable_assignment tuple
                identifier, expression = variable_assignment[1], variable_assignment[2]
                print(f"Identifier in visit_variable_declaration: {identifier}")
                print(f"Expression in visit_variable_declaration: {expression}")

                # Check if the expression is a tuple
                if isinstance(expression, tuple):
                    # Visit the expression
                    value = self.visit_expression(*expression[1:])
                    print(f"Value after visiting expression from visit_variable_declaration: {value}")
                else:
                    value = expression  # Assign the literal value directly
                    print(f"Value in visit_variable_declaration: {value}")

                var_name = identifier
                if var_name in self.symbol_table:
                    raise NameError(f"Variable '{var_name}' is already defined")

                self.symbol_table[var_name] = {'type': datatype}

                if value is not None:
                    # If a value is provided, set it in the symbol table
                    self.symbol_table[var_name]['value'] = value
                else:
                    # Otherwise, set the default value to None
                    self.symbol_table[var_name]['value'] = None
            else:
                # Handle the case where only the identifier is provided without an expression
                identifier = variable_assignment
                print(f"Identifier in visit_variable_declaration: {identifier}")

                var_name = identifier
                if var_name in self.symbol_table:
                    raise NameError(f"Variable '{var_name}' is already defined")

                self.symbol_table[var_name] = {'type': datatype, 'value': None}

    def visit_variable_assignment(self, identifier, value):
        print(f"Identifier in visit_variable_assignment: {identifier}"
              f"\nValue in visit_variable_assignment: {value}")
        if isinstance(value, tuple) and value[0] == 'expression':  # If the value is an expression, evaluate it
            value = self.visit_expression(value[1], value[2], value[3])  # Operator Left_operand Right_operand
        elif isinstance(value, (int, float, str, bool)):  # If the value is a literal value
            pass  # No further processing needed for literal values
        else:
            raise ValueError("Invalid value type")

        if identifier not in self.symbol_table:
            raise NameError(f"Variable '{identifier}' is not defined")

        expected_type = self.symbol_table[identifier]['type']  # Accessing 'type' from the dictionary
        value_type = self.get_value_type(value)
        if value_type != expected_type:
            raise TypeError(
                f"Variable '{identifier}' must be assigned a value of type '{expected_type}', got '{value_type}'")

        print(f"Value of {identifier} in symbol table is {value}")
        self.symbol_table[identifier]['value'] = value  # Replacing the value of the variable in the symbol table

    def visit_expression(self, operator, left_operand=None, right_operand=None):
        l_name = left_operand
        r_name = right_operand

        if operator is None:
            if isinstance(left_operand, str):  # Check if left operand is a string
                if left_operand in self.symbol_table:
                    left_value = self.symbol_table[left_operand]['value']
                    if left_value is not None:
                        left_operand = left_value
                    else:
                        raise ValueError(f"Variable '{left_operand}' has no assigned value")
                else:
                    raise NameError(f"Variable '{left_operand}' is not defined")
            return left_operand

        if operator in ['+', '-', '*', '^', '/']:
            # Evaluate left and right operands recursively if they are expressions
            if isinstance(left_operand, tuple) and left_operand[0] == 'expression':
                left_operand = self.visit_expression(*left_operand[1:])
            if isinstance(right_operand, tuple) and right_operand[0] == 'expression':
                right_operand = self.visit_expression(*right_operand[1:])

        if isinstance(left_operand, str):  # Check if left operand is a string
            if left_operand in self.symbol_table:
                left_value = self.symbol_table[left_operand]['value']
                if left_value is not None:
                    left_operand = left_value
                else:
                    raise ValueError(f"Variable '{left_operand}' has no assigned value")
            else:
                raise NameError(f"Variable '{left_operand}' is not defined")

        if isinstance(right_operand, str):  # Check if right operand is a string
            if right_operand in self.symbol_table:
                right_value = self.symbol_table[right_operand]['value']
                if right_value is not None:
                    right_operand = right_value
                else:
                    raise ValueError(f"Variable '{right_operand}' has no assigned value")
            else:
                raise NameError(f"Variable '{right_operand}' is not defined")

        # Perform the arithmetic operation based on the operator
        if operator == '+':
            # Check if either operand is a string, if so, concatenate them
            if isinstance(left_operand, str) or isinstance(right_operand, str):
                return str(left_operand) + str(right_operand)
            else:
                # Otherwise, treat them as numerical values and perform addition
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
        elif operator == '++':
            if isinstance(l_name, str):
                left_operand += 1
                self.symbol_table[l_name]['value'] = left_operand
                return left_operand
            else:
                raise ValueError(f"{l_name} ++ must be of format: \n string ++")
        elif operator == '--':
            if isinstance(l_name, str):
                left_operand -= 1
                self.symbol_table[l_name]['value'] = left_operand
                return left_operand
            else:
                raise ValueError(f"{l_name} -- must be of format: \n string --")
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def visit_condition_expression(self, operator, left_operand, right_operand):
        print("Condition expression before value unpacking...")
        print(f"Operator: {operator}"
              f"\nLeft operand: {left_operand}"
              f"\nRight operand: {right_operand}")
        if isinstance(left_operand, str):
            if left_operand in self.symbol_table:
                left_value = self.symbol_table[left_operand]['value']
                if left_value is not None:
                    left_operand = left_value
                else:
                    raise ValueError(f"Variable '{left_operand}' has no assigned value")
            else:
                raise NameError(f"Variable '{left_operand}' is not defined")

        if isinstance(right_operand, str):
            if right_operand in self.symbol_table:
                right_value = self.symbol_table[right_operand]['value']
                if right_value is not None:
                    right_operand = right_value
                else:
                    raise ValueError(f"Variable '{right_operand}' has no assigned value")
            else:
                raise NameError(f"Variable '{right_operand}' is not defined")

        print("\nCondition expression after value unpacking...")
        print(f"Operator: {operator}"
              f"\nLeft operand: {left_operand}"
              f"\nRight operand: {right_operand}")
        if operator == '>':
            if left_operand > right_operand:
                return True
            else:
                return False
        elif operator == '<':
            if left_operand < right_operand:
                return True
            else:
                return False
        elif operator == '>=':
            if left_operand >= right_operand:
                return True
            else:
                return False
        elif operator == '<=':
            if left_operand <= right_operand:
                return True
            else:
                return False
        elif operator == '==':
            if left_operand == right_operand:
                return True
            else:
                return False
        elif operator == '!=':
            if left_operand != right_operand:
                return True
            else:
                return False
        else:
            raise ValueError(f"Unknown comparison operator: {operator}")

    def visit_if_statement(self, condition, statements, otherwise_condition=None,
                           otherwise_statements=None):  # else_statements would be statement_list in our language
        print(f"Condition:{condition}"
              f"\nOtherwise condition: {otherwise_condition}"
              f"\nOtherwise statement: {otherwise_statements}")

        original_symbol_table = self.symbol_table.copy()  # Make a copy of the original symbol table
        local_symbol_table = self.symbol_table.copy()  # Copy the current symbol table to the local one

        # Process the comparison
        condition_result = self.visit_condition_expression(condition[1], condition[2], condition[3])

        if condition_result:  # if True
            # If the condition is met, execute the statements within the if statement
            self.symbol_table = local_symbol_table  # Replace the symbol table with the local one
            self.visit(statements)  # do the body of the if_statement
        elif otherwise_statements:
            # If there are otherwise statements, execute them with the original symbol table
            self.symbol_table = original_symbol_table
            self.visit(otherwise_statements)
        elif otherwise_condition:  # if True
            # If the condition is met, execute the statements within the if statement
            self.symbol_table = original_symbol_table  # Replace the symbol table with the local one
            self.visit(otherwise_condition)  # do the body of the if_statement

        # Restore the original symbol table
        self.symbol_table = original_symbol_table

    def visit_array_declaration(self, datatype, identifier, size, values=None):
        print(f"Datatype of the array: {datatype}")  # The datatype of the array.
        print(f"Identifier of array: {identifier}")  # The identifier of the array.
        print(f"Size of the array: {size}")  # The size of the array.
        print(f"Values within the array: {values}")  # The optional array values.

        var_name = identifier
        if var_name in self.symbol_table:
            raise NameError(f"Variable '{var_name}' is already defined")

        if values is None:
            self.symbol_table[var_name] = {'type': datatype, 'value': [None] * size}
        else:
            print(f"Array values pre processing: {values}")
            array_values = self.visit_array_value_list(values)
            print(f"Array values post processing: {array_values}")
            if len(array_values) != size:
                raise ValueError("Number of values does not match the size of the array")
            self.symbol_table[var_name] = {'type': datatype, 'value': array_values}
            print(f"Array values: {array_values}")

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
        print(f"Array identifier: {identifier}")
        print(f"Array index requested: {index}")
        var_name = identifier
        if var_name not in self.symbol_table:
            raise NameError(f"Variable '{var_name}' is not defined")

        array = self.symbol_table[var_name]
        if 'value' not in array:
            raise ValueError(f"Variable '{var_name}' is not an array")

        array_values = array['value']
        print(f"Array values {array_values}")
        array_size = len(array_values)

        # Check if the index is within the bounds of the array
        if not (0 <= index < array_size):
            raise IndexError(f"Index '{index}' out of bounds for array '{var_name}'")

        # Access the value at the specified index
        value_at_index = array_values[index]
        print(f"Value at index{index}: {value_at_index}")
        return value_at_index

    def visit_for_statement(self, variable_declaration, limit_value, step_tag, step_value, statement_list):
        print(f"Variable Declaration: {variable_declaration}")
        print(f"Limit: {limit_value}")
        print(f"Step Tag: {step_tag}")
        print(f"Step Value: {step_value}")
        print(f"Statements: {statement_list}")
        variable_declaration_type, variable_assignment = variable_declaration[1], variable_declaration[2]

        # Check if the variable assignment is None
        if variable_assignment is None:
            raise ValueError("Variable in for loop is not assigned a value")

        # Visit the variable declaration
        self.visit_variable_declaration(variable_declaration_type, variable_assignment)

        # Extracting the starting value and step size based on the given variable_declaration
        start_value = variable_assignment[2]
        step_size = 1  # Default step size is 1

        # Execute the for loop
        if step_tag == "ascend":
            if start_value > limit_value:
                raise ValueError("Start value cannot be greater than the limit value in an incrementing loop")
            else:
                step_size = step_value
        elif step_tag == "descend":
            if start_value < limit_value:
                raise ValueError("Start value cannot be less than the limit value in a decrementing loop")
            else:
                step_size = -step_value

        step_size = int(step_size)

        print(f"Step value is: {step_value}")
        print(f"Step size is: {step_size}")

        # Reject step size if it's zero
        if step_size == 0:
            raise ValueError("Step size cannot be zero")

        # Execute the for loop
        for i in range(start_value, limit_value, step_size):
            # Inside the loop, you can access 'i' as the loop index variable
            self.symbol_table['i'] = i  # Update the symbol table with the current value of 'i'
            self.visit_statement_list(statement_list)

    def visit_do_while_statement(self, statements, condition):
        print(f"Statements: {statements}")
        print(f"Condition: {condition}")

        original_symbol_table = self.symbol_table.copy()  # Make a copy of the original symbol table

        while True:
            local_symbol_table = original_symbol_table.copy()  # Create a local symbol table
            self.symbol_table = local_symbol_table  # Set the symbol table to the local one
            self.visit_statement_list(statements)  # Visit the statements inside the loop

            # Evaluate the condition
            condition_result = self.visit_condition_expression(*condition[1:])
            if not condition_result:  # Break the loop if the condition is false
                break

        self.symbol_table = original_symbol_table  # Restore the original symbol table

    def visit_while_statement(self, condition, statements):
        print(f"Condition: {condition}"
              f"\nStatements: {statements}")
        original_symbol_table = self.symbol_table.copy()  # Make a copy of the original symbol table

        while True:
            local_symbol_table = original_symbol_table.copy()  # Create a local symbol table
            condition_result = self.visit_condition_expression(condition[1], condition[2], condition[3])
            if condition_result:
                self.symbol_table = local_symbol_table  # Set the symbol table to the local one
                self.visit(statements)
            else:
                self.symbol_table = original_symbol_table  # Restore the original symbol table
                break

        self.symbol_table = original_symbol_table  # Restore the original symbol table

    def visit_print_statement(self, text, variable=None):
        print(f"Text in visit_print_statement: {text}")
        print(f"Variable in visit_print_statement: {variable}")
        if isinstance(variable, tuple):
            if variable[0] == 'expression':
                result = self.visit(variable)
                self.output += f"{text}{result}\n"  # Append output to the existing output string
            elif variable[0] == 'array_index_access':
                array_identifier, index = variable[1:]
                if array_identifier in self.symbol_table:
                    array_value = self.symbol_table[array_identifier]['value']
                    if array_value is not None:
                        if 0 <= index < len(array_value):
                            self.output += f"{text}{array_value[index]}\n"  # Append output
                        else:
                            raise IndexError(f"Index {index} out of range for array '{array_identifier}'")
                    else:
                        raise ValueError(f"Array '{array_identifier}' has no assigned values")
                else:
                    raise NameError(f"Array '{array_identifier}' is not defined")
        elif isinstance(variable, str):
            if variable in self.symbol_table:
                value = self.symbol_table[variable]['value']
                if value is not None:
                    self.output += f"{text}{value}\n"  # Append output
                else:
                    raise ValueError(f"Variable '{variable}' has no assigned value")
            else:
                self.output += f"{text}{variable}\n"  # Append output
        elif isinstance(variable, (int, float)):
            self.output += f"{text}{str(variable)}\n"
        elif variable is None:
            self.output += f"{text}\n"  # Append output
        else:
            raise TypeError("Unsupported variable type for printing")

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
