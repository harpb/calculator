from django.http import JsonResponse
from django.views.generic.base import TemplateView
from common.http_exceptions import BadRequest

class JsonResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        del context['view']
        try:
            return JsonResponse(self.get_data(context), **response_kwargs)
        except BadRequest, e:
            response_kwargs['status'] = 400
            return JsonResponse({'error': e.message}, **response_kwargs)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context

class JsonView(TemplateView, JsonResponseMixin):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
