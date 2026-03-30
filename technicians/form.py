from .models import Technician
from django import forms

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ["technician_name","tech_email","tech_phone","is_working"]