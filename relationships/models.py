from django.db import models

from account.models import Person

# person-person relationship

class Friendship(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='friendship_set')
    friend = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reverse_friendship_set')



 
# person-guest relationship






