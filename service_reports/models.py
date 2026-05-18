from django.db import models
from customers.models import Customer
from technicians.models import Technician
from core.permissions import Roles


class ServiceReportQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_superuser or user.groups.filter(name=Roles.ADMIN).exists():
            return self
        return self.filter(technician__user=user)


class ServiceReport(models.Model):
    objects = ServiceReportQuerySet.as_manager()

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        DISPATCHED = "dispatched", "Dispatched"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        EMAILED = "emailed", "Emailed"
        SIGNED = "signed", "Signed"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    # Relationship
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    technician = models.ForeignKey(
        Technician, on_delete=models.PROTECT, null=True, blank=True
    )

    # Content
    issue_reported = models.TextField(blank=True)
    actions_taken = models.TextField(blank=True)
    equipment_serial = models.CharField(max_length=100, blank=True)
    warranty = models.BooleanField(null=True, blank=True)

    # Time
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    job_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Job ID
    service_report_number = models.CharField(
        max_length=20, null=True, blank=True, unique=True
    )

    def __str__(self):
        return f"Job {self.id} - {self.customer}"
