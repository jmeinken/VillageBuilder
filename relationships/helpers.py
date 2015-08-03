import string
import random

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from villagebuilder.settings import BASE_DIR

from account.models import Member, Participant, Guest

class RelationshipTypes():
    SELF = 0
    FRIENDS = 1
    NOT_FRIENDS = 2
    REQUEST_SENT = 3
    REQUEST_RECEIVED = 4
    NO_ACCOUNT = 5
    GUEST_FRIENDS = 6
    NOT_GUEST_FRIENDS = 7




def emailSearch(email, firstName, lastName, currentParticipant):    
    # see if that email exists
    matches = []
    participants = Participant.objects.all().filter(user__email=email)
    if participants.count() == 0:
        participants = Participant.objects.all().filter(user__first_name=firstName).filter(user__last_name=lastName)
        for participant in participants:
            matches.append(getParticipant(participant.id, currentParticipant))
        if email:
            matches.append(simulateParticipant(email, firstName, lastName))
    else:    
        for participant in participants:
            matches.append(getParticipant(participant.id, currentParticipant))
    return {
        'email' : email,
        'name' : firstName + ' ' + lastName,
        'first_name' : firstName,
        'last_name' : lastName,
        'matches' : matches
    }
   
def getPeopleNearYou(currentParticipant):
    participants = Participant.objects.all().filter(type='member')
    results = []
    for participant in participants:
        results.append(getParticipant(participant.id, currentParticipant))
    return results

def getFriendsOfFriends(currentParticipant):
    participants = Participant.objects.all().filter(type='member')
    results = []
    for participant in participants:
        results.append(getParticipant(participant.id, currentParticipant))
    return results  

def getFriends(currentParticipant):
    friends = Member.objects.all().filter(reverse_friendship_set__member=currentParticipant.member)
    results = []
    for friend in friends:
        results.append(getParticipant(friend.id, currentParticipant))
    guestFriends = Guest.objects.all().filter(guestfriendship__member=currentParticipant.member)
    for guestFriend in guestFriends:
        results.append(getParticipant(guestFriend.id, currentParticipant))
    return results  

def getFriendRequests(currentParticipant):   
    friends = (
        Member.objects.all()
        .filter(friendship_set__friend=currentParticipant.member)
        .exclude(reverse_friendship_set__member=currentParticipant.member)
    )
    results = []
    for friend in friends:
        results.append(getParticipant(friend.id, currentParticipant))
    return results  

def searchParticipants(currentParticipant, searchString='', limit=0):
    #tokenize string
    if searchString=='':
        return []
    terms = searchString.split(' ')
    users = User.objects.all()
    for term in terms:
        users = users.filter( Q(last_name__icontains=term)  |  Q(first_name__icontains=term) )
    results = []
    for user in users:
        print str(user)
        participant = user.participant_set.get(type='member')
        results.append(getParticipant(participant.id, currentParticipant))
    return results
    
    
def getParticipant(participantId, currentParticipant):
    participant = Participant.objects.get(id=participantId)
    # member = Member.objects.get(member=participant)
    result = participant.get_public()
    result['relationship'] = getRelationship(currentParticipant, participant)
    print(result)
    return result

def getParticipantFull(participantId, currentParticipant):
    participant = Participant.objects.get(id=participantId)
    result = getParticipant(participantId, currentParticipant)
    print(result)
    result['email'] = ''
    result['phone'] = ''
    if participant.type == 'guest' and currentParticipant.type == 'member':
        if result['relationship'] == RelationshipTypes.GUEST_FRIENDS:
            result['email'] = participant.user.email
    if participant.type == 'member': 
        if (    result['relationship'] == RelationshipTypes.FRIENDS   
                or result['relationship'] == RelationshipTypes.GUEST_FRIENDS   
                or result['relationship'] == RelationshipTypes.REQUEST_RECEIVED
                or result['relationship'] == RelationshipTypes.SELF     
           ):
            if participant.member.share_email:
                result['email'] = participant.user.email
            if participant.member.share_phone:
                result['phone'] = participant.member.get_phone()
    return result
            
def createRandomString(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
    
def simulateParticipant(email, firstName, lastName):
    temp_id = createRandomString(30)
    return {
        'id' : temp_id,
        'name' : firstName + ' ' + lastName,
        'display_address' : email,
        'image' : '/static/img/generic-user.png',
        'thumb' : '/static/img/generic-user.png',
        'relationship' : RelationshipTypes.NO_ACCOUNT,
        'type' : 'none',
    }
    

    
    

    
def getRelationship(currentParticipant, participant):
    # p2p
    if currentParticipant.type == 'member' and participant.type == 'member':
        return getPersonToPersonRelationship(currentParticipant, participant)
    # guest friendships
    if currentParticipant.type == 'member' and participant.type == 'guest':
        return getPersonToGuestRelationship(currentParticipant, participant)
    
def getPersonToPersonRelationship(currentParticipant, participant):
    forward = False
    backward = False
    if currentParticipant == participant:
        return RelationshipTypes.SELF
    for friendship in currentParticipant.member.friendship_set.all():
        if friendship.friend == participant.member:
            forward = True
    for friendship in currentParticipant.member.reverse_friendship_set.all():
        if friendship.member == participant.member:
            backward = True
    if forward and backward:
        return RelationshipTypes.FRIENDS
    if forward:
        return RelationshipTypes.REQUEST_SENT
    if backward:
        return RelationshipTypes.REQUEST_RECEIVED
    return RelationshipTypes.NOT_FRIENDS
    
def getPersonToGuestRelationship(currentParticipant, participant):
    for guestFriendship in currentParticipant.member.guestfriendship_set.all():
        if guestFriendship.guest == participant.guest:
            return RelationshipTypes.GUEST_FRIENDS
    return RelationshipTypes.NOT_GUEST_FRIENDS
    

    
    
    
    
    
    
    
    
    