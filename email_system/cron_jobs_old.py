from datetime import timedelta
import time

from django.utils import timezone
from django.template.loader import render_to_string

from account.models import Participant
from requests.helpers import getRequestsOfFriends, getRelevantRequestComments
from sharing.helpers import getItemsForParticipant
from .helpers import sendMail



def sendDailyUpdates(lastLoginInterval=None, lastEmailedInterval=None, testing=False):
    '''Run once a day to send updates.  Pass arguments for testing.'''
    # get all members to loop through
    memberParticipants = Participant.objects.all().filter(type="member")
    print memberParticipants.count()
    for participant in memberParticipants:
        now = timezone.now()
        if lastLoginInterval:
            lastLogin = timezone.now() - timedelta(days=lastLoginInterval)
        else:
            lastLogin = participant.user.last_login
        if lastEmailedInterval:
            lastEmailed = timezone.now() - timedelta(days=lastEmailedInterval)
        else:
            lastEmailed = participant.member.last_emailed
        if abs((now.date() - lastLogin.date()).days) < 1:         # is this rounded integer or float?
            print participant.get_name() + ': lastlogin, lastemailed, action'
            print(str(lastLogin) + ':' + str(lastEmailed) + ':no email-rencently logged in')
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
            print participant.get_name() + ': lastlogin, lastemailed, req, comment, items, action'
            print(str(lastLogin) + ':' 
                  + str(lastEmailed) + ':'
                  + str(requests.count()) + ':'
                  + str(len(requestComments)) + ':'
                  + str(items.count())  + ':'
                  + ':no email-nothing to show')
            continue
        # we're ready to send that email
        email = participant.user.username
        context = {
            'name' : participant.get_name(),
            'requests' : requests,
            'requestComments' : requestComments,
            'items' : items,
        }
        body = render_to_string('email/plain_text/daily_update.txt', context)
        htmlBody = render_to_string('email/html/daily_update.html', context)
        print participant.get_name() + ': lastlogin, lastemailed, req, comment, items, action'
        print(str(lastLogin) + ':' 
              + str(lastEmailed) + ':'
              + str(requests.count()) + ':'
              + str(len(requestComments)) + ':'
              + str(items.count())  + ':'
              + ':emailed')
        if not testing:
            sendMail(
                'Recent activity update', 
                body,
                htmlBody,
                'info@villagebuilder.net', 
                [email], 
            )
            member = participant.member
            member.last_emailed = timezone.now()
            member.save()
        time.sleep(1)
        
        
            
        
        