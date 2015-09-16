from datetime import timedelta

from django.utils import timezone
from django.template.loader import render_to_string

from account.models import Participant
from requests.helpers import getRequestsOfFriends, getRelevantRequestComments
from sharing.helpers import getItemsForParticipant
from .helpers import sendMail



def sendDailyUpdates(lastLoginInterval=None, lastEmailedInterval=None):
    '''Run once a day to send updates.  Pass arguments for testing.'''
    # get all members to loop through
    memberParticipants = Participant.objects.all().filter(type="member")
    print memberParticipants.count()
    for participant in memberParticipants:
        print 'new loop ' + participant.get_name()
        now = timezone.now()
        if lastLoginInterval:
            lastLogin = timezone.now() - timedelta(days=lastLoginInterval)
        else:
            lastLogin = participant.user.last_login
            print lastLogin
        if lastEmailedInterval:
            lastEmailed = timezone.now() - timedelta(days=lastEmailedInterval)
        else:
            lastEmailed = participant.member.last_emailed
            print lastEmailed
        if abs((now.date() - lastLogin.date()).days) < 1:         # is this rounded integer or float?
            continue
        if lastLogin > lastEmailed:
            sinceDate = lastLogin
        else:
            sinceDate = lastEmailed
        requests = getRequestsOfFriends(participant, sinceDate)
        requestComments = getRelevantRequestComments(participant, sinceDate)
        items = getItemsForParticipant(participant)
        items = items.filter(share_date__gte=sinceDate)
        boolSendEmail = False
        print 'request count/requestComment count/item count'
        print requests.count()
        print len(requestComments)
        print items.count()
        # send if there are any new requests from friends
        if requests.count() > 0:
            boolSendEmail = True
        # send if there are any new request comments and it has been more than 2 days
        if len(requestComments) > 0 and abs((now.date() - sinceDate.date()).days) >= 2:
            boolSendEmail = True
        # send if there are any new items from friends and it has been more than 7 days
        if items.count() > 0 and abs((now.date() - sinceDate.date()).days) >= 7:
            boolSendEmail = True
        if not boolSendEmail:
            continue
        # we're ready to send that email
        print 'participant id and name/request count/item count'
        print(participant.id)
        print(participant.get_name())
        print(requests.count())
        print(items.count())
        email = participant.user.username
        context = {
            'name' : participant.get_name(),
            'requests' : requests,
            'requestComments' : requestComments,
            'items' : items,
        }
        body = render_to_string('email/plain_text/daily_update.txt', context)
        htmlBody = render_to_string('email/html/daily_update.html', context)
        sendMail(
            'Recent activity update', 
            body,
            htmlBody,
            'info@villagebuilder.net', 
            [email], 
        )
        
        
            
        
        