from django.utils import timezone
from .models import Access_key

class ExpiryCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check and update the expiry status of all access keys
        keys = Access_key.objects.all()
        for key in keys:
            key.check_expiry()

        # Continue processing the request
        response = self.get_response(request)
        return response
