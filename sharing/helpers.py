import collections, copy, urllib, json, time
from django.db.models import Q

from account.models import *
from relationships.helpers import getReciprocatedGroups
from relationships.models import *

from .models import *


def getCategoriesWithCounts(items):
    categories = copy.deepcopy(SHARE_CATEGORIES)
    for itemType in categories:
        itemType.append(0)
        for keyword in itemType[2]:
            keyword.append(0)
    for item in items:
        for itemType in categories:
            if item.type == itemType[0]:
                itemType[3] = itemType[3] +1
            for keyword in itemType[2]:
                if keyword[0] in item.itemkeyword_set.values_list('keyword', flat=True):
                    keyword[2] = keyword[2] + 1
    return categories

# returns dict with 'value' integer meters and 'text' string 
def getDistance(member1, member2):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    key = "key=AIzaSyCJ9MW8BDW3-aYbYuoctGstHJkTxevbd9A"
    origins = "origins=" + str(member1.latitude) + ',' + str(member1.longitude)
    destinations = "destinations=" + str(member2.latitude) + ',' + str(member2.longitude)
    response = urllib.urlopen(url + "?" + key + "&" + origins + "&" + destinations + "&units=imperial")
    result = json.load(response)
    return result['rows'][0]['elements'][0]['distance']

def updateAllDistances(member):
    rels = Friendship.objects.all().filter(member=member)
    for rel in rels:
        distance = getDistance(rel.member, rel.friend)
        rel.distance = distance['value']
        rel.distance_text = distance['text']
        rel.save()
        time.sleep(0.01)
    reverseRels = Friendship.objects.all().filter(friend=member)
    for rel in reverseRels:
        distance = getDistance(rel.member, rel.friend)
        rel.distance = distance['value']
        rel.distance_text = distance['text']
        rel.save()
        time.sleep(0.01)
    
    
def removeAllSharing(memberId, participantId):
    itemSharees = ItemSharee.objects.all().filter(
        item__sharer_id=memberId
    ).filter(
        sharee_id=participantId
    )
    itemSharees.delete()
    shareListSharees = ShareListSharee.objects.all().filter(
        shareList__owner_id=memberId                                                        
    ).filter(
        sharee_id=participantId
    )
    shareListSharees.delete()
        
    


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
        # print('groups:')
        # print(partGroupIds)
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

def getItemsSharedByAndForParticipant(participant):
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
        # print('groups:')
        # print(partGroupIds)
        items = Item.objects.all().filter(
            Q(sharer=participant.member) |
            ( Q(share_type='custom') & Q(itemsharee__sharee_id__in=partGroupIds) )  |
            ( Q(share_type='share_list') & Q(sharelist__sharelistsharee__sharee_id__in=partGroupIds) ) |
            ( 
                ( Q(share_type='all_friends') | Q(share_type='all_friends_groups') ) &
                Q(sharer__friendship_set__friend=participant.member)
            ) |
            ( Q(share_type='all_friends_groups') & Q(sharer__groupmembership__group_id__in=groupIds) ) 
        ).distinct().order_by('-share_date')
    return items
    

def filterItems(items, category=None, sharerId=None, groupId=None, searchTerms=None, searchScope='title', hasImage=None):
    if category:
        isItemType = False
        for itemType in SHARE_CATEGORIES:
            # print(itemType[0])
            if category == itemType[0]:
                items = items.filter(type=category)
                isItemType = True
        if isItemType == False:
            items = items.filter(itemkeyword__keyword=category)
    if sharerId:
        items = items.filter(sharer_id=sharerId)
    if groupId:
        items = items.filter( Q(itemsharee__sharee_id=groupId) | Q(sharelist__sharelistsharee__sharee_id=groupId) )
    if searchTerms and searchScope == 'title':
        terms = searchTerms.split(' ')
        for term in terms:
            items = items.filter(title__contains=term)
    if searchTerms and searchScope == 'desc':
        terms = searchTerms.split(' ')
        queries = []
        for term in terms:
            queries.append( Q(title__contains=term) )
            queries.append( Q(description__contains=term) )
        # print('queries')
        # print(queries)
        query = queries.pop()
        for i in queries:
            query |= i
        # print query
        items = items.filter(query)
    if hasImage:
        items = items.exclude(thumb__isnull=True).exclude(thumb__exact='')
    return items 
    

def getItemsSharedByCurrentMember(member):
    items = Item.objects.all().filter(sharer=member).order_by('-share_date')
    return items

# filters: sharer, group, search_string (title only or title and desc), category, keyword, has image
# order_by: share_date (asc), share date(desc)
# show in table: share date, category, keyword(s), title, image. shared by