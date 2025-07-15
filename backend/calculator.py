import uuid # uuid is used for unique identification, reading history, error handling and session management
from decimal import Decimal

class Calculator:
    """Calculator logic"""

    def __init__(self, database=None):
        self.result_value = Decimal('0')
        self.database = database
        self.session_id = str(uuid.uuid4())

    def add(self, number):
        old_result = self.result_value
        self.result_value += Decimal(str(number))

        if self.database:
            try:
                self.database.save_calculation(
                    self.session_id, "addition", old_result, number, self.result_value
                )
                self.database.save_session(self.session_id, self.result_value)
            except Exception as e:
                print(f"Database error: {e}")
        
        return float(self.result_value)
        
    def subtract(self, number):
        old_result = self.result_value
        self.result_value -= Decimal(str(number))
        
        if self.database:
            try:
                self.database.save_calculation(
                    self.session_id, "subtraction", old_result, number, self.result_value
                )
                self.database.save_session(self.session_id, self.result_value)
            except Exception as e:
                print(f"Database error: {e}")
        
        return float(self.result_value)
    
    def multiply(self, number):
        old_result = self.result_value
        self.result_value *= Decimal(str(number))
        
        if self.database:
            try:
                self.database.save_calculation(
                    self.session_id, "multiplication", old_result, number, self.result_value
                )
                self.database.save_session(self.session_id, self.result_value)
            except Exception as e:
                print(f"Database error: {e}")
        
        return float(self.result_value)
    
    def divide(self, number):
        if number == 0:
            return "Error! Cannot divide by zero!"
        
        old_result = self.result_value
        self.result_value /= Decimal(str(number))
        
        if self.database:
            try:
                self.database.save_calculation(
                    self.session_id, "division", old_result, number, self.result_value
                )
                self.database.save_session(self.session_id, self.result_value)
            except Exception as e:
                print(f"Database error: {e}")
        
        return float(self.result_value)
    
    def reset(self):
        self.result_value = Decimal('0')
        if self.database:
            try:
                self.database.save_session(self.session_id, self.result_value)
            except Exception as e:
                print(f"Database error: {e}")
        return float(self.result_value)
    
    def result(self):
        return float(self.result_value)
    
    def history(self, limit=10):
        if self.database:
            try:
                return self.database.history(self.session_id, limit)  # Muudetud view_history -> history
            except Exception as e:
                print(f"Database error: {e}")
                return []
        return []

    def calculate(self, first_operand, second_operand, operator):
        from decimal import Decimal, DivisionByZero
        try:
            a = Decimal(str(first_operand))
            b = Decimal(str(second_operand))
            if operator == '+':
                result = a + b
            elif operator == '-':
                result = a - b
            elif operator == '*':
                result = a * b
            elif operator == '/':
                if b == 0:
                    return 'Error!'
                result = a / b
            else:
                return 'Error! Unknown operator!'
            # Optionally save to history if self.database exists
            if self.database:
                try:
                    self.database.save_calculation(
                        self.session_id, operator, a, b, result
                    )
                    self.database.save_session(self.session_id, result)
                except Exception as e:
                    print(f"Database error: {e}")
            return float(result)
        except DivisionByZero:
            return 'Error! Cannot divide by zero!'
        except Exception as e:
            print(f"Calculation error: {e}")
            return 'Error'