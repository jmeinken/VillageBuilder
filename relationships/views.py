from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import *
from account.models import Participant




@login_required
def add_friend(request):
    print 'add friend'
    if request.method == "POST":
        url = request.POST.get("redirect")
        friendId = request.POST.get("friend-id")
        currentParticipant = Participant.objects.get(user=request.user, participant_type='person')
        friendship = Friendship(person=currentParticipant.member.person, friend_id=friendId)
        friendship.save()
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
