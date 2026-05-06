from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
        ),name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view')
]