from kfsd.apps.core.auth.key import APIKeyUser


class KubefacetsAPIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.api_key_user = APIKeyUser(request)
        response = self.get_response(request)
        return response
