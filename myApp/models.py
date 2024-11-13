# attendance_app/models.py
from django.db import models
from django.utils import timezone

from django.db import models

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)  # Make last_name nullable
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event_date = models.DateTimeField(default=timezone.now)
    scanned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.attendee.name} - {self.scanned_at}"
