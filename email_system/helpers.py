
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
    body = render_to_string('email/forgot_password.html', context)
    sendMail(
        'forgot password', 
        body,
        'info@villagebuilder.net', 
        [email], 
    )


# this should only be called from other methods in the email system
def sendMail(subject, message, fromMail, toList, failSilently=False):
    try:
        send_mail(subject, message, fromMail, toList, failSilently)
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