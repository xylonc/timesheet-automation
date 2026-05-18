from django.shortcuts import render, redirect
from .forms import ServiceReportForm
from .models import ServiceReport


def create_service_report(request):
    if request.method == "POST":
        form = ServiceReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service_report_list")
    else:
        form = ServiceReportForm()

    return render(request, "service_reports/create_service_report.html", {"form": form})


def service_report_list(request):
    service_reports = ServiceReport.objects.visible_to(request.user)
    return render(
        request,
        "service_reports/service_report_list.html",
        {"service_reports": service_reports},
    )
