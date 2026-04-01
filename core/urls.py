from django.urls import path , include
from .views import home 

urlpatterns = [
    path('', home, name='home'),
    path('timesheets/', include("timesheets.urls")),
    path('customers/' , include("customers.urls")),
    path('technicians/', include("technicians.urls")),
    path('users/', include("users.urls")),
]