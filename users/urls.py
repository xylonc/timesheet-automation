from django.urls import path , include
from . import views

urlpatterns = [
    path('registration/', views.register_view , name='register_view'),
    path('login/', views.login_view , name='login_view'),
]