from django.db import models

class Technicians(models.Model):
    technician_name = models.CharField(("technician name"), max_length= 50)
    tech_email = models.CharField(("Serviceman email") , max_length=100)
    tech_phone = models.CharField(("Serviceman phone"), max_length=8)
    is_working = models.BooleanField(default=False)
    
    def __str__(self):
        return self.technician_name
