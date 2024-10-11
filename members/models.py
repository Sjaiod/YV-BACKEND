from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework.authtoken.models import Token
from django.db import models

class Member(AbstractUser):
    ROLE_CHOICES = [
        ('gm', 'General Member'),
        ('admin', 'Administrator'),
        ('mod', 'Moderator'),
    ]
    
    username = models.CharField(max_length=255, null=True, blank=False)
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


    
class MemberToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(Member, related_name='member_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = Token.generate_key()
        return super().save(*args, **kwargs)

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
