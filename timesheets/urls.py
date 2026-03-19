from django.urls import path
from . import views

urlpatterns = [
    path('createtimesheet/', views.CreateTimeSheetForm , name ='create_timesheet'),
]
