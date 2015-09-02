import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import contrib




from account.models import Member, Participant
from main.helpers import getCurrentUser

from .forms import NewMessageForm
from .models import *
from .helpers import *



@login_required
@csrf_exempt
def message_list(request):
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    messages = Message.objects.all().filter(recipient=currentParticipant).filter(viewed=False).order_by('-sent_on')
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
    # !!don't create any variables with the name 'messages', especially for the context
    # passed to the template
    print participantId
    participantId = int(participantId)
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    # post new message
    if request.method == "POST":
        newMessageForm = NewMessageForm(request.POST, participant=currentParticipant)
        if newMessageForm.is_valid():
            message = newMessageForm.save(commit=False)
            message.sender = currentParticipant
            message.save()
            contrib.messages.success(request, "Message sent to " + message.recipient.get_name() + '.')
            return redirect(reverse("pm:messages", args=[message.recipient.id]))
    participants = getParticipantsWithRecentMessages(currentParticipant)
    if participantId != 0:
        talkingTo = Participant.objects.get(id=participantId)
        messageList = getConversation(talkingTo, currentParticipant)
        messageList.filter(sender=talkingTo).update(viewed=True)
        form = NewMessageForm(participant=currentParticipant, initial={
            'recipient' : talkingTo,
            'body' : request.GET.get('msg')
        })
    else:
        messageList = []
        form = NewMessageForm(participant=currentParticipant)
        talkingTo = None
    context = {
        'messageList' : messageList,
        'conversation' : participantId,
        'participant' : talkingTo,
        'current' : getCurrentUser(request),
        'newMessageForm' : form,
        'participants' : participants,
    }
    return render(request, 'pm/messages.html', context)
