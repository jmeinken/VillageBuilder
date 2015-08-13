from django.db import models
from account.models import Participant


class Message(models.Model):
    sender = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='message_sent_set')
    recipient = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='message_received_set')
    sent_on = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=60)
    body = models.TextField()
    viewed = models.BooleanField(default=False)
    
    

