from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)
    blood_group=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class VolunteerIntakeStatus(models.Model):
    is_open = models.BooleanField(default=False)
    current_sheet_id = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)