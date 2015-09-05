from django.db import models
from account.models import Participant


class Message(models.Model):
    sender = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='message_sent_set')
    recipient = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='message_received_set')
    sent_on = models.DateTimeField(auto_now_add=True, db_index=True)
    body = models.TextField()
    viewed = models.BooleanField(default=False, db_index=True)
    
    

