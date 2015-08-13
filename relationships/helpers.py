import string
import random

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from villagebuilder.settings import BASE_DIR

from account.models import Member, Participant, Guest
from main import helpers

from .models import *


class RelationshipTypes():
    SELF = 0
    FRIENDS = 1
    NOT_FRIENDS = 2
    REQUEST_SENT = 3
    REQUEST_RECEIVED = 4
    NO_ACCOUNT = 5
    GUEST_FRIENDS = 6
    NOT_GUEST_FRIENDS = 7
    GROUP_OWNER = 8
    GROUP_MEMBER = 10
    NOT_GROUP_MEMBER = 11
    GROUP_MEMBER_REQUESTED = 12
    GROUP_MEMBER_INVITED = 13
    NONE = 15


'''
    The following functions return model object querysets
'''

def getReciprocatedFriends(currentParticipant):
    friends = (
        Member.objects.all()
        .filter(reverse_friendship_set__member=currentParticipant.member)
        .filter(friendship_set__friend=currentParticipant.member)
    )
    return friends

#only works for members getting guests
def getReciprocatedFriendsAndGuests(currentParticipant):
    relations = Participant.objects.all().filter(
        (
            Q(member__reverse_friendship_set__member    =currentParticipant.member) & 
            Q(member__friendship_set__friend            =currentParticipant.member)
        ) |
        Q(guest__guestfriendship__member            =currentParticipant.member)
    )
    return relations


'''
    The rest don't return querysets but special participant dicts
'''

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

# requires a member be provided for current participant
def getRelations(currentParticipant, relationshipTypes=[]):
    relations = Participant.objects.all().filter(
        Q(member__reverse_friendship_set__member    =currentParticipant.member) | 
        Q(member__friendship_set__friend            =currentParticipant.member) |
        Q(guest__guestfriendship__member            =currentParticipant.member) | 
        Q(group__groupmembership__member            =currentParticipant.member) |
        Q(group__owner                              =currentParticipant.member)
    )
    results = []
    for relation in relations:
        participant = getParticipant(relation.id, currentParticipant)
        if participant['relationship'] in relationshipTypes:
            results.append(participant)
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

def getGroupMembers(group, relationshipTypes, currentParticipant):
    memberships = GroupMembership.objects.filter(group=group)
    results = []
    if group.owner == currentParticipant.member and RelationshipTypes.GROUP_OWNER in relationshipTypes:
        result = getParticipant(group.owner.id, currentParticipant)
        relationship = getRelationship(group.participant, group.owner.participant)
        results.append(result)
    for membership in memberships:
        result = getParticipant(membership.member.id, currentParticipant)
        relationship = getRelationship(group.participant, membership.member.participant)
        if relationship in relationshipTypes:
            results.append(result)
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
    groups = Group.objects.all().filter(title__icontains=searchString)
    for group in groups:
        results.append(getParticipant(group.participant.id, currentParticipant))
    return results
    
    
def getParticipant(participantId, contextParticipant=None):
    participant = Participant.objects.get(id=participantId)
    # member = Member.objects.get(member=participant)
    result = participant.get_public()
    if contextParticipant:
        result['relationship'] = getRelationship(contextParticipant, participant)
    else:
        result['relationship'] = RelationshipTypes.NONE
    if contextParticipant:
        contextGroups = Group.objects.filter(owner=contextParticipant.member)
        result['group_relationships'] = []
        for group in contextGroups:
            result['group_relationships'].append({
                'id' : group.id,
                'name' : group.title,
                'relationship' : getRelationship(group.participant, participant),
            })
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
    if participant.type == 'group':
        result['description'] = participant.group.description
    return result
            

    
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
    

    
    

# relationship of participantA to participantB
def getRelationship(a, b):
    # p2p
    if a.type == 'member' and b.type == 'member':
        return getMemberToMemberRelationship(a.member, b.member)
    # guest friendships
    if a.type == 'guest' and b.type == 'member':
        return getMemberToGuestRelationship(b.member, a.guest)
    if a.type == 'member' and b.type == 'guest':
        return getMemberToGuestRelationship(a.member, b.guest)
    # group memberships
    if a.type == 'member' and b.type == 'group':
        return getMemberToGroupRelationship(a.member, b.group)
    if a.type == 'group' and b.type == 'member':
        return getMemberToGroupRelationship(b.member, a.group)
    return RelationshipTypes.NONE
    
def getMemberToGroupRelationship(member, group):
    if member.id == group.owner.id:
        return RelationshipTypes.GROUP_OWNER
    membership = GroupMembership.objects.filter(member=member, group=group)
    if membership.count() == 0:
        return RelationshipTypes.NOT_GROUP_MEMBER
    if membership[0].requested and membership[0].invited:
        return RelationshipTypes.GROUP_MEMBER
    if membership[0].requested:
        return RelationshipTypes.GROUP_MEMBER_REQUESTED
    if membership[0].invited:
        return RelationshipTypes.GROUP_MEMBER_INVITED
    
    
def getMemberToMemberRelationship(memberA, memberB):
    forward = False
    backward = False
    if memberA.id == memberB.id:
        return RelationshipTypes.SELF
    for friendship in memberA.friendship_set.all():
        if friendship.friend == memberB:
            forward = True
    for friendship in memberA.reverse_friendship_set.all():
        if friendship.member == memberB:
            backward = True
    if forward and backward:
        return RelationshipTypes.FRIENDS
    if forward:
        return RelationshipTypes.REQUEST_SENT
    if backward:
        return RelationshipTypes.REQUEST_RECEIVED
    return RelationshipTypes.NOT_FRIENDS
    
def getMemberToGuestRelationship(member, guest):
    for guestFriendship in member.guestfriendship_set.all():
        if guestFriendship.guest == guest:
            return RelationshipTypes.GUEST_FRIENDS
    return RelationshipTypes.NOT_GUEST_FRIENDS
    

    
    
    
    
    
    
    
    
    