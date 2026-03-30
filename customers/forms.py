from .models import Customer
from django import forms

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["contact_person", "company_name", "phone", "address"]
        
