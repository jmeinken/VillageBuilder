import json
import threading

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages

from .models import *
from account.models import Participant, Guest

from account.helpers import *
from main.helpers import *
from relationships.helpers import *
from alerts.helpers import registerEvent
from sharing.helpers import removeAllSharing, getDistance, setSharingAction
from email_system.helpers import email_friend_request, email_friend_confirmation



@login_required
@csrf_exempt
@transaction.atomic
def add_friend(request):
    # print 'add friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        friend = Participant.objects.all().get(pk=friendId)
        friendship = Friendship(member=currentParticipant.member, friend_id=friendId)
        distance = getDistance(currentParticipant.member, friend.member)
        friendship.distance = distance['value']
        friendship.distance_text = distance['text']
        friendship.save()
        relationship = getRelationship(currentParticipant, friend)
        if relationship == RelationshipTypes.FRIENDS:
            t = threading.Thread(target=email_friend_confirmation, args=(request, friendship))
            t.start()
        else:
            t = threading.Thread(target=email_friend_request, args=(request, friendship))
            t.start()
        #register event
        eventDict = {
            'member_id' : currentParticipant.id,
            'friend_id' : friendId,
        }
        registerEvent('add friend', eventDict)
        if request.is_ajax():
            data = {'friendId' : friendId}
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            if relationship == RelationshipTypes.FRIENDS:
                messages.success(request, 'You are now friends with ' + friend.get_name() + '.')
            else:
                messages.success(request, 'A friend invite has been sent to ' + friend.get_name() + '.')
            return redirect(url)
    return redirect('login')

