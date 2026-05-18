from django import forms
from .models import ServiceReport


class ServiceReportForm(forms.ModelForm):
    class Meta:
        model = ServiceReport
        fields = [
            "customer",
            "technician",
            "job_date",
            "issue_reported",
            "actions_taken",
            "start_time",
            "end_time",
            "equipment_serial",
            "warranty",
        ]
