from django.db.models import Q
from django.db.models import Max

from account.models import Participant
from relationships.helpers import getParticipant

from .models import Message

# returns a list of participants with recent activity
def getParticipantsWithRecentMessages(currentParticipant, count=10):
    participants = Participant.objects.all().filter(
        Q(message_sent_set__recipient=currentParticipant) |
        Q(message_received_set__sender=currentParticipant)                            
    ).annotate(received_date=Max('message_received_set__sent_on')).distinct().order_by('received_date')
    results = []
    for participant in participants:
        result = getParticipant(participant.id, currentParticipant)
        messages = currentParticipant.message_received_set.all().filter(sender=participant)
        hasUnviewedMessages = False
        for message in messages:
            print message.recipient
            if not message.viewed :
                hasUnviewedMessages = True
        result['has_unviewed_messages'] = hasUnviewedMessages
        results.append(result)
    return results

def getConversation(participant, currentParticipant, count=10):
    messages = Message.objects.all().filter(
        ( Q(sender=participant) & Q(recipient=currentParticipant) ) |
        ( Q(sender=currentParticipant) & Q(recipient=participant) )
    ).order_by('sent_on')
    return messages