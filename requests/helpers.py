import json

from django.core.urlresolvers import reverse
from django.db.models import Q

from relationships.helpers import getReciprocatedFriends
from .models import *
from account.models import Participant
from alerts.models import Event


def getViewersForRequest(request):
    # all reciprocated friends (missing group connections)
    participants = Participant.objects.filter(
        Q(member__friendship_set__friend=request.member) & 
        Q(member__reverse_friendship_set__member=request.member)
    )
    return participants

def getViewersForRequestComment(requestComment):
    # requester and everyone who has commented on this request
    request = requestComment.request
    participants = Participant.objects.filter(
        Q(member__requestcomment__request=request) | 
        Q(member__request=request)
    ).exclude(member=requestComment.member).distinct()
    return participants

def getRequestList(currentParticipant, start=0, end=10):
    #get list of friends
    friends = getReciprocatedFriends(currentParticipant)
    friendIds = []
    friendIds.append(currentParticipant.id)
    for friend in friends:
        friendIds.append(friend.id)
    requests = Request.objects.all().filter(member_id__in=friendIds).order_by('-date')
    requestList = []
    for request in requests[start:end]:
        requestList.append({
             'request' : request,
             'comments' : RequestComment.objects.all().filter(request=request).order_by('date')    
        })
    return {
        'requests' : requestList,
        'total_count' : requests.count(),
    }
    
def getRequestsOfFriends(currentParticipant, sinceDate):
    friends = getReciprocatedFriends(currentParticipant)
    requests = Request.objects.all().filter(date__gte=sinceDate).filter(member__in=friends)
    return requests

def getRelevantRequestComments(participant, sinceDate):
    # use event alerts to get comments to show
    events = (Event.objects.all()
        .filter(viewed=False)
        .filter(event_type="request comment")
        .filter(created__gte=sinceDate)
        .filter(affected_participant=participant)
    )
    results = []
    for event in events:
        requestId = json.loads(event.event_data)['request_id']
        commentIds = json.loads(event.more_data)['comment_ids']
        request = Request.objects.get(pk=requestId)
        comments = RequestComment.objects.all().filter(id__in=commentIds)
        if comments.count() == 0:
            event.delete()
            continue
        names = []
        for i in range(0, comments.count()):
            names.append(comments[i].member.participant.get_name())
            if i == 0:
                image = comments[i].member.participant.get_thumb()
        names = list(set(names)) # remove duplicates
        nameStr = ''
        for i in range(0, len(names)):
            if i == 0:
                nameStr = comments[i].member.participant.get_name()
                image = comments[i].member.participant.get_thumb()
            elif i == comments.count() - 1:
                nameStr = nameStr + ' and ' + comments[i].member.participant.get_name()
            else:
                nameStr = nameStr + ', ' + comments[i].member.participant.get_name()
        requesterName = request.member.participant.get_name()
        textStr = (nameStr 
            + ' commented on ' 
            + requesterName 
            + '\'s post.\n'
            + 'https://villagebuilder.net' + reverse('requests:request', args=[requestId])
        )
        htmlStr = (nameStr 
            + ' commented on <a href="https://villagebuilder.net' 
            + reverse('requests:request', args=[requestId])
            + '" style="color: #0099FF;">'
            + requesterName 
            + '\'s post.</a>'
        )
        results.append({'text' : textStr, 'html' : htmlStr})
    return results
    
def getSingleRequest(requestId):
    requests = Request.objects.all().filter(pk=requestId)
    requestList = []
    for request in requests:
        requestList.append({
             'request' : request,
             'comments' : RequestComment.objects.all().filter(request=request).order_by('date')    
        })
    return {
        'requests' : requestList,
        'total_count' : requests.count(),
    }

    