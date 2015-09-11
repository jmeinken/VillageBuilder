
import datetime

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from villagebuilder.settings import BASE_DIR


def email_forgot_password(request, member):
    email = member.participant.user.username
    context = {
        'name' : member.participant.get_name(), 
        'link' : request.build_absolute_uri(reverse('reset_password', args=[member.code])),
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
    if pm.recipient.type == 'member' and pm.recipient.member.email_messages:
        email = pm.recipient.user.username
        context = {
            'name' : pm.recipient.get_name(),
            'sender_name' : pm.sender.get_name(),
            'pmMessage' : pm.body,
            'link' : request.build_absolute_uri(reverse('pm:messages', args=[pm.sender.id])),
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
    if friendship.friend.email_friend_requests:
        email = friendship.friend.participant.user.username
        context = {
            'name' : friendship.friend.participant.get_name(),
            'requester_name' : friendship.member.participant.get_name(),
            'link' : request.build_absolute_uri(reverse('account:view', args=[friendship.member.id])),
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