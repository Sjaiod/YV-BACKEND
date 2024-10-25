from django.db import models

class VolunteerSeason(models.Model):
    event_name = models.CharField(max_length=100)
    file_id = models.CharField(max_length=255)
    intake_status = models.BooleanField(default=True)

    def __str__(self):
        return self.event_name
