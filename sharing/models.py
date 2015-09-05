import collections

from django.db import models
from account.models import Member, Participant

# computer value, display value
# !! these should all be unique names even across item types
stuffKeywords = [
    ['tools', 'tools'],
    ['electronics', 'electronics'],
    ['food', 'food'],
    ['toys/games', 'toys/games'],
    ['outdoor/camping', 'outdoor/camping'],
    ['instruments', 'instruments'],
    ['art', 'art'],
    ['tickets', 'tickets'],
    ['materials', 'materials'],
    ['other stuff', 'other stuff'],
]
spaceKeywords = [
    ['event space', 'event space'],
    ['meeting space', 'meeting space'],
    ['garden space', 'garden space'],
    ['storage space', 'storage space'],
    ['play area', 'play area'],
    ['kitchen/dining space', 'kitchen/dining space'],
    ['other space', 'other space'],            
]
laborKeywords = [
    ['home repair', 'home repair'],
    ['computer/technical', 'computer/technical'],
    ['child care', 'child care'],
    ['legal', 'legal'],
    ['creative', 'creative'],
    ['yard/gardening', 'yard/gardening'],
    ['other labor', 'other labor'],             
]
# computer value, display value, associated keywords
SHARE_CATEGORIES = [
    ['stuff', 'Stuff', stuffKeywords],
    ['space', 'Space', spaceKeywords],
    ['labor', 'Labor/Skills', laborKeywords],                                 
]

OLD_SHARE_CATEGORIES = collections.OrderedDict()
OLD_SHARE_CATEGORIES['Stuff'] = collections.OrderedDict([
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
])
OLD_SHARE_CATEGORIES['Space'] = collections.OrderedDict([
    ('event space', 'event space',),
    ('meeting space', 'meeting space',),
    ('garden space', 'garden space',),
    ('storage space', 'storage space',),
    ('play area', 'play area',),
    ('kitchen/dining space', 'kitchen/dining space',),
    ('other', 'other',),
])
OLD_SHARE_CATEGORIES['Skills/Labor'] = collections.OrderedDict([
    ('home repair', 'home repair',),
    ('computer/technical', 'computer/technical',),
    ('child care', 'child care',),
    ('legal', 'legal',),
    ('creative', 'creative',),
    ('yard/gardening', 'yard/gardening',),
    ('other', 'other',),
])                



class Item(models.Model):
    SHARE_TYPES = (
        ('all_friends', 'all_friends'),
        ('all_friends_groups', 'all_friends_groups'),
        ('share_list', 'share_list'),
        ('custom', 'custom'),
    )
    ITEM_TYPES = ()
    for category in SHARE_CATEGORIES:
        ITEM_TYPES = ITEM_TYPES + ((category[0], category[1]),)
    print(ITEM_TYPES)
    sharer = models.ForeignKey(Member, on_delete=models.CASCADE)
    share_type = models.CharField(max_length=30, choices=SHARE_TYPES, db_index=True)
    share_date = models.DateTimeField(auto_now_add=True, db_index=True)
    type = models.CharField(max_length=30, choices=ITEM_TYPES, db_index=True)
    title = models.CharField(max_length=120, db_index=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=30, blank=True, null=True)
    thumb = models.CharField(max_length=30, blank=True, null=True)
    to_borrow = models.BooleanField(default=True, db_index=True)
    to_keep = models.BooleanField(default=False, db_index=True)
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
    keyword = models.CharField(max_length=60, db_index=True)

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
    

    
    
    