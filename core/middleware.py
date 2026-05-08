from django.urls import resolve , Resolver404
from django.conf import settings
from django.contrib.auth.views import redirect_to_login

EXEMPT_VIEW_NAMES = {
    'users:login_view',
    'users:password_reset',
    'users:password_reset_done',
    'users:password_reset_confirm',
    'users:password_reset_complete',
}

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if request.user.is_authenticated:
            return self.get_response(request)
        
        #static file bypass cannot use resolver 
        if request.path.startswith(settings.STATIC_URL):
            return self.get_response(request)

        #paths exempt from authentication
        
        try:
            match = resolve(request.path_info)
            if match.view_name in EXEMPT_VIEW_NAMES:
                return self.get_response(request)
        except Resolver404:
            pass

        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        