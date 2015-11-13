import os
import datetime
import string
import random

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from villagebuilder.settings import BASE_DIR

from account.models import Member, Participant, Group


def createRandomString(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def handle_uploaded_file(f, fileGroup='user_pics'):
    indexPath = BASE_DIR + '/villagebuilder/static/uploads/' + fileGroup + '.txt'
    indexFile = open(indexPath, 'a+')
    i = indexFile.read()
    indexFile.close()
    indexFile = open(indexPath, 'w')
    if i == '':
        j = 0
    else:
        j = 1 + int(i)
    indexFile.write(str(j))
    indexFile.close()
    fileName = 'image' + str(j) + '.png'
    path = BASE_DIR + '/villagebuilder/static/uploads/' + fileGroup + '/' + fileName
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return {
        'path' : '/static/uploads/' + fileGroup + '/' + fileName,
        'file' : fileName,
    }
    
def ifkeyset(arr, key, ifempty='', ifset='[+]'):
    if key in arr.keys():
        return ifset.replace('[+]', str(arr[key]))
    else:
        return ifempty
    
def ifset(val, ifempty='', ifset='[+]'):
    if val:
        return ifset.replace('[+]', str(val))
    else:
        return ifempty
    
def getCurrentUser(request):
    user = request.user
    participant = Participant.objects.get(user=user, type='member')
    member = Member.objects.get(participant=participant)
    groups = Group.objects.all().filter(participant__user=user, participant__type='group')
    return {
        'user' : user,
        'member' : member,
        'groups' : groups,
    }
    

    

    
    
    
    