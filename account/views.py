import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate

from villagebuilder.utils import console
from .forms import *
from .models import Member, Participant

from account.helpers import *
from main.helpers import *
from relationships.helpers import *
from sharing.helpers import *
from relationships.models import GroupMembership



    
@login_required
def delete_group(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    if request.method == "POST":
        groupId = request.POST.get('group_id')
        group = Group.objects.get(pk=groupId)
        groupName = group.title
        if group.owner == currentParticipant.member:
            group.delete()
        messages.success(request, 'Your group ' + groupName + ' was successfully deleted.')
    return redirect(reverse('home'))



@login_required
def view(request, participantId):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    accountInfo = getParticipantFull(participantId, currentParticipant)
    participant = Participant.objects.get(pk=participantId)
    if participant.type == 'member':
        relTypes = [
            RelationshipTypes.FRIENDS,
            RelationshipTypes.GUEST_FRIENDS,
        ]
        relations = getRelations(participant, currentParticipant, relTypes)
        allItems = getItemsSharedByAndForParticipant(currentParticipant)
        items = filterItems(allItems, sharerId=participant.id) 
    if participant.type == 'group':
        relTypes = [
            RelationshipTypes.GROUP_OWNER,
            RelationshipTypes.GROUP_MEMBER,
        ]
        relations = getRelations(participant, currentParticipant, relTypes)
        allItems = getItemsSharedByAndForParticipant(currentParticipant)
        items = filterItems(allItems, groupId=participant.id) 
    if participant.type == 'guest':
        relTypes = [
            RelationshipTypes.GUEST_FRIENDS,
        ]
        relations = getRelations(participant, currentParticipant, relTypes)
        items = None
    context = {
        'account' : accountInfo,
        'relations' : relations,
        'RelationshipTypes' : RelationshipTypes,
        'current' : getCurrentUser(request),
        'items' : items,
    }
    return render(request, 'account/account_view.html', context)

@login_required
def account(request):
    print 'OK'
    showEditView = ''
    user = request.user
    userEmailForm = UserEmailForm(instance=user)
    userNameForm = UserNameForm(instance=user)
    userPasswordForm = UserPasswordForm(user)
    participant = Participant.objects.get(user=user, type='member')
    member = Member.objects.get(participant=participant)
    addressForm = AddressForm(instance=member)
    memberPrivacyForm = MemberPrivacyForm(instance=member)
    memberPhoneForm = MemberPhoneForm(instance=member)
    memberDisplayAddressForm = MemberDisplayAddressForm(instance=member)
    if request.method == "POST":
        formName = request.POST.get("form-name")
        if formName == 'userEmailForm':
            userEmailForm = UserEmailForm(request.POST, instance=user)
            if userEmailForm.is_valid():
                userEmailForm.save()
            else:
                showEditView = 'userEmailForm'
        if formName == 'userNameForm':
            userNameForm = UserNameForm(request.POST, instance=user)
            if userNameForm.is_valid():
                userNameForm.save()
            else:
                showEditView = 'userNameForm'
        if formName == 'memberPrivacyForm':
            memberPrivacyForm = MemberPrivacyForm(request.POST, instance=member)
            if memberPrivacyForm.is_valid():
                memberPrivacyForm.save()
            else:
                showEditView = 'memberPrivacyForm'
        if formName == 'memberPhoneForm':
            memberPhoneForm = MemberPhoneForm(request.POST, instance=member)
            if memberPhoneForm.is_valid():
                memberPhoneForm.save()
            else:
                showEditView = 'memberPhoneForm'
        if formName == 'memberDisplayAddressForm':
            memberDisplayAddressForm = MemberDisplayAddressForm(request.POST, instance=member)
            if memberDisplayAddressForm.is_valid():
                memberDisplayAddressForm.save()
            else:
                showEditView = 'memberDisplayAddressForm'
        if formName == 'userPasswordForm':
            userPasswordForm = UserPasswordForm(user, request.POST)
            if userPasswordForm.is_valid():
                user.set_password(userPasswordForm.cleaned_data['new_password'])
                user.save()
            else:
                showEditView = 'userPasswordForm'
        if formName == 'addressForm':
            addressForm = AddressForm(request.POST, instance=member)
            if addressForm.is_valid():
                addressForm.save()
                memberDisplayAddressForm = MemberDisplayAddressForm(instance=member)
            else:
                print 'fail'
                showEditView = 'addressForm'
        if formName == 'deleteAccountForm':
            user.delete()
            return redirect(reverse('login'))
    context = {
        'addressForm' : addressForm,
        'userEmailForm' : userEmailForm,
        'userNameForm' : userNameForm,
        'userPasswordForm' : userPasswordForm,
        'memberPrivacyForm' : memberPrivacyForm,
        'memberPhoneForm' : memberPhoneForm,
        'memberDisplayAddressForm' : memberDisplayAddressForm,
        'showEditView' : showEditView,
        # display values should always show what's currently in the DB
        'userEmailDisplay' : UserEmailForm(instance=user),
        'userNameDisplay' : UserNameForm(instance=user),
        'memberPrivacyDisplay' : MemberPrivacyForm(instance=member),
        'memberPhoneDisplay' : MemberPhoneForm(instance=member),
        'memberDisplayAddressDisplay' : MemberDisplayAddressForm(instance=member),
        'current' : getCurrentUser(request),
    }
    return render(request, 'account/account.html', context)

@transaction.atomic
def create_group(request):
    groupForm = GroupCreateForm
    if request.method == "POST":
        groupForm = GroupCreateForm(request.POST)
        if groupForm.is_valid():
            group = groupForm.save(commit=False)
            user = request.user
            participant = Participant(user=user, type='group')
            participant.save()
            group.participant = participant
            group.owner = Participant.objects.get(type='member', user=user).member
            group.id = participant.id
            group.save()
            messages.success(request, '''
                Your group has been successfully created.
                From this page you can add group info and invite more members.
            ''')
            return redirect('account:edit_group', group.id)
    context = {
        'current' : getCurrentUser(request),  
        'groupForm' : groupForm,
    }
    return render(request, 'account/create_group.html', context)

def edit_group(request, groupId):
    group = Group.objects.get(id=groupId)
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    currentMembers = getRelations(group.participant, currentParticipant, [RelationshipTypes.GROUP_OWNER, RelationshipTypes.GROUP_MEMBER])
    awaitingApproval = getRelations(group.participant, currentParticipant, [RelationshipTypes.GROUP_MEMBER_REQUESTED])
    invited = getRelations(group.participant, currentParticipant, [RelationshipTypes.GROUP_MEMBER_INVITED])
    groupForm = GroupForm(instance=group)
    if request.method == "POST":
        groupForm = GroupForm(request.POST, instance=group)
        if groupForm.is_valid():
            groupForm.save()
            messages.success(request, '''
                Your group info has been updated.
            ''')
    relationshipTypes = [
        RelationshipTypes.FRIENDS,
        RelationshipTypes.REQUEST_RECEIVED,                 
    ]
    ownerFriends = getRelations(currentParticipant, currentParticipant, relationshipTypes)
    for participant in list(ownerFriends):
        if participant in currentMembers or participant in invited:
            ownerFriends.remove(participant)
    context = {
        'current' : getCurrentUser(request),  
        'RelationshipTypes' : RelationshipTypes,
        'group' : group,
        'form' : groupForm,
        'currentMembers' : currentMembers,
        'awaitingApproval' : awaitingApproval,
        'invited' : invited,
        'owner_friends' : ownerFriends
    }
    return render(request, 'account/edit_group.html', context)

def account_info(request):
    if request.method == "POST":
        myform = AccountInfoForm(request.POST)
        if myform.is_valid():
            # save form data to session
            for field in myform.cleaned_data:
                request.session[field] = myform.cleaned_data[field]
            request.session['account_info'] = 'complete'
            destination = ifset(request.POST['redirect-url'], 'account:address')
            return redirect(reverse(destination))
    else:
        myform = AccountInfoForm(initial={
            'email': ifkeyset(request.session, 'email'),
            'first_name': ifkeyset(request.session, 'first_name'),
            'last_name': ifkeyset(request.session, 'last_name'),
        })
    # show page
    context = {
        'user' : request.user,
        'nav'  : build_nav(request, 'account_info'),
        'form' : myform,
        'callback' : reverse('account:account_info')
    }
    return render(request, 'account/account_info.html', context)


def address(request):
    if 'account_info' not in request.session.keys():
        return redirect(reverse('account:account_info'))
    if request.method == "POST":
        myform = AddressForm(request.POST)
        if myform.is_valid():
            # save form data to session
            for field in myform.cleaned_data:
                request.session[field] = str(myform.cleaned_data[field])
            request.session['address'] = 'complete'
            destination = ifset(request.POST['redirect-url'], 'account:personal_info')
            return redirect(reverse(destination))
    else:
        myform = AddressForm()
    context = {
        'user' : request.user,
        'nav'  : build_nav(request, 'address'),
        'form' : myform,
        'callback' : reverse('account:address')
    }
    return render(request, 'account/address.html', context)


@csrf_exempt
def upload_image(request):
    response = {}
    if request.method == "POST" and request.is_ajax():
        if 'image' in request.FILES:
            imagePath = handle_uploaded_file(request.FILES['image'])
            thumbPath = handle_uploaded_file(request.FILES['thumb'])
            if 'member_id' in request.POST:
                member = Member.objects.get(id=request.POST['member_id'])
                member.image = imagePath['file']
                member.thumb = thumbPath['file']
                member.save()
            response = {
                'image' : imagePath,
                'thumb' : thumbPath,
            }
            if 'group_id' in request.POST:
                group = Group.objects.get(id=request.POST['group_id'])
                group.image = imagePath['file']
                group.thumb = thumbPath['file']
                group.save()
            response = {
                'image' : imagePath,
                'thumb' : thumbPath,
            }
        else:
            response['test'] = 'Goodbye cruel world'
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps('Goodbye world'),
            content_type="application/json"
        )


