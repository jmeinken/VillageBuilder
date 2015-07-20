from django.core.urlresolvers import reverse
from enum import Enum

from villagebuilder.settings import BASE_DIR

from .models import Member, Participant, Person

# used by account creation views to render wizard navigation
def build_nav(request, current_view):
    if current_view == 'account_info':
        nav_account_info = { 'label' : 'Account Info', 'class_attr' : 'active disabled' }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        if 'account_info' in request.session.keys():
            nav_address = { 'label' : 'Address', 'link' : reverse('account:address') }
        else:
            nav_address = { 'label' : 'Address', 'class_attr' : 'disabled' }
        if 'address'  in request.session.keys():
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'link' : reverse('account:personal_info') }
        else:
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'class_attr' : 'disabled' }
    if current_view == 'address':
        nav_address = { 'label' : 'Address', 'class_attr' : 'active disabled' }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        nav_account_info = { 'label' : 'Account Info', 'link' : reverse('account:account_info') }
        if 'address'  in request.session.keys():
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'link' : reverse('account:personal_info') }
        else:
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'class_attr' : 'disabled' }   
    if current_view == 'personal_info':
        nav_account_info = { 'label' : 'Account Info', 'link' : reverse('account:account_info') }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        nav_address = { 'label' : 'Address', 'link' : reverse('account:address') }
        nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'class_attr' : 'active disabled' }
    return [nav_account_info, nav_address, nav_personal_info, nav_complete]

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
    member = Member.objects.get(member=participant)
    return {
        'user' : user,
        'member' : member,
    }
    
def getPeopleNearYou(currentParticipant):
    participants = Participant.objects.all()
    results = []
    for participant in participants:
        results.append(getParticipant(participant.id, currentParticipant))
    return results
    
    
    
def getParticipant(participantId, currentParticipant):
    participant = Participant.objects.get(id=participantId)
    # member = Member.objects.get(member=participant)
    return {
        'id' : participant.id,
        'name' : participant.user.first_name + ' ' + participant.user.last_name,
        'display_address' : participant.member.get_display_address(),
        'user_pic' : participant.member.get_user_pic(),
        'relationship' : getRelationship(currentParticipant, participant),
    }
    
class RelationshipTypes():
    SELF = 0
    FRIENDS = 1
    NOT_FRIENDS = 2
    REQUEST_SENT = 3
    REQUEST_RECEIVED = 4
    
def getRelationship(currentParticipant, participant):
    forward = False
    backward = False
    if currentParticipant == participant:
        return RelationshipTypes.SELF
    for friendship in currentParticipant.member.person.friendship_set.all():
        if friendship.friend == participant.member.person:
            forward = True
    for friendship in currentParticipant.member.person.reverse_friendship_set.all():
        if friendship.person == participant.member.person:
            backward = True
    if forward and backward:
        return RelationshipTypes.FRIENDS
    if forward:
        return RelationshipTypes.REQUEST_SENT
    if backward:
        return RelationshipTypes.REQUEST_RECEIVED
    return RelationshipTypes.NOT_FRIENDS
    
    
    
    
    
    
    
    
    