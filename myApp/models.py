# attendance_app/models.py
from django.db import models
from django.utils import timezone

from django.db import models

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_initial = models.CharField(max_length=2, null=True, blank=True)
    nickname = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Ensure nickname is unique
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)  # Email is no longer unique and can be nullable

    def __str__(self):
        return f"{self.first_name} {self.middle_initial or ''} {self.last_name or ''}"



class Attendance(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event_date = models.DateTimeField(default=timezone.now)
    scanned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.attendee.name} - {self.scanned_at}"