@login_required
@csrf_exempt
def add_guest_friend(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        guestId = request.POST.get("guest-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        guestFriendship = GuestFriendship(member=currentParticipant.member, guest_id=guestId)
        guestFriendship.save()
        #register event
        #eventDict = {
        #    'member_id' : currentParticipant.id,
        #    'friend_id' : friendId,
        #}
        #registerEvent('add friend', eventDict)
        if request.is_ajax():
            data = {'guestId' : guestId}
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            guest = Participant.objects.all().get(pk=guestId)
            messages.success(request, 'You are now friends with ' + guest.get_name() + '.')
            return redirect(url)
    return redirect('login')

@login_required
def add_group_members(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group_id")
        invites = request.POST.getlist("invites[]")
        for memberId in invites:
            groupMembership = GroupMembership.objects.all().filter(member_id=memberId, group_id=groupId)
            if groupMembership.count() == 0:
                groupMembership = GroupMembership(member_id=memberId, group_id=groupId)
            else:
                groupMembership = groupMembership[0]
                setSharingAction(currentParticipant.member.id, groupId, "new group")
            groupMembership.invited = True
            groupMembership.save()
            # register event
            eventDict = {
                'group_id' : groupId,
                'member_id' : memberId,
            }
            registerEvent('group invite', eventDict)
        messages.success(request, "Selected people have been invited to join your group.")
        return redirect(url)
    return redirect('login')

@login_required
@csrf_exempt
@transaction.atomic
def join_group(request):
    # print 'join_group'
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group_id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        groupMembership = GroupMembership.objects.all().filter(member=currentParticipant.member, group_id=groupId)
        if groupMembership.count() == 0:
            groupMembership = GroupMembership(member=currentParticipant.member, group_id=groupId)
        else:
            groupMembership = groupMembership[0]
            setSharingAction(currentParticipant.member.id, groupId, "new group")
        groupMembership.requested = True
        groupMembership.save()
        # register event
        eventDict = {
            'group_id' : groupId,
            'member_id' : currentParticipant.id,
        }
        registerEvent('group request', eventDict)
        return redirect(url)
    return redirect('login')

@login_required
@transaction.atomic
def unjoin_group(request):
    # print('unjoin')
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group_id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        groupMembership = GroupMembership.objects.all().filter(member=currentParticipant.member, group_id=groupId)
        if groupMembership.count() != 0:
            groupMembership = groupMembership[0]
            groupMembership.delete()
        removeAllSharing(currentParticipant.id, groupId)
        return redirect(url)
    return redirect('login')

@login_required
@csrf_exempt
def add_to_group(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group-id")
        memberId = request.POST.get("member-id")
        groupMembership = GroupMembership.objects.all().filter(member_id=memberId, group_id=groupId)
        if groupMembership.count() == 0:
            groupMembership = GroupMembership(member_id=memberId, group_id=groupId)
        else:
            groupMembership = groupMembership[0]
            setSharingAction(memberId, groupId, "new group")
        groupMembership.invited = True
        groupMembership.save()
        # register event
        eventDict = {
            'group_id' : groupId,
            'member_id' : memberId,
        }
        registerEvent('group invite', eventDict)
        return redirect(url)
    return redirect('login')

@login_required
@transaction.atomic
def remove_from_group(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group-id")
        memberId = request.POST.get("member-id")
        groupMembership = GroupMembership.objects.get(member_id=memberId, group_id=groupId)
        groupMembership.delete()
        removeAllSharing(memberId, groupId)
        return redirect(url)
    return redirect('login')


@login_required
@csrf_exempt
@transaction.atomic
def create_guest(request):
    # print 'create guest'
    if request.method == "POST":
        url = request.POST.get("redirect")
        tempId = request.POST.get("guest_temp_id")
        guestFirstName = request.POST.get("guest_first_name")
        guestLastName = request.POST.get("guest_last_name")
        if request.POST.get("guest_email"):
            guestEmail = request.POST.get("guest_email")
        else:
            guestEmail = User.objects.all().filter(first_name=guestFirstName, last_name=guestLastName)[0].email
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        # check if guest already exists
        user = User.objects.all().filter(email=guestEmail)
        if user.count() == 0:
            # create user, participant and guest
            user = User.objects.create_user(
                guestEmail, 
                guestEmail, 
                createRandomString(15), 
            )
            if guestFirstName or guestLastName:
                user.first_name = guestFirstName
                user.last_name = guestLastName
            else:
                user.first_name = guestEmail
            user.save()
            participant = Participant(
                user = user, 
                type = 'guest',
            )
            participant.save()
            guest = Guest(
                id = participant.id,
                participant = participant,
                code = createRandomString(60),
                created_by = currentParticipant.member,
            )
            guest.save()
        else:
            guest = Participant.objects.all().get(user=user,type='guest').guest
        # add guest as friend
        guestFriendship = GuestFriendship(
            member=currentParticipant.member, 
            guest=guest
        )
        guestFriendship.save()
        #register event
        #eventDict = {
        #   'person_id' : currentParticipant.id,
        #    'guest_id' : guest.id,
        #}
        # registerEvent('add friend', eventDict)
        if request.is_ajax():
            data = {'guestId' : guest.id, 'tempId' : tempId}
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            return redirect(url)
    return redirect('login')

@login_required
@transaction.atomic
def remove_friend(request):
    # print 'remove friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        friendships = Friendship.objects.all().filter(member=currentParticipant.member, friend_id=friendId)
        if friendships.count() > 0:
            friendships[0].delete()
        reverseFriendships = Friendship.objects.all().filter(friend=currentParticipant.member, member_id=friendId)
        if reverseFriendships.count() > 0:
            reverseFriendships[0].delete()
        removeAllSharing(currentParticipant.id, friendId)
        removeAllSharing(friendId, currentParticipant.id)
        friend = Participant.objects.all().get(pk=friendId)
        messages.success(request, 'You are no longer friends with ' + friend.get_name() + '.')
        return redirect(url)
    return redirect('login')

@login_required
@transaction.atomic
def remove_guest_friend(request):
    # print 'remove guest friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        guestFriendship = GuestFriendship.objects.get(member=currentParticipant.member, guest_id=friendId)
        guestFriendship.delete()
        removeAllSharing(currentParticipant.id, friendId)
        return redirect(url)
    return redirect('login')

@login_required
def email_search(request):
    email = request.POST.getlist("email[]")
    firstName = request.POST.getlist("first_name[]")
    lastName = request.POST.getlist("last_name[]")
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    results = []
    for i, value in enumerate(email):
        if email[i] or (firstName[i] and lastName[i]):
            results.append( emailSearch(email[i], firstName[i], lastName[i], currentParticipant) )
    return render(request, 'relationships/email_search.html', {
        'current' : getCurrentUser(request), 
        'RelationshipTypes' : RelationshipTypes,
        'results' : results,
    })
    
@login_required
def friend_suggestions(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    return render(request, 'relationships/friend_suggestions.html', {
        'current' : getCurrentUser(request), 
        'RelationshipTypes' : RelationshipTypes,
        'suggestions' : getPeopleNearYou(currentParticipant, 100)
    })


@login_required
def relationships(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    friends = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.FRIENDS, 
        RelationshipTypes.GUEST_FRIENDS,
    ])
    friendRequestReceived = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.REQUEST_RECEIVED, 
    ])
    friendRequestSent = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.REQUEST_SENT, 
    ])
    groupOwner = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.GROUP_OWNER, 
    ])
    groupMember = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.GROUP_MEMBER, 
    ])
    groupMemberRequested = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.GROUP_MEMBER_REQUESTED, 
    ])
    groupMemberInvited = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.GROUP_MEMBER_INVITED, 
    ])

    context = {
        'current' : getCurrentUser(request),
        'friends' : friends,
        'friendRequestReceived' : friendRequestReceived,
        'friendRequestSent' : friendRequestSent,
        'groupOwner' : groupOwner,
        'groupMember' : groupMember,
        'groupMemberRequested' : groupMemberRequested,
        'groupMemberInvited' : groupMemberInvited,        
        'RelationshipTypes' : RelationshipTypes,
        'groupCount' : len(groupOwner) + len(groupMember),
        'requestReceivedCount' : len(friendRequestReceived) + len(groupMemberInvited),
        'requestSentCount' : len(friendRequestSent) + len(groupMemberRequested)
    }
    return render(request, 'relationships/relationships.html', context)

@login_required
def participant_search(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    searchString = request.GET.get("participant-search-txt")
    if searchString:
        matches = searchParticipants(currentParticipant, searchString)
    else:
        matches = None
    context = {
        'current' : getCurrentUser(request),
        'matches' : matches,
        'RelationshipTypes' : RelationshipTypes
    }
    return render(request, 'relationships/participant_search.html', context)


