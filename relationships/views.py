from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
from account.models import Participant

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
        currentParticipant = Participant.objects.get(user=request.user, participant_type='person')
        friendship = Friendship(person=currentParticipant.member.person, friend_id=friendId)
        friendship.save()
        #register event
        eventDict = {
            'person_id' : currentParticipant.id,
            'friend_id' : friendId,
        }
        registerEvent('add friend', eventDict)
        return redirect(url)
    return redirect('login')

@login_required
def remove_friend(request):
    print 'remove friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, participant_type='person')
        friendship = Friendship.objects.get(person=currentParticipant.member.person, friend_id=friendId)
        friendship.delete()
        return redirect(url)
    return redirect('login')

@login_required
def email_search(request):
    email = request.POST.getlist("email[]")
    firstName = request.POST.getlist("first_name[]")
    lastName = request.POST.getlist("last_name[]")
    currentParticipant = Participant.objects.get(user=request.user, participant_type='person')
    results = []
    for i, value in enumerate(email):
        if email[i] or (firstName[i] and lastName[i]):
            results.append( emailSearch(email[i], firstName[i], lastName[i], currentParticipant) )
    return render(request, 'email_search.html', {
        'current' : getCurrentUser(request), 
        'RelationshipTypes' : RelationshipTypes,
        'results' : results,
    })


@login_required
def relationships(request):
    currentParticipant = Participant.objects.get(user=request.user, participant_type='person')
    context = {
        'current' : getCurrentUser(request),
        'friends' : getFriends(currentParticipant),
        'friendRequests' : getFriendRequests(currentParticipant),
        'RelationshipTypes' : RelationshipTypes
    }
    return render(request, 'relationships.html', context)

@login_required
def participant_search(request):
    currentParticipant = Participant.objects.get(user=request.user, participant_type='person')
    searchString = request.GET.get("participant-search-txt")
    matches = searchParticipants(currentParticipant, searchString)
    context = {
        'current' : getCurrentUser(request),
        'matches' : matches,
        'RelationshipTypes' : RelationshipTypes
    }
    return render(request, 'participant_search.html', context)
