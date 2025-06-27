from http import HTTPStatus
from rest_framework.renderers import JSONRenderer


class ApiRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": HTTPStatus(status_code).name,
            "code": status_code,
            "data": data,
        }
        return super(ApiRenderer, self).render(response, accepted_media_type, renderer_context)