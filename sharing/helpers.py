
from .models import *

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
        groupIds = Groups.objects.all().filter(
            Q(owner = participant.member) |
            Q(groupmembership__member = participant.member)
        ).values_list('pk', flat=True)
        partGroupIds = groupIds.append(participant.id)
        items = Item.objects.all().filter(
            ( Q(share_type='custom') & Q(itemsharee__sharee_id__in=partGroupIds) ) |
            ( Q(share_type='share list') & Q(sharelist__sharelistsharee__sharee_id__in=partGroupIds) ) |
            ( 
                ( Q(share_type='all friends') | Q(share_type='all friends and all groups') ) &
                Q(sharer__friendship__friend=participant.member)
            ) |
            ( Q(share_type='all friends and all groups') & Q(sharer__groupmembership__group_id__in=groupIds) )                              
        )
    return items
        