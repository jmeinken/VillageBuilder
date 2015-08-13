from django.db.models import Q

from account.models import Participant
from relationships.helpers import getParticipant

from .models import Message

# returns a list of participants with recent activity
def getParticipantsWithRecentMessages(currentParticipant, count=10):
    participants = Participant.objects.all().filter(
        Q(message_sent_set__recipient=currentParticipant) |
        Q(message_received_set__sender=currentParticipant)                            
    ).distinct()
    results = []
    for participant in participants:
        results.append(getParticipant(participant.id, currentParticipant))
    return results

def getConversation(participant, currentParticipant, count=10):
    messages = Message.objects.all().filter(
        ( Q(sender=participant) & Q(recipient=currentParticipant) ) |
        ( Q(sender=currentParticipant) & Q(recipient=participant) )
    )
    return messages