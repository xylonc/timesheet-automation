from django.shortcuts import render , redirect 
from .forms import CustomUserCreationForm
from django.db import transaction
from django.contrib.auth.models import Group
from core.permissions import Roles

def create_admin(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                user.groups.add(Group.objects.get(name=Roles.ADMIN))
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
    
    return render(request , 'users/create_admin.html',{'user_form':user_form})