
import json

from .models import *
from relationships.models import Friendship
from account.models import Member
from django.template.loader import render_to_string


def registerEvent(eventType, eventDict):
    if eventType == 'add friend':
        affectedParticipant = eventDict['friend_id']
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
    event.active = False
    event.save()
    
def getAlerts(currentParticipant):
    events = Event.objects.all().filter(affected_participant=currentParticipant).filter(active=True).order_by('created')
    responses = []
    count = 0
    for event in events:
        data = json.loads(event.event_data)
        if event.event_type == 'add friend':
            # check if still exists
            if Friendship.objects.all().filter(member_id=data['member_id'],friend_id=data['friend_id']).count()!=1:
                event.delete()
                continue
            # check if reciprocated
            member = Member.objects.get(id=data['member_id'])
            image = member.get_user_pic()
            friendName = member.participant.user.get_full_name()
            friendId = member.participant.id
            if Friendship.objects.all().filter(member_id=data['friend_id'],friend_id=data['member_id']).count()==1:
                response = {
                    'id' : event.id,
                    'image' : image,
                    'alt' : 'my image',
                    'text' : 'You are now friends with ' + friendName + '.',
                    'viewed' : event.viewed,
                    'form' : '', 
                }
            else:
                form = render_to_string('blocks/alert_add_friend.html', { 'friendId' : friendId })
                response = {
                    'id' : event.id,
                    'image' : image,
                    'alt' : 'my image',
                    'text' : friendName + ' added you as a friend.',
                    'viewed' : event.viewed,
                    'form' : form,
                }
            # get image 
            responses.append(response)
            if event.viewed == False:
                count += 1
    return {
        'alerts' : responses,
        'count' : count,
    }

        
        
    