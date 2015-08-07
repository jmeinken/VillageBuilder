from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from account.helpers import *
from main.helpers import *
from relationships.helpers import *
from alerts.helpers import *
from requests.helpers import *

@login_required
def home(request):
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    context = {
            'current' : getCurrentUser(request),
            'peopleNearYou' : getPeopleNearYou(currentParticipant),
            'friendsOfFriends' : getFriendsOfFriends(currentParticipant),
            'RelationshipTypes' : RelationshipTypes,
            'requests' : getRequestList(currentParticipant)
        }
    return render(request, 'core/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def test_view(request):
    return HttpResponse("It worked!")
