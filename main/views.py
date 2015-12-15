#-----------------------------------------------------------------
# all this crap is from django.contrib.auth.views
# much of it is needed to make login view work
import warnings

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

#-----------------------------------------------------------------



from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.mail import send_mail
from django.db import transaction

from account.helpers import *
from main.helpers import *
from relationships.helpers import *
from alerts.helpers import *
from requests.helpers import *
from email_system.helpers import *
from sharing.models import SHARE_CATEGORIES
from sharing.helpers import *
from account.forms import AccountInfoForm

from .forms import RequestResetPasswordForm, ResetPasswordForm

def custom_404(request):
    context = {}
    return render(request, 'core/404.html', context)

def custom_500(request):
    context = {}
    return render(request, 'core/500.html', context)

def custom_403(request):
    context = {}
    return render(request, 'core/403.html', context)

def facebook_test(request):
    context = {}
    return render(request, 'core/facebook_test.html', context)

def facebook_login_test(request):
    context = {}
    return render(request, 'core/facebook_login_test.html', context)

@login_required
def home(request):
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    requestList = getRequestList(currentParticipant, 0, 10)
    totalCount = requestList['total_count']
    if totalCount > 10:
        moreRequests = True
    else:
        moreRequests = False
    items = getItemsForParticipant(currentParticipant)
    recentItems = items[:5]
    shareCategories = getCategoriesWithCounts(items)
    # print(shareCategories)
    totalSharedWithYou = 0
    # print(shareCategories)
    for category in shareCategories:
        totalSharedWithYou = totalSharedWithYou + category[3]
    # does this person have any friends? (also need to exclude admin)
    relationships = getRelations(currentParticipant, currentParticipant, relationshipTypes=[
        RelationshipTypes.FRIENDS,
        RelationshipTypes.REQUEST_SENT, 
        RelationshipTypes.GROUP_MEMBER,
        RelationshipTypes.GROUP_MEMBER_REQUESTED,                                                                              
    ])
    relationshipCount = len(relationships)
    hasRelationshipActivity = doesUserHaveRelationshipActivity(currentParticipant)
    if Item.objects.filter(sharer=currentParticipant.member).count() == 0:
        hasSharedSomething = False
    else:
        hasSharedSomething = True
    context = {
            'current' : getCurrentUser(request),
            'peopleNearYou' : getPeopleNearYou(currentParticipant),
            'friendsOfFriends' : getFriendsOfFriends(currentParticipant),
            'RelationshipTypes' : RelationshipTypes,
            'requests' : requestList['requests'],
            'moreRequests' : moreRequests,
            'maxRequest' : 10,
            'shareCategories' : shareCategories,
            'totalSharedWithYou' : totalSharedWithYou,
            'recentItems' : recentItems,
            'hasRelationshipActivity' : hasRelationshipActivity,
            'hasSharedSomething' : hasSharedSomething,
            'actions' : getSharingActions(currentParticipant.member)
        }
    return render(request, 'core/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def info(request):
    context = {}
    return render(request, 'core/boilerplate.html', context)

def test_view(request):
    return HttpResponse("It worked!")

@csrf_protect
@transaction.atomic
def reset_password(request, code):
    successMessage = ''
    errorMessage = ''
    members = Member.objects.all().filter(code=code)
    if members.count() != 1 or not code:
        return redirect('login')
    member = members[0]
    user = member.participant.user
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            member.code = ''
            member.save()
            successMessage = 'Password Changed.  You can now <a href="' + reverse('login') + '">login</a>.'
    else:
        form = ResetPasswordForm()
    context = {
        'code' : code,
        'successMessage' : successMessage,
        'errorMessage' : errorMessage,
        'form' : form,
        'member' : member,
    }
    return render(request, 'core/reset_password.html', context)

@csrf_protect
def request_reset_password(request):
    successMessage = ''
    errorMessage = ''
    if request.method == "POST":
        form = RequestResetPasswordForm(request.POST)
        if form.is_valid():
            # get user
            user = User.objects.get(username=form.cleaned_data['email'])
            member = Participant.objects.get(user=user, type='member').member
            member.code = createRandomString(60)
            member.save()
            result = email_forgot_password(request, member)
            if result:
                successMessage = 'An email has been sent to you.  Please check your junk mail folder if it doesn\'t arrive.'
            else:
                errorMessage = ('There was an error with our email system.  If the problem ' +
                    'persists, contact <a href="mailto:admin@villagebuilder.net">the VillageBuilder administrator</a>.')
    else:
        form = RequestResetPasswordForm()
    context = {
        'form' : form,
        'successMessage' : successMessage,
        'errorMessage' : errorMessage,
    }
    return render(request, 'core/request_reset_password.html', context)

def hide_me(request):
    '''This will put a cookie on your browser that hides you from google analytics for 2 years.'''
    return render(request, 'core/hide_me.html', {})

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_view(request, template_name='core/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    This was copied and modified from django.contrib.auth.views.py.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)
    
    createAccountForm = AccountInfoForm(initial={
            'email': ifkeyset(request.session, 'email'),
            'first_name': ifkeyset(request.session, 'first_name'),
            'last_name': ifkeyset(request.session, 'last_name'),
        })

    context = {
        'form': form,
        'createAccountForm' : createAccountForm,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


