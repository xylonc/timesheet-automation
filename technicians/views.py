from django.shortcuts import render , redirect
from .forms import TechnicianForm
from .models import Technician
from django.db import transaction
from users.models import UserProfile
from users.forms import CustomUserCreationForm

def create_technician(request):
    if request.method == "POST":
        tech_form = TechnicianForm(request.POST)
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid() and tech_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                UserProfile.objects.create(
                    user=user,
                    role=UserProfile.Role.TECHNICIAN
                )
                tech = tech_form.save(commit=False)
                tech.user = user
                tech.save()
            return redirect('technicians_list')
    else:
        tech_form = TechnicianForm()
        user_form = CustomUserCreationForm()
    
    return render(request , 'technician/create_technician.html' , {'user_form':user_form, 'tech_form':tech_form})

def technicians_list(request):
    technicians = Technician.objects.all()
    return render(request, 'technician/technician_list.html', {'technicians':technicians})
