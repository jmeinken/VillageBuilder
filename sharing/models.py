from django.db import models
from account.models import Member, Participant

class Item(models.Model):
    SHARE_TYPES = (
        ('all_friends', 'all_friends'),
        ('all_friends_groups', 'all_friends_groups'),
        ('share_list', 'share_list'),
        ('custom', 'custom'),
    )
    ITEM_TYPES = (
        ('stuff','stuff'),
        ('space','space'),
        ('labor','labor'),
    )
    sharer = models.ForeignKey(Member, on_delete=models.CASCADE)
    share_type = models.CharField(max_length=30, choices=SHARE_TYPES)
    share_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=30, choices=ITEM_TYPES)
    title = models.CharField(max_length=60)
    description = models.TextField()
    image = models.CharField(max_length=30, blank=True, null=True)
    thumb = models.CharField(max_length=30, blank=True, null=True)
    # category = models.ForeignKey("Category", on_delete=models.CASCADE)
    sharelist = models.ForeignKey("Sharelist", on_delete=models.CASCADE, null=True, blank=True)

#class Category(models.Model):
#    name = models.CharField(max_length=60)
#    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    
class ItemSharee(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    sharee = models.ForeignKey(Participant, on_delete=models.CASCADE)
    
class Sharelist(models.Model):
    name = models.CharField(max_length=60)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    
class SharelistSharee(models.Model):
    sharelist = models.ForeignKey("Sharelist", on_delete=models.CASCADE)
    sharee = models.ForeignKey(Participant, on_delete=models.CASCADE)
    