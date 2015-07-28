import string
import random

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from villagebuilder.settings import BASE_DIR

from account.models import Member, Participant, Person, Guest




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
    participants = Participant.objects.all().filter(participant_type='person')
    results = []
    for participant in participants:
        results.append(getParticipant(participant.id, currentParticipant))
    return results

def getFriendsOfFriends(currentParticipant):
    participants = Participant.objects.all().filter(participant_type='person')
    results = []
    for participant in participants:
        results.append(getParticipant(participant.id, currentParticipant))
    return results  

def getFriends(currentParticipant):
    friends = Person.objects.all().filter(reverse_friendship_set__person=currentParticipant.member.person)
    results = []
    for friend in friends:
        results.append(getParticipant(friend.id, currentParticipant))
    guestFriends = Guest.objects.all().filter(guestfriendship__person=currentParticipant.member.person)
    for guestFriend in guestFriends:
        results.append(getParticipant(guestFriend.id, currentParticipant))
    return results  

def getFriendRequests(currentParticipant):   
    friends = (
        Person.objects.all()
        .filter(friendship_set__friend=currentParticipant.member.person)
        .exclude(reverse_friendship_set__person=currentParticipant.member.person)
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
        participant = user.participant_set.get(participant_type='person')
        results.append(getParticipant(participant.id, currentParticipant))
    return results
    
    
def getParticipant(participantId, currentParticipant):
    participant = Participant.objects.get(id=participantId)
    # member = Member.objects.get(member=participant)
    if participant.participant_type == 'person': 
        result = {
            'id' : participant.id,
            'name' : participant.user.first_name + ' ' + participant.user.last_name,
            'display_address' : participant.member.get_display_address(),
            'user_pic' : participant.member.get_user_pic(),
            'relationship' : getRelationship(currentParticipant, participant),
            'participant_type' : ParticipantTypes.PERSON,
        }
    if participant.participant_type == 'guest': 
        result = {
            'id' : participant.id,
            'name' : participant.user.first_name + ' ' + participant.user.last_name,
            'display_address' : '(guest account)',
            'user_pic' : participant.guest.get_user_pic(),
            'relationship' : getRelationship(currentParticipant, participant),
            'participant_type' : ParticipantTypes.GUEST,
        }
    return result

def getParticipantFull(participantId, currentParticipant):
    participant = Participant.objects.get(id=participantId)
    result = getParticipant(participantId, currentParticipant)
    result['email'] = ''
    result['full_address'] = ''
    result['phone'] = ''
    if participant.participant_type == 'guest' and currentParticipant.participant_type == 'person':
        if result.relationship == RelationshipTypes.GUEST_FRIENDS:
            result['email'] = participant.user.email
    if participant.participant_type == 'person': 
        if (    result['relationship'] == RelationshipTypes.FRIENDS   
                or result['relationship'] == RelationshipTypes.GUEST_FRIENDS   
                or result['relationship'] == RelationshipTypes.REQUEST_RECEIVED   
           ):
            if participant.member.share_email:
                result['email'] = participant.user.email
            if participant.member.share_address:
                result['full_address'] = participant.member.full_address
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
        'user_pic' : '/static/img/generic-user.png',
        'relationship' : RelationshipTypes.NO_ACCOUNT,
        'participant_type' : ParticipantTypes.NONE,
    }
    
class RelationshipTypes():
    SELF = 0
    FRIENDS = 1
    NOT_FRIENDS = 2
    REQUEST_SENT = 3
    REQUEST_RECEIVED = 4
    NO_ACCOUNT = 5
    GUEST_FRIENDS = 6
    NOT_GUEST_FRIENDS = 7
    
    
class ParticipantTypes():
    PERSON = 0
    GUEST = 1
    GROUP = 2
    NONE = 4
    
def getRelationship(currentParticipant, participant):
    # p2p
    if currentParticipant.participant_type == 'person' and participant.participant_type == 'person':
        return getPersonToPersonRelationship(currentParticipant, participant)
    # guest friendships
    if currentParticipant.participant_type == 'person' and participant.participant_type == 'guest':
        return getPersonToGuestRelationship(currentParticipant, participant)
    
def getPersonToPersonRelationship(currentParticipant, participant):
    forward = False
    backward = False
    if currentParticipant == participant:
        return RelationshipTypes.SELF
    for friendship in currentParticipant.member.person.friendship_set.all():
        if friendship.friend == participant.member.person:
            forward = True
    for friendship in currentParticipant.member.person.reverse_friendship_set.all():
        if friendship.person == participant.member.person:
            backward = True
    if forward and backward:
        return RelationshipTypes.FRIENDS
    if forward:
        return RelationshipTypes.REQUEST_SENT
    if backward:
        return RelationshipTypes.REQUEST_RECEIVED
    return RelationshipTypes.NOT_FRIENDS
    
def getPersonToGuestRelationship(currentParticipant, participant):
    for guestFriendship in currentParticipant.member.person.guestfriendship_set.all():
        if guestFriendship.guest == participant.guest:
            return RelationshipTypes.GUEST_FRIENDS
    return RelationshipTypes.NOT_GUEST_FRIENDS
    

    
    
    
    
    
    
    
    
    