@transaction.atomic
def personal_info(request):
    if 'account_info' not in request.session.keys():
        return redirect(reverse('account:account_info'))
    if 'address' not in request.session.keys():
        return redirect(reverse('account:address'))
    if request.method == "POST":
        #save user
        user = User.objects.create_user(
            ifkeyset(request.session, 'email'), 
            ifkeyset(request.session, 'email'), 
            ifkeyset(request.session, 'password')
        )
        user.first_name = ifkeyset(request.session, 'first_name')
        user.last_name = ifkeyset(request.session, 'last_name')
        user.save()
        #save participant
        participant = Participant(
            user = user, 
            type = 'member',
        )
        participant.save()
        #save member through PersonalInfoForm
        member = Member(
            id = participant.id,
            participant = participant,
            latitude = ifkeyset(request.session, 'latitude'),
            longitude = ifkeyset(request.session, 'longitude'), 
        )
        personalInfoForm = PersonalInfoForm(request.POST, instance=member)
        if personalInfoForm.is_valid():
            # get data from session
            print personalInfoForm
            personalInfoForm.save()
            # add admin as friend
            admins = Member.objects.all().filter(is_admin=True)
            if admins.count() > 0:
                admin = admins[0]
                friendship1 = Friendship(member=member, friend=admin)
                friendship1.save()
                friendship2 = Friendship(member=admin, friend=member)
                friendship2.save()
            # log the user in
            user = authenticate(
                username=ifkeyset(request.session, 'email'),
                password=ifkeyset(request.session, 'password')
            )
            request.session.flush()  #don't flush after login
            # user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Account successfully created for ' + participant.get_name() + '. Welcome!')
            return redirect(reverse('home'))
        else:
            print 'invalid'
    else:
        personalInfoForm = PersonalInfoForm(initial={
            'full_address': ifkeyset(request.session, 'full_address'),
            'street': ifkeyset(request.session, 'street'),
            'city': ifkeyset(request.session, 'city'),
            'neighborhood': ifkeyset(request.session, 'neighborhood'),
            'state': ifkeyset(request.session, 'state'),
            'zip_code': ifkeyset(request.session, 'zip_code'),
        })
    # show page
    accountInfoForm = AccountInfoForm(initial={
            'email': ifkeyset(request.session, 'email'),
            'first_name': ifkeyset(request.session, 'first_name'),
            'last_name': ifkeyset(request.session, 'last_name'),
        })
    context = {
        'user' : request.user,
        'nav'  : build_nav(request, 'personal_info'),
        'form' : personalInfoForm,
        'hiddenForm' : accountInfoForm,
        'callback' : reverse('account:personal_info')
    }
    return render(request, 'account/personal_info.html', context)


def confirmation(request):
    # show page
    context = {
        'user' : request.user,
        'nav'  : build_nav(request, 'confirmation'),
    }
    return render(request, 'account/confirmation.html', context)


    
    
    
    
    
    
    
    
    
    
    
    
