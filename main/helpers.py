from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from villagebuilder.settings import BASE_DIR

from account.models import Member, Participant, Person

def handle_uploaded_file(f):
    indexPath = BASE_DIR + '/main/static/uploads/user_pics.txt'
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
    fileName = 'user' + str(j) + '.png'
    path = BASE_DIR + '/main/static/uploads/user_pics/' + fileName
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return {
        'path' : '/static/uploads/user_pics/' + fileName,
        'file' : fileName,
    }
    
def ifkeyset(arr, key, ifempty='', ifset='[+]'):
    if key in arr.keys():
        return ifset.replace('[+]', str(arr[key]))
    else:
        return ifempty
    
def getCurrentUser(request):
    user = request.user
    participant = Participant.objects.get(user=user, participant_type='person')
    member = Member.objects.get(participant=participant)
    return {
        'user' : user,
        'member' : member,
    }
    

    
    
    
    