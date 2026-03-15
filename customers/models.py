from django.db import models

class customer(models.Model):
    contact_person = models.CharField(("Contact Persons"), max_length=50)
    company_name = models.CharField(("Company Name"), max_length = 200)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.company_name
    