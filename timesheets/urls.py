from django.urls import path
from . import views

urlpatterns = [
    path('', views.timesheet_list, name='timesheet_list'),
    path('createtimesheet/', views.create_timesheet , name ='create_timesheet'),
]
