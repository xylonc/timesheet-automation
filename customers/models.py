from django.db import models
from core.permissions import Roles

class CustomerQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_superuser or user.groups.filter(name=Roles.ADMIN).exists():
            return self
        return self.filter(timesheet__technician__user=user).distinct()

class Customer(models.Model):
    objects = CustomerQuerySet.as_manager()
    contact_person = models.CharField(("Contact Persons"), max_length=50)
    company_name = models.CharField(("Company Name"), max_length = 200)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.company_name