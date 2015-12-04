import string
import random

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from villagebuilder.settings import BASE_DIR

from account.models import Member, Participant, Guest
from main.helpers import *

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
    ).distinct()
    return friends



def getFriendInvites(participant, sinceDate):    
    
    relationships = (
        Friendship.objects.all()
        .filter(friend=participant.member)
        .filter(created__gte=sinceDate)
        .exclude(member__reverse_friendship_set__member=participant.member)
    )
    return relationships

def getFriendConfirmations(participant, sinceDate):
    relationships = (
        Friendship.objects.all()
        .filter(friend=participant.member)
        .filter(created__gte=sinceDate)
        .filter(member__reverse_friendship_set__member=participant.member)
    )
    return relationships


def getReciprocatedGroups(currentParticipant):
    groups = Group.objects.all().filter(
            Q(owner = currentParticipant.member) |
            (  Q(groupmembership__member = currentParticipant.member) &
               Q(groupmembership__invited = True) &
               Q(groupmembership__requested = True)
            )
        ).distinct()
    return groups

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

def getUnreciprocatedFriendsAndGuests(currentParticipant):
    relations = Participant.objects.all().filter(
        Q(member__reverse_friendship_set__member    =currentParticipant.member) | 
        Q(member__friendship_set__friend            =currentParticipant.member) |
        Q(guest__guestfriendship__member            =currentParticipant.member)
    ).distinct()
    return relations

def doesUserHaveRelationshipActivity(currentParticipant):
    relations = Participant.objects.all().filter(
        Q(member__reverse_friendship_set__member    =currentParticipant.member) | 
        Q(guest__guestfriendship__member            =currentParticipant.member)
    ).distinct()
    if relations.count() == 0:
        return False
    if relations.count() == 1 and relations[0].member.is_admin:
        return False
    return True


'''
    The rest don't return querysets but special participant dicts
'''

def emailSearch(email, firstName, lastName, currentParticipant):    
    # see if that email exists
    matches = []
    participants = Participant.objects.all().filter(user__email=email).exclude(type='group')
    if participants.count() == 0:
        participants = Participant.objects.all().filter(user__first_name=firstName).filter(user__last_name=lastName)
        for participant in participants:
            matches.append(getParticipant(participant.id, currentParticipant))
        if email:
            matches.append(simulateParticipant(email, firstName, lastName))
    else:    
        for participant in participants:
            # print('participant Id:')
            # print(participant.id)
            matches.append(getParticipant(participant.id, currentParticipant))
    return {
        'email' : email,
        'name' : firstName + ' ' + lastName,
        'first_name' : firstName,
        'last_name' : lastName,
        'matches' : matches
    }
   
def getPeopleNearYou(currentParticipant):
    friends = Member.objects.all().filter(reverse_friendship_set__member=currentParticipant.member)
    lat = currentParticipant.member.latitude
    lng = currentParticipant.member.longitude
    members = Member.objects.raw('''SELECT *, POW(latitude - %s, 2) + POW(longitude - %s, 2) as distance
        FROM account_member
        ORDER BY distance
        LIMIT 6''', [lat, lng])
    results = []
    for member in members:
        if member != currentParticipant.member and not member in friends:
            results.append(getParticipant(member.id, currentParticipant))
    return results

def getFriendsOfFriends(currentParticipant):
    friends = Member.objects.all().filter(reverse_friendship_set__member=currentParticipant.member).order_by('?')
    resultIds = []
    results = []
    for friend in friends:
        if not friend.is_admin:
            friendFriends = getReciprocatedFriends(friend.participant).order_by('?')
            for friendFriend in friendFriends:
                if not friendFriend.is_admin and friendFriend != currentParticipant.member and not friendFriend.id in resultIds:
                    resultIds.append(friendFriend.id)    
            if len(resultIds) >= 5:
                for resultId in resultIds:
                    results.append(getParticipant(resultIds[i], currentParticipant))
                return results[:5]
    for resultId in resultIds:
        results.append(getParticipant(resultId, currentParticipant))
    return results[:5]  

# requires a member be provided for current participant
# returns participants related to contextParticipant with currentParticipant context
def getRelations(contextParticipant, currentParticipant, relationshipTypes=[]):
    if contextParticipant.type == 'member':
        allRelations = _getAllRelationsMember(contextParticipant)
    if contextParticipant.type == 'group':
        allRelations = _getAllRelationsGroup(contextParticipant)
    results = []
    if contextParticipant.type == 'guest':
        allRelations = _getAllRelationsGuest(contextParticipant)
    results = []
    for relation in allRelations:
        contextRel = getRelationship(contextParticipant, relation)
        if contextRel in relationshipTypes:
            participant = getParticipant(relation.id, currentParticipant)
            results.append(participant)
    return results

def _getAllRelationsMember(participant):
    allRelations = Participant.objects.all().filter(
        Q(member__reverse_friendship_set__member    =participant.member) | 
        Q(member__friendship_set__friend            =participant.member) |
        Q(guest__guestfriendship__member            =participant.member) | 
        Q(group__groupmembership__member            =participant.member) |
        Q(group__owner                              =participant.member)
    ).distinct()
    return allRelations

def _getAllRelationsGroup(participant):
    allRelations = Participant.objects.all().filter(
        Q(member__groupmembership__group = participant.group) |
        Q(member__group = participant.group)                                           
    ).distinct()
    return allRelations

def _getAllRelationsGuest(participant):
    allRelations = Participant.objects.all().filter(
        guest__guestfriendship__guest=participant.guest                                   
    ).distinct()
    return allRelations


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
        participants = user.participant_set.filter(type='member')
        if not participants:
            participants = user.participant_set.filter(type='guest')
        results.append(getParticipant(participants[0].id, currentParticipant))
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
    # print(result)
    result['full_display_address'] = participant.get_display_address_long()
    result['email'] = ''
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
        return _getMemberToMemberRelationship(a.member, b.member)
    # guest friendships
    if a.type == 'guest' and b.type == 'member':
        return _getMemberToGuestRelationship(b.member, a.guest)
    if a.type == 'member' and b.type == 'guest':
        return _getMemberToGuestRelationship(a.member, b.guest)
    # group memberships
    if a.type == 'member' and b.type == 'group':
        return _getMemberToGroupRelationship(a.member, b.group)
    if a.type == 'group' and b.type == 'member':
        return _getMemberToGroupRelationship(b.member, a.group)
    return RelationshipTypes.NONE
    
def _getMemberToGroupRelationship(member, group):
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
    
    
def _getMemberToMemberRelationship(memberA, memberB):
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
    
def _getMemberToGuestRelationship(member, guest):
    for guestFriendship in member.guestfriendship_set.all():
        if guestFriendship.guest == guest:
            return RelationshipTypes.GUEST_FRIENDS
    return RelationshipTypes.NOT_GUEST_FRIENDS
    

    
    
    
    
    
    
    
    
    