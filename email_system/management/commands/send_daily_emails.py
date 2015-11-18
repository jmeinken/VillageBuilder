import time

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import timezone

from account.models import Participant
from requests.helpers import getRequestsOfFriends, getRelevantRequestComments
from sharing.helpers import getItemsForParticipant
from relationships.helpers import getFriendInvites, getFriendConfirmations
from pm.models import Message
from email_system.helpers import sendMail



class Command(BaseCommand):

    help = 'Call with: python manage.py send_daily_emails [--testing]'
    
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--testing',
            action='store_true',
            dest='testing',
            default=False,
            help='Do not actually send emails or update database')

    def handle(self, *args, **options):
        memberParticipants = Participant.objects.all().filter(type="member")
        self.stdout.write('total people: ' + str(memberParticipants.count()))
        if options['testing']:
            self.stdout.write("Just testing")
        for participant in memberParticipants:
            lastLogin = participant.user.last_login
            lastEmailed = participant.member.last_emailed
            cutoffDate = max([lastLogin, lastEmailed])
            data = {
                'friend_invites' : {},
                'friend_confirmations' : {},
                'messages' : {},
                'requests' : {},
                'request_comments' : {},
                'items' : {},
            }
            mem = participant.member
            data['friend_invites']['pref'] = mem.email_friend_requests == mem.EMAIL_DAILY_DIGEST
            data['friend_confirmations']['pref'] = mem.email_friend_requests == mem.EMAIL_DAILY_DIGEST
            data['messages']['pref'] = mem.email_pm == mem.EMAIL_DAILY_DIGEST
            data['requests']['pref'] = mem.email_requests == mem.EMAIL_DAILY_DIGEST
            data['request_comments']['pref'] = mem.email_request_comments == mem.EMAIL_DAILY_DIGEST
            data['items']['pref'] = mem.email_shared_items == mem.EMAIL_DAILY_DIGEST
            # new requests for participant
            if data['requests']['pref']:
                data['requests']['coll'] = getRequestsOfFriends(participant, cutoffDate)
                data['requests']['count'] = data['requests']['coll'].count()
            # new request comments for participant
            if data['request_comments']['pref']:
                data['request_comments']['coll'] = getRelevantRequestComments(participant, cutoffDate)
                data['request_comments']['count'] = len(data['request_comments']['coll'])
            # new shared items for participant
            if data['items']['pref']:
                data['items']['coll'] = getItemsForParticipant(participant).filter(share_date__gte=cutoffDate)
                data['items']['count'] = data['items']['coll'].count()
            # new friend requests for participant
            if data['friend_invites']['pref']:
                data['friend_invites']['coll'] = getFriendInvites(participant, cutoffDate)
                data['friend_invites']['count'] = data['friend_invites']['coll'].count()
            # new friend confirmations for participant
            if data['friend_confirmations']['pref']:
                data['friend_confirmations']['coll'] = getFriendConfirmations(participant, cutoffDate)
                data['friend_confirmations']['count'] = data['friend_confirmations']['coll'].count()
            # new pm's for participant
            if data['messages']['pref']:
                data['messages']['coll'] = Message.objects.filter(recipient=participant)
                data['messages']['coll'] = data['messages']['coll'].filter(sent_on__gte=cutoffDate)
                data['messages']['count'] = data['messages']['coll'].count()
                
            self.stdout.write('----------------------------------------------') 
            self.stdout.write(str(participant.id) + ": " + participant.get_name())
            self.stdout.write('login: ' + str(lastLogin) + "; last emailed: " + str(lastEmailed))
            for key in data:
                if data[key]['pref']:
                    self.stdout.write(key + ": " + str(data[key]['count']))
            
            # determine if there is anything to send
            counts = []
            for key in data:
                if data[key]['pref']:
                    counts.append(data[key]['count'])
                            
            if max(counts) > 0:
                context = {
                    'name' : participant.get_name(),
                    'data' : data,
                }
                body = render_to_string('email/plain_text/daily_update.txt', context)
                htmlBody = render_to_string('email/html/daily_update.html', context)
                # self.stdout.write('--------') 
                # self.stdout.write(htmlBody)
                if not options['testing']:
                    email = participant.user.username
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
            
            
            