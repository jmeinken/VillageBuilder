from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Member, Participant
from main.helpers import getCurrentUser

from .forms import NewMessageForm, NewConversationMessageForm
from .models import *
from .helpers import *



@login_required
def messages(request, participantId):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    if request.method == "POST":
        newMessageForm = NewMessageForm(currentParticipant, request.POST)
        if newMessageForm.is_valid():
            message = newMessageForm.save(commit=False)
            message.sender = currentParticipant
            message.save()
    participants = getParticipantsWithRecentMessages(currentParticipant)
    if participantId != '0':
        talkingTo = Participant.objects.get(id=participantId)
        messages = getConversation(talkingTo, currentParticipant)
        form = NewConversationMessageForm(participantId)
    else:
        messages = False
        form = NewMessageForm(currentParticipant)
    context = {
        'messages' : messages,
        'conversation' : participantId,
        'current' : getCurrentUser(request),
        'newMessageForm' : form,
        'participants' : participants
    }
    return render(request, 'pm/messages.html', context)
