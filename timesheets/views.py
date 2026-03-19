from django.shortcuts import render , redirect 
from .forms import TimeSheetForms

def CreateTimeSheetForm(request):
    if request.method == 'POST':
        form = TimeSheetForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TimeSheetForms()
    
    return render(request, 'timesheet/create_timesheet.html', {'form':form})
    


