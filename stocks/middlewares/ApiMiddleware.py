from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework_api_key.models import APIKey

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_API_KEY' in request.META:
            try:
                api_key = request.META['HTTP_API_KEY']
                key = APIKey.objects.get_from_key(key=api_key)
                request.api_key = key
            except (ValueError, ValidationError, APIKey.DoesNotExist):
                return JsonResponse({'error': 'Invalid API key'}, status=401)
        return self.get_response(request)