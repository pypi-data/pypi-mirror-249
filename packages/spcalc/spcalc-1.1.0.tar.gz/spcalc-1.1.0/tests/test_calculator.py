# test cases for calculator.py
from src.calculator import Calculator
from src.add import Add
from src.subtract import Subtract
from src.multiply import Multiply
from src.divide import Divide
import pytest


class TestCalculator:
    def test_calculator_add(self):
        calculator = Calculator(1, 2, Add())
        assert calculator.execute() == 3

    def test_calculator_subtract(self):
        calculator = Calculator(1, 2, Subtract())
        assert calculator.execute() == -1

    def test_calculator_multiply(self):
        calculator = Calculator(1, 2, Multiply())
        assert calculator.execute() == 2

    def test_calculator_divide(self):
        calculator = Calculator(1, 2, Divide())
        assert calculator.execute() == 0.5

    def test_calculator_divide_by_zero(self):
        calculator = Calculator(1, 0, Divide())
        with pytest.raises(ZeroDivisionError):
            calculator.execute()
