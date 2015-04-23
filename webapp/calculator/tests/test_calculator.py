'''
Created on Apr 23, 2015

@author: Harp
'''
from calculator.models import Calculator, CalculatorException
from common.test_cases import HarpTestCase


class TestCalculator(HarpTestCase):


    def setUp(self):
        pass

    def test_reduce(self):
        tokens = [123, '+', 234]
        expected = 357
        # CALL
        Calculator.reduce(tokens)
        # ASSERT
        self.assertEqual([expected], tokens)

    def test_reduce__left_parenthese(self):
        tokens = ['(', 234]
        # CALL
        Calculator.reduce(tokens)
        # ASSERT
        self.assertEqual([234], tokens)

    def test_reduce__left_parenthese_with_has_left(self):
        tokens = [5.0, '(', 234.0]
        # CALL
        Calculator.reduce(tokens)
        # ASSERT
        self.assertEqual([5, 'x', 234], tokens)

    def test_evaluate__number(self):
        expression = '54.5'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(54.5, answer)

    def test_evaluate__passes(self):
        expression = '10.4 + 2 x 3(5 + 2(2) - 10%)'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(61.99999999999999, answer)

    def test_evaluate__passes_higher_order_front(self):
        expression = '10 x 2 + -3'  # 17
        # CALL
        actual = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(17, actual)

    def test_evaluate__right_side_multi_percent(self):
        expression = '3 x 50%'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(1.5, answer)

    def test_evaluate__right_side_add_percent(self):
        expression = '3 + 50%'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(4.5, answer)

    def test_evaluate__left_side_percent(self):
        expression = '50% + 4'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(4.5, answer)

    def test_evaluate__parantheses_expression(self):
        expression = '(5)'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(5.0, answer)

    def test_evaluate__parantheses_expression_complex(self):
        expression = '(7)9 x 8(2)(2)5(1)'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(10080, answer)

    def test_evaluate__parantheses_expression_simple(self):
        expression = '8 x(6)(8)'
        # CALL
        answer = Calculator.evaluate(expression)
        # ASSERT
        self.assertEqual(384, answer)

    def test_evaluate__invalid_character(self):
        expression = '3*4'
        # CALL & ASSERT
        self.assertRaisesMessage(
            CalculatorException, 'Invalid character: *', Calculator.evaluate, expression)

    def test_evaluate__invalid_expression(self):
        expression = '('
        # CALL & ASSERT
        self.assertRaisesMessage(
            CalculatorException, 'Unequal parantheses', Calculator.evaluate, expression)

if __name__ == "__main__":
    module_name = 'calculator.tests.test_calculator'
    test_class_name = 'TestCalculator'
    test_methods = ''
#     test_methods = ['test_evaluate__number']
    HarpTestCase.run_tests(module_name, test_class_name, test_methods)
