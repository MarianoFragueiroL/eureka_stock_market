from django.http import JsonResponse
from django.core.exceptions import ValidationError
from ..models import ApiKey

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_API_KEY' in request.META:
            try:
                api_key = request.META['HTTP_API_KEY']
                key = ApiKey.objects.get(key=api_key)
                request.user = key.user
            except (ValueError, ValidationError, ApiKey.DoesNotExist):
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        return self.get_response(request)