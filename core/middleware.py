from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import redirect_to_login

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        exempt_urls = [
            settings.LOGIN_URL,
        ]
        if not request.user.is_authenticated:
            if not any(request.path.startswith(url) for url in exempt_urls):
                return redirect_to_login(
                    request.get_full_path(),
                    settings.LOGIN_URL,
                    )
        response = self.get_response(request)
        return response
        