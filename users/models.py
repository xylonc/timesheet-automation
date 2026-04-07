from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'admin' , 'Admin'
        TECHNICIAN = 'technician', 'Technician'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)

    def __str__(self):
        return f"{self.user.username} - {self.role}"