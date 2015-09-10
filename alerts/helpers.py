
import json

from .models import *
from relationships.models import Friendship, GroupMembership
from account.models import Member, Group
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


# CALLING FOR ADDING FRIEND
#eventDict = {
#    'member_id' : currentParticipant.id,
#    'friend_id' : friendId,
#}
#registerEvent('add friend', eventDict)

# CALLING FOR INVITING TO GROUP
#eventDict = {
#    'group_id' : currentParticipant.id,
#    'member_id' : friendId,
#}
#registerEvent('group invite', eventDict)

# CALLING FOR REQUESTING TO JOIN GROUP
#eventDict = {
#    'group_id' : currentParticipant.id,
#    'member_id' : friendId,
#}
#registerEvent('group request', eventDict)

def registerEvent(eventType, eventDict):
    if eventType == 'add friend':
        affectedParticipant = eventDict['friend_id']
    if eventType == 'group invite':
        affectedParticipant = eventDict['member_id']
    if eventType == 'group request':
        group = Group.objects.get(id=eventDict['group_id'])
        affectedParticipant = group.owner.id
    ## check for duplicate
    duplicate = (Event.objects.all()
            .filter(affected_participant_id = affectedParticipant)
            .filter(event_type = eventType)
            .filter(event_data = json.dumps(eventDict))
            .filter(active = True)
            .count()
    )
    if duplicate == 0:
        event = Event(
            affected_participant_id = affectedParticipant,
            event_type = eventType,
            event_data = json.dumps(eventDict),
            viewed = False,
            active = True,
        )
        event.save()

def resetAlertCount(currentParticipant):
    events = Event.objects.all().filter(affected_participant=currentParticipant).filter(active=True).order_by('created')
    for event in events:
        event.viewed=True
        event.save()

def deleteAlert(alertId):
    event = Event.objects.get(pk=alertId)
    # event.active = False
    # event.save()
    event.delete()

    
def getAlerts(currentParticipant):
    events = Event.objects.all().filter(affected_participant=currentParticipant).filter(active=True).order_by('-created')
    responses = []
    count = 0
    for event in events:
        if event.event_type == 'add friend' and getAddFriendAlert(event):
            responses.append( getAddFriendAlert(event) )
            if event.viewed == False:
                count += 1
        elif event.event_type == 'group request' and getGroupRequestAlert(event):
            responses.append( getGroupRequestAlert(event) )
            if event.viewed == False:
                count += 1
        elif event.event_type == 'group invite' and getGroupInviteAlert(event):
            responses.append( getGroupInviteAlert(event) )
            if event.viewed == False:
                count += 1
    return {
        'alerts' : responses,
        'count' : count,
    }
    
def getGroupInviteAlert(event):
    data = json.loads(event.event_data)
    # check if still exists
    memberships = GroupMembership.objects.all().filter(member_id=data['member_id'],group_id=data['group_id'])
    if memberships.count() != 1 or not memberships[0].invited:
        event.delete()
        return None
    # check if reciprocated
    membership = memberships[0]
    groupOwnerName = membership.group.owner.participant.get_name()
    groupOwnerId = membership.group.owner.id
    groupName = membership.group.participant.get_name()
    groupId = membership.group.id
    linkedGroupOwnerName = '<a href="' + reverse('account:view', args=[groupOwnerId]) + '">' + groupOwnerName + '</a>'
    linkedGroupName = '<a href="' + reverse('account:view', args=[groupId]) + '">' + groupName + '</a>'
    if membership.requested:
        response = {
            'id' : event.id,
            'image' : membership.group.participant.get_image(),
            'alt' : 'my image',
            'text' : 'You are now a member of ' + linkedGroupName,
            'viewed' : event.viewed,
            'form' : '', 
        }
    else:
        form = render_to_string('alerts/blocks/alert_join_group.html', { 'groupId' : data['group_id'] })
        response = {
            'id' : event.id,
            'image' : membership.member.participant.get_image(),
            'alt' : 'my image',
            'text' : linkedGroupOwnerName + ' has invited you to join the group ' + linkedGroupName,
            'viewed' : event.viewed,
            'form' : form,
        }
    return response

def getGroupRequestAlert(event):
    data = json.loads(event.event_data)
    # check if still exists
    memberships = GroupMembership.objects.all().filter(member_id=data['member_id'],group_id=data['group_id'])
    if memberships.count() != 1 or not memberships[0].requested:
        event.delete()
        return None
    # check if reciprocated
    membership = memberships[0]
    memberName = membership.member.participant.get_name()
    memberId = membership.member.id
    linkedName = '<a href="' + reverse('account:view', args=[memberId]) + '">' + memberName + '</a>'
    if membership.invited:
        response = {
            'id' : event.id,
            'image' : membership.member.participant.get_image(),
            'alt' : 'my image',
            'text' : linkedName + ' has joined your group ' + membership.group.participant.get_name(),
            'viewed' : event.viewed,
            'form' : '', 
        }
    else:
        form = render_to_string('alerts/blocks/alert_invite_to_group.html', { 'groupId' : data['group_id'], 'memberId' : data['member_id'] })
        response = {
            'id' : event.id,
            'image' : membership.member.participant.get_image(),
            'alt' : 'my image',
            'text' : linkedName + ' wants to join your group ' + membership.group.participant.get_name(),
            'viewed' : event.viewed,
            'form' : form,
        }
    return response
    
def getAddFriendAlert(event):
    data = json.loads(event.event_data)
    # check if still exists
    if Friendship.objects.all().filter(member_id=data['member_id'],friend_id=data['friend_id']).count()!=1:
        event.delete()
        return None
    # check if reciprocated
    member = Member.objects.get(id=data['member_id'])
    image = member.get_thumb()
    friendName = member.participant.user.get_full_name()
    friendId = member.participant.id
    linkedName = '<a href="' + reverse('account:view', args=[friendId]) + '">' + friendName + '</a>'
    if Friendship.objects.all().filter(member_id=data['friend_id'],friend_id=data['member_id']).count()==1:
        response = {
            'id' : event.id,
            'image' : image,
            'alt' : 'my image',
            'text' : 'You are now friends with ' + linkedName + '.',
            'viewed' : event.viewed,
            'form' : '', 
        }
    else:
        form = render_to_string('alerts/blocks/alert_add_friend.html', { 'friendId' : friendId })
        response = {
            'id' : event.id,
            'image' : image,
            'alt' : 'my image',
            'text' : linkedName + ' wants to be friends.',
            'viewed' : event.viewed,
            'form' : form,
        } 
    return response
        
        
    