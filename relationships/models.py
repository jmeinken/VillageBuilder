from django.db import models

from account.models import Guest, Member, Group

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
        
class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    requested = models.BooleanField(default=False, db_index=True)
    invited = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        unique_together = ('group', 'member',)
        




 
# person-guest relationship






