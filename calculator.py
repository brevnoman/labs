import unittest


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b


class CalculatorTest(unittest.TestCase):
    a = 5
    b = 6
    def test_add(self):
        result = Calculator.add(a=self.a, b=self.b)
        self.assertEqual(result, 11)
    def test_subtract(self):
        result = Calculator.subtract(a=self.a, b=self.b)
        self.assertEqual(result, -1)
    def test_multiply(self):
        result = Calculator.multiply(a=self.a, b=self.b)
        self.assertEqual(result, 30)
    def test_divide(self):
        result = Calculator.divide(a=self.a, b=self.b)
