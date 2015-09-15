from django.db import models
from account.models import Participant

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
      ("add friend", "add friend"),
    )
    affected_participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, db_index=True)
    viewed = models.BooleanField(db_index=True)
    active = models.BooleanField(db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    event_data = models.TextField(blank=True, null=True)
    more_data = models.TextField(blank=True, null=True)
