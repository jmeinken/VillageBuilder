import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.urlresolvers import reverse



from account.models import Member, Participant
from main.helpers import getCurrentUser

from .forms import NewMessageForm, NewConversationMessageForm
from .models import *
from .helpers import *



@login_required
@csrf_exempt
def message_list(request):
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    messages = Message.objects.all().filter(recipient=currentParticipant).filter(viewed=False)
    context = {
            'messages' : messages,
        }
    html = render_to_string('pm/message_list.html', context)
    data = {
        'html' : html,
        'count' : messages.count()
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")



@login_required
def messages(request, participantId):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    if request.method == "POST":
        newMessageForm = NewMessageForm(currentParticipant, request.POST)
        if newMessageForm.is_valid():
            message = newMessageForm.save(commit=False)
            message.sender = currentParticipant
            message.save()
            return redirect(reverse("pm:messages", args=[message.recipient.id]))
    participants = getParticipantsWithRecentMessages(currentParticipant)
    if participantId != '0':
        talkingTo = Participant.objects.get(id=participantId)
        messageList = getConversation(talkingTo, currentParticipant)
        messageList.filter(sender=talkingTo).update(viewed=True)
        form = NewConversationMessageForm(participantId)
    else:
        messageList = []
        form = NewMessageForm(currentParticipant)
    context = {
        'messages' : messageList,
        'conversation' : int(participantId),
        'current' : getCurrentUser(request),
        'newMessageForm' : form,
        'participants' : participants,
    }
    return render(request, 'pm/messages.html', context)
