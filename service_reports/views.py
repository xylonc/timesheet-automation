from django.shortcuts import render, redirect
from .forms import ServiceReportForm
from .models import ServiceReport
from django.http import Http404
from django.db import transaction
from django.contrib import messages
from .models import ServiceReport
from .exceptions import InvalidTransition, TransitionNotAllowed
from django.views.decorators.http import require_POST


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
    service_reports = ServiceReport.objects.visible_to(request.user).select_related("customer", "technician")
    return render(
        request,
        "service_reports/service_report_list.html",
        {"service_reports": service_reports},
    )

@require_POST
def approve_service_report(request,pk):
    try:
        with transaction.atomic():
            try:
                report = ServiceReport.objects.select_for_update().get(pk=pk)
            except ServiceReport.DoesNotExist:
                raise Http404
            report.transition_to(ServiceReport.Status.APPROVED, actor=request.user)
        messages.success(request,"Report approved.")
    except (InvalidTransition, TransitionNotAllowed) as e:
        messages.error(request,str(e))
    return redirect("service_report_list")