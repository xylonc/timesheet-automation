from django.db import models
from customers.models import Customer
from technicians.models import Technician
from django.contrib.auth.models import Group
from core.permissions import Roles

class TimesheetQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_superuser or user.groups.filter(name=Roles.ADMIN).exists():
            return self
        return self.filter(technician__user=user)

class Timesheet(models.Model):
    objects = TimesheetQuerySet.as_manager()

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress' , 'In Progress'
        COMPLETED = 'completed' , 'Completed'
    
    status = models.CharField(max_length=20,choices = Status.choices, default= Status.IN_PROGRESS)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)

    job_date = models.DateField()

    issue_reported = models.TextField()
    actions_taken = models.TextField()

    start_time = models.TimeField()
    end_time = models.TimeField()
    # hours_worked = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} - {self.customer}"
    