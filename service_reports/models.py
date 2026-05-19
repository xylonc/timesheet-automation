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
        Status.SIGNED: set(),
        Status.CANCELLED: set(),
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
    
    TRANSITION_PRECONDITIONS = {
        Status.SUBMITTED: '_check_can_submit',
        Status.APPROVED: '_check_can_approve',
        Status.EMAILED: '_check_can_email',
        Status.SIGNED: '_check_can_sign',
        Status.CANCELLED: '_check_can_cancel',
    }
    
    def transition_to(self, new_status, actor):
        allowed = self.ALLOWED_TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise InvalidTransition(
                f"Cannot transition from {self.status} to {new_status}."
            )
        method_name = self.TRANSITION_PRECONDITIONS.get(new_status)
        if method_name:
            getattr(self, method_name)(actor) #deferred lookup as we are passing the name of the function not the actual function
            #Method defined below so we cannot access function name now instead we defer it to a later time when we actually need to call it. 
        self.status=new_status
        self.save(update_fields=['status'])
    
    def _check_can_submit(self,  actor):
        # dispatched to submitted must have the relevant fields filled out
        errors =[]
        if not self.issue_reported:
            errors.append("Issue reported must be filled before dispatching.")
        elif not self.actions_taken:
            errors.append("Actions taken must be filled before dispatching.")
        elif not self.equipment_serial:
            errors.append("Equipment serial must be filled before dispatching.")
        elif not self.start_time or not self.end_time:
            errors.append("Start and end time must be filled before dispatching.")
        if errors:
            raise TransitionNotAllowed(", ".join(errors))
        
    def _check_can_approve(self, actor):
        # Only admins can approve
        if not actor.is_superuser and not actor.groups.filter(name=Roles.ADMIN).exists():
            raise TransitionNotAllowed("Only admins can approve service reports.")
        if not self.job_date:
            raise TransitionNotAllowed("Job date must be filled before approving.")
        if not self.warranty:
            raise TransitionNotAllowed("Warranty status must be filled before approving.")
    
    def _check_can_email(self, actor):
        if not self.customer.customer_email:
            raise TransitionNotAllowed("Customer has no email on file")
        
    def _check_can_sign(self, actor):
        pass
    
    def _check_can_cancel(self, actor):
        pass 