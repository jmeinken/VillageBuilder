
import datetime

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from villagebuilder.settings import BASE_DIR
from sharing.helpers import *
from requests.helpers import *


def email_forgot_password(request, member):
    email = member.participant.user.username
    context = {
        'email_title' : 'VillageBuilder Password Reset',
        'name' : member.participant.get_name(), 
        'link' : request.build_absolute_uri(reverse('reset_password', args=[member.code])),
        'unsubscribe' : member.get_unsubscribe_code(),
    }
    body = render_to_string('email/plain_text/forgot_password.txt', context)
    htmlBody = render_to_string('email/html/forgot_password.html', context)
    return sendMail(
        'forgot password', 
        body,
        htmlBody,
        'info@villagebuilder.net', 
        [email], 
    )
    
def email_new_pm(request, pm):
    
    if pm.recipient.type == 'member':
        if pm.recipient.member.email_pm == pm.recipient.member.EMAIL_IMMEDIATELY:
            email = pm.recipient.user.username
            context = {
                'email_title' : 'New Message on VillageBuilder',
                'name' : pm.recipient.get_name(),
                'sender_name' : pm.sender.get_name(),
                'pmMessage' : pm.body,
                'link' : request.build_absolute_uri(reverse('pm:messages', args=[pm.sender.id])),
                'unsubscribe' : pm.recipient.member.get_unsubscribe_code(),
            }
            body = render_to_string('email/plain_text/new_pm.txt', context)
            htmlBody = render_to_string('email/html/new_pm.html', context)
            return sendMail(
                'New message from ' + pm.sender.get_name(), 
                body,
                htmlBody,
                'info@villagebuilder.net', 
                [email], 
            )
    
def email_friend_request(request, friendship):
    if friendship.friend.email_friend_requests == friendship.friend.EMAIL_IMMEDIATELY:
        email = friendship.friend.participant.user.username
        context = {
            'email_title' : 'New Friend Request on VillageBuilder',
            'name' : friendship.friend.participant.get_name(),
            'requester_name' : friendship.member.participant.get_name(),
            'link' : request.build_absolute_uri(reverse('account:view', args=[friendship.member.id])),
            'unsubscribe' : friendship.friend.get_unsubscribe_code(),
        }
        body = render_to_string('email/plain_text/friend_request.txt', context)
        htmlBody = render_to_string('email/html/friend_request.html', context)
        return sendMail(
            friendship.member.participant.get_name() + ' wants to be friends', 
            body,
            htmlBody,
            'info@villagebuilder.net', 
            [email], 
        )
        
def email_friend_confirmation(request, friendship):
    if friendship.friend.email_friend_requests == friendship.friend.EMAIL_IMMEDIATELY:
        items = getItemsForParticipant(friendship.friend.participant)
        items = filterItems(items, sharerId=friendship.member.id)
        email = friendship.friend.participant.user.username
        context = {
            'email_title' : 'Friendship Confirmation on VillageBuilder',
            'name' : friendship.friend.participant.get_name(),
            'requester_name' : friendship.member.participant.get_name(),
            'link' : request.build_absolute_uri( reverse('sharing:items') 
                + '?sharer=' 
                +  str(friendship.member.id)
            ),
            'items' :items,
            'unsubscribe' : friendship.friend.get_unsubscribe_code(),
        }
        body = render_to_string('email/plain_text/friend_confirmation.txt', context)
        htmlBody = render_to_string('email/html/friend_confirmation.html', context)
        return sendMail(
            'You are now friends with ' + friendship.member.participant.get_name(), 
            body,
            htmlBody,
            'info@villagebuilder.net', 
            [email], 
        )
        
def email_new_item(request, item):
    # who is this item shared with?
    participants = getParticipantsForItem(item)
    print '---' + item.title + '--------------------'
    for participant in participants:
        print str(participant.id) + ': ' + participant.get_name()
    print '------------------------------------------'
    
    for participant in participants:
        if participant.member.email_shared_items == participant.member.EMAIL_IMMEDIATELY:
            context = {
                'email_title' : 'New Item on VillageBuilder',
                'name' : participant.get_name(),
                'item' : item,
                'unsubscribe' : participant.member.get_unsubscribe_code(),       
            }
            body = render_to_string('email/plain_text/new_item.txt', context)
            htmlBody = render_to_string('email/html/new_item.html', context)
            email = participant.user.username
            sendMail(
                item.sharer.participant.get_name() + ' shared something with you', 
                body,
                htmlBody,
                'info@villagebuilder.net', 
                [email], 
            )

def email_new_request(request, new_request):
    participants = getViewersForRequest(new_request)
    print '---Request ' + str(new_request.id) + '--------------------'
    for participant in participants:
        print str(participant.id) + ': ' + participant.get_name()
    print '------------------------------------------'
    for participant in participants:
        if participant.member.email_requests == participant.member.EMAIL_IMMEDIATELY:
            context = {
                'email_title' : 'New Post on VillageBuilder',
                'name' : participant.get_name(),
                'request' : new_request,
                'unsubscribe' : participant.member.get_unsubscribe_code(),       
            }
            body = render_to_string('email/plain_text/new_request.txt', context)
            htmlBody = render_to_string('email/html/new_request.html', context)
            email = participant.user.username
            sendMail(
                'new request from ' + new_request.member.participant.get_name(), 
                body,
                htmlBody,
                'info@villagebuilder.net', 
                [email], 
            )


def email_new_request_comment(request, request_comment):
    participants = getViewersForRequestComment(request_comment)
    print '---Request Comment ' + str(request_comment.id) + '--------------------'
    for participant in participants:
        print str(participant.id) + ': ' + participant.get_name()
    print '------------------------------------------'
    for participant in participants:
        if participant.member.email_request_comments == participant.member.EMAIL_IMMEDIATELY:
            context = {
                'email_title' : 'New Comment on VillageBuilder',
                'name' : participant.get_name(),
                'request_comment' : request_comment,
                'unsubscribe' : participant.member.get_unsubscribe_code(),       
            }
            body = render_to_string('email/plain_text/new_request_comment.txt', context)
            htmlBody = render_to_string('email/html/new_request_comment.html', context)
            email = participant.user.username
            sendMail(
                'new comment from ' + request_comment.member.participant.get_name(), 
                body,
                htmlBody,
                'info@villagebuilder.net', 
                [email], 
            )


# this should only be called from other methods in the email system
def sendMail(subject, message, htmlMessage, fromMail, toList, failSilently=False):
    subject = '[VillageBuilder] ' + subject
    try:
        send_mail(subject, message, fromMail, toList, failSilently, html_message=htmlMessage)
        action = 'SENT'
    except:
        action = 'FAIL'
    logDir = BASE_DIR + '/villagebuilder/logs/'
    myFile = open(logDir + 'emails.txt', 'a+')
    myFile.write(
        action + '\t' +
        str(datetime.datetime.now()) + '\t' +
        subject + '\t' +
        'from:' + fromMail + '\t' +
        'to:' + str(toList) + '\n'
    )
    myFile.close()
    myFile = open(logDir + 'emails_full.txt', 'a+')
    myFile.write(
        '-----------------------------------------------------' + '\n'
        'time: ' + str(datetime.datetime.now()) + '\n' +
        'subject: ' + subject + '\n' +
        'from: ' + fromMail + '\n' +
        'to: ' + str(toList) + '\n' + 
        'body:' + '\n' + 
        message + '\n' + 
        '-----------------------------------------------------' + '\n'
    )
    myFile.close()
    if action == 'SENT':
        return True
    else:
        return False