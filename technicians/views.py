from django.shortcuts import render , redirect
from .forms import TechnicianForm
from .models import Technician
from django.db import transaction
from users.forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from core.permissions import Roles

def create_technician(request):
    if request.method == "POST":
        tech_form = TechnicianForm(request.POST)
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid() and tech_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                tech = tech_form.save(commit=False)
                tech.user = user
                tech.save()
                user.groups.add(Group.objects.get(name=Roles.TECHNICIAN))
            return redirect('technicians_list')
    else:
        tech_form = TechnicianForm()
        user_form = CustomUserCreationForm()
    
    return render(request , 'technician/create_technician.html' , {'user_form':user_form, 'tech_form':tech_form})

def technicians_list(request):
    technicians = Technician.objects.visible_to(request.user)
    return render(request, 'technician/technician_list.html', {'technicians':technicians})
