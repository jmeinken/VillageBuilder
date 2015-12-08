import collections, copy, urllib, json, time
from django.db.models import Q

from account.models import *
from relationships.helpers import getReciprocatedGroups
from relationships.models import *

from .models import *


def getSharingActions(member):
    actions = SharingActionNeeded.objects.filter(alertee=member)
    for action in actions:
        relationships = GroupMembership.objects.filter(group=action.subject.group, member=action.alertee)
        if relationships.count() == 0 or not relationships[0].requested or not relationships[0].invited:
            action.delete()
    return SharingActionNeeded.objects.filter(alertee=member)

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
        
def getParticipantsForItem(item):
    groups = getReciprocatedGroups(item.sharer.participant)
    groupIds = []
    for group in groups:
        groupIds.append(group.id)
    
    if item.share_type == 'all_friends':
        participants = Participant.objects.filter(
            Q(member__friendship_set__friend=item.sharer) & 
            Q(member__reverse_friendship_set__member=item.sharer)
        )
    if item.share_type == 'all_friends_groups':
        #ignoring things shared through groups
        participants = Participant.objects.filter(
            (Q(member__friendship_set__friend=item.sharer) & 
            Q(member__reverse_friendship_set__member=item.sharer))  
            # | Q(member__groupmembership__group_id__in=groupIds)
        ).exclude(member=item.sharer).distinct()
    if item.share_type == 'share_list':
        #ignoring things shared through groups
        participants = Participant.objects.filter(
            Q(sharelistsharee__shareList__item=item)                               
        )
    if item.share_type == 'custom':
        #ignoring things shared through groups
        participants = Participant.objects.filter(
            Q(itemsharee__item=item)                                      
        )
    return participants    
        
    


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
                Q(sharer__friendship_set__friend=participant.member) & 
                Q(sharer__reverse_friendship_set__member=participant.member)
            ) |
            ( Q(share_type='all_friends_groups') & Q(sharer__groupmembership__group_id__in=groupIds) &
               Q(sharer__groupmembership__requested=True) & Q(sharer__groupmembership__invited=True)) 
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

def getQuickShareKeywords(item_category, item_label):
    result = []
    if item_category == 'tools':
        result.append('tools')
    if item_category == 'kids':
        result.append('kids')
    if item_category == 'camping':
        result.append('outdoor/camping')
    if item_category == 'sports':
        result.append('sports/games')
    if item_label in ['food_processor', 'blender', 'stand_mixer', 'kitchen_scale']:
        result.append('electronics/appliances')
    return result

def getQuickShareItems():
    item_list1 = {}
    item_list2 = {}
    item_list3 = {}
    
    item_list1['kitchen'] = {
        'serving_bowl' : 'serving bowl',
        'serving_tray' : 'serving tray',
        'food_processor' : 'food processor',
        'blender' : 'blender',
        'stand_mixer' : 'stand mixer',
        'can_opener' : 'can opener',
        'large_pot' : 'large pot',
        'serving_spoon' : 'serving spoon',
        'ladle' : 'ladle',
        'potato_peeler' : 'potato peeler',
        'kitchen_scale' : 'kitchen scale',
        'rolling_pin' : 'rolling pin',
        'pizza_pan' : 'pizza pan',
        'knife_sharpener' : 'knife sharpener',                   
    }
    item_list2['tools'] = {
        'power_drill' : 'power drill',
        'hammer' : 'hammer',
        'screwdriver' : 'screwdriver',
        'staple_gun' : 'staple gun',
        'pliers' : 'pliers',
        'wrench' : 'wrench',
        'socket_wrench' : 'socket wrench',
        'stud_finder' : 'stud finder',
        'level' : 'level',
        'plunger' : 'plunger',
        'snake' : 'plumbing snake/auger',                  
    }
    item_list1['kids'] = {
        'play_pen' : 'play yard (play pen)',
        'child_carrier' : 'child carrier',
        'stroller' : 'stroller',
        'car_seat' : 'car seat',
        'bike' : 'bike',
        'scooter' : 'scooter',
        'baby_gate' : 'baby gate',
        'night_light' : 'night light',
        'bath' : 'bath tub',
        'baby_monitor' : 'baby monitor',   
    }
    item_list2['camping/outdoor'] = {
        'tent' : 'tent',
        'sleeping_bag' : 'sleeping bag',
        'sleeping_pad' : 'sleeping pad',
        'cooler' : 'cooler',
        'ice_packs' : 'ice packs',
        'camp_chairs' : 'camp chairs',
        'golf_umbrella' : 'golf umbrella',
        'lighter' : 'lighter',
        'tarp' : 'tarp',
        'flashlight' : 'flashlight',
        'lantern' : 'lantern',
        'pocket_knife' : 'pocket knife',
        'first_aid' : 'first aid kit',
        'insect_repellant' : 'insect repellant',
        'sunblock' : 'sunblock',
        'portable_radio' : 'portable radio'
    }
    item_list3['sports'] = {
        'basketball' : 'basketball',
        'soccer_ball' : 'soccer ball',
        'football' : 'football',
        'volleyball' : 'volleyball',
        'frisbee' : 'frisbee',
        'golf_clubs' : 'golf clubs',
        'tennis_racket' : 'tennis racket',
        'tennis_ball' : 'tennis ball',
        'racquetball_racket' : 'racquetball racket',
        'racquetball_ball' : 'racquetball ball',
        'yoga_mat' : 'yoga mat',
        'bike_pump' : 'bike pump',
        'ball_pump' : 'ball pump',
    }
    item_list3['yard'] = {
        'ext_ladder' : 'extension ladder',
        'wheelbarrow' : 'wheelbarrow',
        'grill' : 'grill',
        'bucket' : 'bucket',
        'chainsaw' : 'chainsaw',
        'lawnmower' : 'lawnmower',
        'hedge_trimmers' : 'hedge trimmers',
        'weed_wacker' : 'weed wacker',
        'pruner' : 'pruner',
        'lopper' : 'lopper',
        'saw' : 'saw',
        'shovel' : 'shovel',
        'hoe' : 'hoe',
        'snow_shovel' : 'snow shovel',
    }
    item_list3['auto'] = {
        'jack' : 'car jack',
        'jumper_cables' : 'jumper cables',
        'fix_a_flat' : 'fix-a-flat',
        'hand_vac' : 'cordless hand vacuum',
    }
    item_list1['assorted'] = {
        'air_mattress' : 'air mattress',
        'space_heater' : 'space heater',
        'glue' : 'glue',
        'duct_tape' : 'duct tape',
        'masking_tape' : 'masking tape',
        'packing_tape' : 'packing tape',
        'headphones' : 'headphones',
        'step_ladder' : 'step ladder',
        'x_cord' : 'extension cord',
    }
    
    
    return [item_list1, item_list2, item_list3]
    

# filters: sharer, group, search_string (title only or title and desc), category, keyword, has image
# order_by: share_date (asc), share date(desc)
# show in table: share date, category, keyword(s), title, image. shared by