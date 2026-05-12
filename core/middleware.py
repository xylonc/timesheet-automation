from django.urls import resolve , Resolver404
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from .permissions import ROLE_RULES
from django.http import HttpResponseForbidden , HttpResponseRedirect

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
        try:
            match = resolve(request.path_info)
            if match.view_name in EXEMPT_VIEW_NAMES:
                return self.get_response(request)
        except Resolver404:
            pass

        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
    
AUTHENTICATED_EXEMPT = {
    'users:logout_view',
}
    
class RoleRequiredMiddleware:
    def __init__(self , get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_superuser:
            return self.get_response(request)
        if not request.user.is_authenticated: # allow unauthenticated users go to exempted pages
            return self.get_response(request)
        try:
            match = resolve(request.path_info)
        except Resolver404:
            return self.get_response(request)
        if match.view_name in AUTHENTICATED_EXEMPT:# allow users to logout 
            return self.get_response(request)
        allowed_roles = ROLE_RULES.get(match.view_name)
        if allowed_roles is None:
            return HttpResponseForbidden()
        user_groups = set(request.user.groups.values_list('name', flat=True))
        if user_groups & allowed_roles: 
            return self.get_response(request)
        return HttpResponseForbidden()
            
