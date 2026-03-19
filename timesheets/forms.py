from django import forms 
from .models import Timesheet

class CreateTimeSheetForms(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['customer','technician','job_date','issue reported','actions_taken','end_time' ]

        