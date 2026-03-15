from django.db import models
from customers.models import Customer
from technicians.models import Technician

class Timesheet(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    technicians = models.ForeignKey(Technician, on_delete=models.CASCADE)

    job_date = models.DateField()

    issue_reported = models.TextField()
    actions_taken = models.TextField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    hours_worked = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} - {self.customer}"