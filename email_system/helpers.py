
import datetime

from villagebuilder.settings import BASE_DIR


def email_forgot_password(member):
    email = member.participant.user.username
    sendMail(
        'forgot password', 
        'Your temporary code is: ' + member.code, 
        'john.meinken@uc.edu', 
        [email], 
    )


# this should only be called from other methods in the email system
def sendMail(subject, message, fromMail, toList, failSilently=False):
    try:
        send_mail(subject, message, fromMail, toList, failSilently)
        action = 'SENT'
    except:
        action = 'FAIL'
    logDir = BASE_DIR + '/email_system/logs/'
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