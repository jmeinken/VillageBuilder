
from django.db.models import Q

from account.models import *
from relationships.helpers import getReciprocatedGroups

from .models import *


def getCategoriesWithCounts(items):
    categories = {}
    for key, keywords in SHARE_CATEGORIES.items():
        categories[key] = {}
        categories[key]['count'] = 0
        categories[key]['keywords'] = {}
        for keyword in keywords:
            categories[key]['keywords'][keyword[0]] = 0
    for item in items:
        for key in categories.keys():
            print(item.type)
            print(type(key))
            if item.type.lower() == key.lower():
                categories[key]['count'] = categories[key]['count'] + 1
            for keyword in categories[key]['keywords'].keys():
                if keyword in item.itemkeyword_set.values_list('keyword', flat=True):
                    categories[key]['keywords'][keyword] = categories[key]['keywords'][keyword] + 1
    return categories


# get all items shared with (not by) this participant
# participant must be current participant
def getItemsForParticipant(participant):
    if participant.type == 'guest':
        items = Item.objects.all().filter(
            ( Q(share_type='custom') & Q(itemsharee__sharee=participant) ) |
            ( Q(share_type='share list') & Q(sharelist__sharelistsharee__sharee=participant) ) |
            ( 
                ( Q(share_type='all friends') | Q(share_type='all friends and all groups') ) &
                Q(sharer__guest_friendship__guest=participant.guest)
            )
        )
    if participant.type == 'member':
        groups = getReciprocatedGroups(participant)
        groupIds = []
        for group in groups:
            groupIds.append(group.id)
        partGroupIds = groupIds
        partGroupIds.append(participant.id)
        print('groups:')
        print(partGroupIds)
        items = Item.objects.all().filter(
            ( Q(share_type='custom') & Q(itemsharee__sharee_id__in=partGroupIds) )  |
            ( Q(share_type='share_list') & Q(sharelist__sharelistsharee__sharee_id__in=partGroupIds) ) |
            ( 
                ( Q(share_type='all_friends') | Q(share_type='all_friends_groups') ) &
                Q(sharer__friendship_set__friend=participant.member)
            ) |
            ( Q(share_type='all_friends_groups') & Q(sharer__groupmembership__group_id__in=groupIds) ) 
        ).exclude(sharer=participant.member).distinct().order_by('-share_date')
    return items 

def getItemsSharedByCurrentMember(member):
    items = Item.objects.all().filter(sharer=member)
    return items

# filters: sharer, group, search_string (title only or title and desc), category, keyword, has image
# order_by: share_date (asc), share date(desc)
# show in table: share date, category, keyword(s), title, image. shared by