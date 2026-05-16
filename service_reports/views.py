from django.shortcuts import render , redirect 
from .forms import TimeSheetForms
from .models import Timesheet
from django.contrib.auth.decorators import login_required

def create_timesheet(request):
    if request.method == 'POST':
        form = TimeSheetForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timesheet_list')
    else:
        form = TimeSheetForms()
    
    return render(request, 'timesheet/create_timesheet.html', {'form':form})

def timesheet_list(request):
    timesheets = Timesheet.objects.visible_to(request.user)
    return render(request, 'timesheet/timesheet_list.html', {'timesheets': timesheets})
    


