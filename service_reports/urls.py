from django.urls import path
from . import views

urlpatterns = [
    path("", views.service_report_list, name="service_report_list"),
    path(
        "createservicereport/",
        views.create_service_report,
        name="create_service_report",
    ),
    path("<int:pk>/approve/", views.approve_service_report, name="approve_service_report")
]
