from django.db import models
from members.models import Member  # Import the Member model

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    from_date = models.DateTimeField()  # Start date and time of the event
    to_date = models.DateTimeField()    # End date and time of the event
    place = models.CharField(max_length=255)
    participants = models.ManyToManyField(Member, related_name='events')  # Relationship to Member

    def __str__(self):
        return self.name