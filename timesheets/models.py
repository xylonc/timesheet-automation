from django.db import models
from customers.models import customer
from technicians.models import technicians

class timesheets(models.Model):
    Customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    Technicians = models.ForeignKey(technicians, on_delete=models.CASCADE)

    job_date = models.DateField()

    issue_reported = models.TextField()
    actions_taken = models.TextField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    hours_worked = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} - {self.customer}"