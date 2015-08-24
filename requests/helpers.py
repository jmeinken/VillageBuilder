
from relationships.helpers import getReciprocatedFriends

from .models import *




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

    