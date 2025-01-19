from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework.authtoken.models import Token
from django.db import models

class Member(AbstractUser):
    ROLE_CHOICES = [
        ('gm', 'General Member'),
        ('admin', 'Administrator'),
        ('mod', 'Moderator'),
    ]
    username = None    
    member_name = models.CharField(max_length=255, null=True, blank=False)
    email = models.EmailField(blank=False, unique=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    nid = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='gm')
    facebook = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    gmail = models.EmailField(blank=True)
    profile_pic = models.CharField(max_length=255,null=True,default="profilepic", blank=True)  # Now storing the image ID as a string
    availability = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
