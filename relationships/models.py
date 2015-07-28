from django.db import models

from account.models import Person, Guest

# person-person relationship

class Friendship(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='friendship_set')
    friend = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reverse_friendship_set')
    
    class Meta:
        unique_together = ('person', 'friend',)
        
class GuestFriendship(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('person', 'guest',)



 
# person-guest relationship






