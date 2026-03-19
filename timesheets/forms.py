from django import forms 
from .models import Timesheet

class TimeSheetForms(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['customer','technician','job_date','issue_reported','actions_taken','start_time','end_time' ]

        