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
        response = self.client.get(self.endpoint)
        self.assertEqual(400, response.status_code)

    def test_invalid_expression(self):
        expression = '('
        # CALL
        status_code, content = self.http_get(self.endpoint, {'expression': expression})
        # ASSERT
        self.assertEqual(400, status_code)
        self.assertEqual(200, content)

    def test_success_response(self):
        expression = '1 + 3'
        # CALL
        status_code, content = self.http_get(self.endpoint, {'expression': expression})
        # ASSERT
        self.assertEqual(200, status_code)
        self.assertEqual(200, content)


if __name__ == "__main__":
    module_name = 'calculator.tests.test_evaluate_expression_view'
    test_class_name = 'TestEvaluateExpressionView'
    test_methods = ''
#     test_methods = ['test_missing_expression']
    HarpTestCase.run_tests(module_name, test_class_name, test_methods)
