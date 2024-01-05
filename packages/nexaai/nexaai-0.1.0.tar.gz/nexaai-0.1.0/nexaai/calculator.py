import numpy as np

class Calculator:
    def __init__(self):
        """Calculator class for basic arithmetic operations."""
    
    def add(self, a, b):
        """Add two numbers."""
        return np.add(a, b)
    
    def subtract(self, a, b):
        """Subtract two numbers."""
        return np.subtract(a, b)

    def multiply(self, a, b):
        """Multiply two numbers."""
        return np.multiply(a, b)

    def divide(self, a, b):
        """Divide two numbers. Returns np.nan if division by zero occurs."""
        # Using np.divide which handles division by zero gracefully
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        return np.divide(a, b)
