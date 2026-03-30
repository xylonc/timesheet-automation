from django.shortcuts import render , redirect
from .form import TechnicianForm
from .models import Technician

def create_technician(request):
    if request.method == "POST":
        form = TechnicianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('technicians_list')
    else:
        form = TechnicianForm()
    
    return render(request , 'technician/create_technician.html' , {'form':form})

def technicians_list(request):
    technicians = Technician.objects.all()
    return render(request, 'technician/technician_list.html', {'technicians':technicians})
