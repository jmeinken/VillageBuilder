import collections

from django.db import models
from account.models import Member, Participant


SHARE_CATEGORIES = collections.OrderedDict()
SHARE_CATEGORIES['Stuff'] = (
    ('tools', 'tools',),
    ('electronics', 'electronics',),
    ('food', 'food',),
    ('toys/games', 'toys/games',),
    ('outdoor/camping', 'outdoor/camping',),
    ('instruments', 'instruments',),
    ('art', 'art',),
    ('tickets', 'tickets',),
    ('materials', 'materials',),
    ('other', 'other',),
)
SHARE_CATEGORIES['Space'] = [
    ('event space', 'event space',),
    ('meeting space', 'meeting space',),
    ('garden space', 'garden space',),
    ('storage space', 'storage space',),
    ('play area', 'play area',),
    ('kitchen/dining space', 'kitchen/dining space',),
    ('other', 'other',),
]
SHARE_CATEGORIES['Skills'] = [
    ('home repair', 'home repair',),
    ('computer', 'computer',),
    ('child care', 'child care',),
    ('legal', 'legal',),
    ('creative', 'creative',),
    ('yard/gardening', 'yard/gardening',),
    ('other', 'other',),
]                



class Item(models.Model):
    SHARE_TYPES = (
        ('all_friends', 'all_friends'),
        ('all_friends_groups', 'all_friends_groups'),
        ('share_list', 'share_list'),
        ('custom', 'custom'),
    )
    ITEM_TYPES = (
        ('stuff','Stuff'),
        ('space','Space'),
        ('skills','Skills'),
    )
    sharer = models.ForeignKey(Member, on_delete=models.CASCADE)
    share_type = models.CharField(max_length=30, choices=SHARE_TYPES)
    share_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=30, choices=ITEM_TYPES)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=30, blank=True, null=True)
    thumb = models.CharField(max_length=30, blank=True, null=True)
    to_borrow = models.BooleanField(default=True)
    to_keep = models.BooleanField(default=False)
    # category = models.ForeignKey("Category", on_delete=models.CASCADE)
    sharelist = models.ForeignKey("ShareList", on_delete=models.CASCADE, null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return '/static/uploads/item_pics/' + self.image
        return '/static/img/generic-item.png'
    
    def get_thumb(self):
        if self.thumb:
            return '/static/uploads/item_pics/' + self.thumb
        return '/static/img/generic-item.png'
    
    
class ItemKeyword(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=60)

#class Category(models.Model):
#    name = models.CharField(max_length=60)
#    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    
class ItemSharee(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sharee = models.ForeignKey(Participant, on_delete=models.CASCADE)
    
class ShareList(models.Model):
    name = models.CharField(max_length=60)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    
class ShareListSharee(models.Model):
    shareList = models.ForeignKey("ShareList", on_delete=models.CASCADE)
    sharee = models.ForeignKey(Participant, on_delete=models.CASCADE)
    

    
    
    