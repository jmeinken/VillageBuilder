from django.db import models

from account.models import Guest, Member

# person-person relationship

class Friendship(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='friendship_set')
    friend = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reverse_friendship_set')
    
    class Meta:
        unique_together = ('member', 'friend',)
        

        
class GuestFriendship(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('member', 'guest',)



 
# person-guest relationship






