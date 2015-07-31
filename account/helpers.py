from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from villagebuilder.settings import BASE_DIR

from .models import Member, Participant, Person, Guest
from relationships.helpers import *

# used by account creation views to render wizard navigation
def build_nav(request, current_view):
    if current_view == 'account_info':
        nav_account_info = { 'label' : 'Account Info', 'class_attr' : 'active disabled' }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        nav_address = { 'label' : 'Address', 'link' :  '#', 'id' : 'address-link'}
        if 'address'  in request.session.keys():
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'link' : '#', 'id' : 'personal-info-link' }
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

def getParticipantInfo(participantId, currentParticipant, basic=True):
    participant = Participant.objects.get(id=participantId)
    relationship = getRelationship(currentParticipant, participant)
    if (    relationship == RelationshipTypes.SELF 
            or relationship == RelationshipTypes.FRIENDS
            or relationship == RelationshipTypes.REQUEST_RECEIVED
       ):
        result = getInfoForFriend(participant, currentParticipant)
    else:
        result = getInfoForNonFriend(participant, currentParticipant)
    result['relationship'] = relationship
    return result

def getInfoForFriend(participant, currentParticipant):
    result = {}
    if participant.participant_type == 'person':
        member = Member.objects.get(participant=participant)
        person = Person.objects.get(member=member)
        result['name'] = participant.user.get_full_name()
    if participant.participant_type == 'guest':
        guest = Guest.objects.get(guest=guest)
        result['name'] = participant.user.get_full_name()
    return result    
        
def getInfoForNonFriend(participant, currentParticipant):
    result = {}
    if participant.participant_type == 'person':
        member = Member.objects.get(participant=participant)
        person = Person.objects.get(member=member)
        result['name'] = participant.user.get_full_name()
    if participant.participant_type == 'guest':
        guest = Guest.objects.get(guest=guest)
        result['name'] = participant.user.get_full_name()
    return result          
        
        
        