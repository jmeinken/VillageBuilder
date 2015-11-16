from django.core.management.base import BaseCommand, CommandError

from account.models import Participant
from requests.helpers import getRequestsOfFriends, getRelevantRequestComments
from sharing.helpers import getItemsForParticipant
from relationships.helpers import getFriendInvites, getFriendConfirmations
from pm.models import Message

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
        print memberParticipants.count()
        if options['testing']:
            self.stdout.write("Just testing")
        for participant in memberParticipants:
            lastLogin = participant.user.last_login
            lastEmailed = participant.member.last_emailed
            cutoffDate = max([lastLogin, lastEmailed])
            prefs = {
                'email_friend_requests' : participant.member.email_friend_requests,
                'email_pm' : participant.member.email_pm,
                'email_requests' : participant.member.email_requests,
                'email_request_comments' : participant.member.email_request_comments,
                'email_shared_items' : participant.member.email_shared_items,
            }
            self.stdout.write(str(cutoffDate))
            # new requests for participant
            requests = getRequestsOfFriends(participant, cutoffDate)
            # new request comments for participant
            requestComments = getRelevantRequestComments(participant, cutoffDate)
            # new shared items for participant
            items = getItemsForParticipant(participant)
            items = items.filter(share_date__gte=cutoffDate)
            # new friend requests for participant
            friendInvites = getFriendInvites(participant, cutoffDate)
            # new friend confirmations for participant
            friendConfirmations = getFriendConfirmations(participant, cutoffDate)
            #new pm's for participant
            messages = Message.objects.filter(recipient=participant)
            messages = messages.filter(sent_on__gte=cutoffDate)
            
            
            
            self.stdout.write(str(requests.count()))
            self.stdout.write(str(len(requestComments)))
            self.stdout.write(str(items.count()))
            self.stdout.write(str(friendInvites.count()))
            self.stdout.write(str(friendConfirmations.count()))
            self.stdout.write(str(messages.count()))
            