from django.db import models
from customers.models import Customer
from technicians.models import Technician
from core.permissions import Roles
from .exceptions import InvalidTransition, TransitionNotAllowed


class ServiceReportQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_superuser or user.groups.filter(name=Roles.ADMIN).exists():
            return self
        return self.filter(technician__user=user)


class ServiceReport(models.Model):
    objects = ServiceReportQuerySet.as_manager()

    class Status(models.TextChoices):
        DISPATCHED = "dispatched", "Dispatched"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        EMAILED = "emailed", "Emailed"
        SIGNED = "signed", "Signed"
        CANCELLED = "cancelled", "Cancelled"
    
    ALLOWED_TRANSITIONS = {
        Status.DISPATCHED: [Status.SUBMITTED, Status.CANCELLED],
        Status.SUBMITTED: [Status.APPROVED],
        Status.APPROVED: [Status.EMAILED],
        Status.EMAILED: [Status.SIGNED],
        Status.SIGNED: [],
        Status.CANCELLED: [],
    }

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DISPATCHED
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
    
    
    
    def transition_to(self, new_status, actor):
        allowed = self.ALLOWED_TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise InvalidTransition(
                f"Cannot transition from {self.status} to {new_status}."
            )
        self._check_preconditions(new_status, actor)
        self.status=new_status
        self.save(update_fields=['status'])
    
    def _check_preconditions(self, new_status, actor):

        # dispatched to submitted must have the relevant fields filled out
        if new_status == self.Status.DISPATCHED:
            if not self.issue_reported:
                raise TransitionNotAllowed("Issue reported must be filled before dispatching.")
            elif not self.actions_taken:
                raise TransitionNotAllowed("Actions taken must be filled before dispatching.")
            elif not self.equipment_serial:
                raise TransitionNotAllowed("Equipment serial must be filled before dispatching.")
            elif not self.start_time or not self.end_time:
                raise TransitionNotAllowed("Start and end time must be filled before dispatching.")

        # from dispatched to submitted: job date must be set  
        if new_status == self.Status.SUBMITTED:
            if not self.job_date:
                raise TransitionNotAllowed("Job date must be set before submitting.")
            
        
            
