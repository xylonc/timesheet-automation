from django.urls import path , include
from . import views
from .models import Customer

urlpatterns = [
    path('', views.customer_list , name = "customer_list"),
    path('createcustomer/', views.create_customer , name = 'create_customer')
]