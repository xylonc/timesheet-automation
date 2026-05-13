from django.db import models
from django.conf import settings
from core.permissions import Roles

class TechnicianQuerySet(models.QuerySet):
    def visible_to(self,user):
        if user.is_superuser or user.groups.filter(name=Roles.ADMIN).exists():
            return self
        return self.filter(user=user)


class Technician(models.Model):
    objects = TechnicianQuerySet.as_manager()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    technician_name = models.CharField(("technician name"), max_length=50)
    tech_phone = models.CharField(("Serviceman phone"), max_length=8)
    is_working = models.BooleanField(default=False)

    def __str__(self):
        return self.technician_name