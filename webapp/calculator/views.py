from common.class_views import JsonView
from .models import Calculator, CalculatorException
from common.http_exceptions import BadRequest

class EvaluateExpressionView(JsonView):

    def get_data(self, context):
        expression = self.request.GET.get('expression')

        try:
            context['answer'] = Calculator.evaluate(expression)
        except CalculatorException:
            raise BadRequest('Failed to evaluate expression.')
        return context

