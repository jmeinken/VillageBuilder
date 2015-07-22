from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q

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

    