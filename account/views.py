import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction

from villagebuilder.utils import console
from .forms import AccountInfoForm, AddressForm, PersonalInfoForm
from .models import Member, Participant, Person
from .helpers import build_nav, handle_uploaded_file, ifkeyset


def account_info(request):
    print 'test'
    if request.method == "POST":
        myform = AccountInfoForm(request.POST)
        if myform.is_valid():
            # save form data to session
            for field in myform.cleaned_data:
                request.session[field] = myform.cleaned_data[field]
            request.session['account_info'] = 'complete'
            return redirect(reverse('account:address'))
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
    return render(request, 'account_info.html', context)


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
            return redirect(reverse('account:personal_info'))
    else:
        myform = AddressForm()
    context = {
        'user' : request.user,
        'nav'  : build_nav(request, 'address'),
        'form' : myform,
        'callback' : reverse('account:address')
    }
    return render(request, 'address.html', context)

@csrf_exempt
def upload_image(request):
    response = {}
    if request.method == "POST" and request.is_ajax():
        if 'medium' in request.FILES:
            path = handle_uploaded_file(request.FILES['medium'])
            response = path
        else:
            response['test'] = 'Goodbly world'
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
            participant_type = 'person',
        )
        participant.save()
        #save member through PersonalInfoForm
        member = Member(
            member = participant,
            latitude = ifkeyset(request.session, 'latitude'),
            longitude = ifkeyset(request.session, 'longitude'), 
        )
        personalInfoForm = PersonalInfoForm(request.POST, instance=member)
        if personalInfoForm.is_valid():
            # get data from session
            print personalInfoForm
            personalInfoForm.save()
            #save person
            person = Person(
                person = member,
                first_name = ifkeyset(request.session, 'first_name'),
                last_name = ifkeyset(request.session, 'last_name')
            )
            person.save()
            print 'validated'
            #save user to database
            return redirect(reverse('account:confirmation'))
        else:
            print 'invalid'
    else:
        personalInfoForm = PersonalInfoForm(initial={
            'full_address': ifkeyset(request.session, 'full_address'),
            'street': ifkeyset(request.session, 'street'),
            'city': ifkeyset(request.session, 'city'),
            'neighborhood': ifkeyset(request.session, 'neighborhood'),
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
    return render(request, 'personal_info.html', context)

def confirmation(request):
    return HttpResponse("It worked!")
