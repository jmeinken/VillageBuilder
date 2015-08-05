import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.models import User

from .models import *
from account.models import Participant, Guest

from account.helpers import *
from main.helpers import *
from relationships.helpers import *
from alerts.helpers import registerEvent



@login_required
@csrf_exempt
def add_friend(request):
    print 'add friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        friendship = Friendship(member=currentParticipant.member, friend_id=friendId)
        friendship.save()
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
            return redirect(url)
    return redirect('login')

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
            groupMembership.invited = True
            groupMembership.save()
        return redirect(url)
    return redirect('login')

@login_required
def join_group(request):
    print 'join_group'
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        groupMembership = GroupMembership.objects.all().filter(member=currentParticipant.member, group_id=groupId)
        if groupMembership.count() == 0:
            groupMembership = GroupMembership(member=currentParticipant.member, group_id=groupId)
        else:
            groupMembership = groupMembership[0]
        groupMembership.requested = True
        groupMembership.save()
        #register event
        #eventDict = {
        #    'member_id' : currentParticipant.id,
        #    'friend_id' : friendId,
        #}
        # registerEvent('add friend', eventDict)
        return redirect(url)
    return redirect('login')

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
        groupMembership.invited = True
        groupMembership.save()
        return redirect(url)
    return redirect('login')

def remove_from_group(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        groupId = request.POST.get("group-id")
        memberId = request.POST.get("member-id")
        groupMembership = GroupMembership.objects.get(member_id=memberId, group_id=groupId)
        if groupMembership.requested:
            groupMembership.invited = False
            groupMembership.save()
        else:
            groupMembership.delete()
        return redirect(url)
    return redirect('login')


@login_required
@csrf_exempt
@transaction.atomic
def create_guest(request):
    print 'create guest'
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
            user.first_name = guestFirstName
            user.last_name = guestLastName
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
def remove_friend(request):
    print 'remove friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        friendship = Friendship.objects.get(member=currentParticipant.member, friend_id=friendId)
        friendship.delete()
        return redirect(url)
    return redirect('login')

@login_required
def remove_guest_friend(request):
    print 'remove guest friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, type='person')
        guestFriendship = GuestFriendship.objects.get(person=currentParticipant.member.person, guest_id=friendId)
        guestFriendship.delete()
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
def relationships(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    context = {
        'current' : getCurrentUser(request),
        'friends' : getFriends(currentParticipant),
        'friendRequests' : getFriendRequests(currentParticipant),
        'RelationshipTypes' : RelationshipTypes
    }
    return render(request, 'relationships/relationships.html', context)

@login_required
def participant_search(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    searchString = request.GET.get("participant-search-txt")
    matches = searchParticipants(currentParticipant, searchString)
    context = {
        'current' : getCurrentUser(request),
        'matches' : matches,
        'RelationshipTypes' : RelationshipTypes
    }
    return render(request, 'relationships/participant_search.html', context)
