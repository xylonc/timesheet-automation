from .models import Technician
from django import forms
from users.models import User

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ["technician_name","tech_phone","is_working"]
