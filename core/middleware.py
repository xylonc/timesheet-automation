from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        exempt_urls = [
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/password_reset/',
            '/accounts/password_reset/done/',
            '/accounts/reset/',
            '/accounts/reset/done/',
            '/users/registration/',
        ]
        
        if not request.user.is_authenticated:
            if not any(request.path.startswith(url) for url in exempt_urls):
                return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        
        
        return response
        