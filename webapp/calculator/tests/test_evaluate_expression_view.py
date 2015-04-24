'''
Created on Apr 23, 2015

@author: Harp
'''
from django.core.urlresolvers import reverse
from common.test_cases import IntegrationTestCase, HarpTestCase

class TestEvaluateExpressionView(IntegrationTestCase):

    def setUp(self):
        self.endpoint = reverse('evaluate')

    def test_missing_expression(self):
        status_code, content = self.http_get(self.endpoint)
        self.assertEqual(200, status_code)
        self.assertEqual(0, content['answer'])

    def test_success_response(self):
        cases = {
            '': 0,
            '-1234': -1234,
            '+1234': 1234,
            'x 1234': 0,
            '/ 1234': 0,
            '(-1234)': -1234,
            '(+1234)': +1234,
            '0': 0,
            '12345678910014': 12345678910014,
            '1 + 3': 4,
            '1 + -3': -2,
            '2 + -3': -1,
            '-9% + 2': 1.91,
            '-9%%%': -9e-06,
            ' -9% %   %': -9e-06,
            '2 x -9%': -0.18,
            '3  x 4': 12,
            '10 x 2 + -3': 17,
            '3 x 50%': 1.5,
            '3 + 50%': 4.5,
            '50% + 4': 4.5,
            '(5)': 5.0,
            '(5)9': 45.0,
            '5(9)': 45.0,
            '8 x(6)(8)': 384,
            '(7)9 x 8(2)(2)5(1)': 10080,
            '10.4 + 2 x 3(5 + 2(2) - 10%)': 61.99999999999999,
        }
        for expression, answer in cases.iteritems():
#             print '{} => {}'.format(expression, answer)
            # CALL
            status_code, content = self.http_get(self.endpoint, {'expression': expression})
            # ASSERT
            self.assertEqual(200, status_code)
            message = '{} evaluted to {}, expected {}'.format(
                expression, content['answer'], answer)
            self.assertEqual(answer, content['answer'], message)

    def test_bad_request_response(self):
        cases = [
            None,
            '3*4',
            '(',
            ')',
            '%',
            '+',
            '-',
            '1 / 0',
            '/ 0',
            '* 1234',
        ]
        for expression in cases:
#             print '{}'.format(expression)
            # CALL
            status_code, content = self.http_get(self.endpoint, {'expression': expression})
            # ASSERT
            self.assertEqual(400, status_code)
            self.assertEqual('Failed to evaluate expression.', content['error'])

if __name__ == "__main__":
    module_name = 'calculator.tests.test_evaluate_expression_view'
    test_class_name = 'TestEvaluateExpressionView'
    test_methods = ''
#     test_methods = ['test_success_response']
    HarpTestCase.run_tests(module_name, test_class_name, test_methods)
