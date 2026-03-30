from django.urls import path , include
from . import views
from .models import Technician

urlpatterns =[
    path('', views.technicians_list , name = "technicians_list"),
    path('createtechnician/', views.create_technician , name = "create_technician")
    
]