from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages

from main.helpers import getCurrentUser
from relationships.helpers import *
from .forms import *

@login_required
@transaction.atomic
def share_item(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    if request.method == "POST":
        itemForm = ItemForm(request.POST)
        shareForm = ShareForm(request.POST)
        if itemForm.is_valid():
            item = itemForm.save(commit=False)
            item.sharer = currentParticipant.member
            sharingWith = request.POST.get('sharingWith')
            if sharingWith=='all_friends' or sharingWith=='all_friends_groups' or sharingWith=='custom':
                item.share_type = sharingWith
            else:
                item.share_type = 'share_list'
            item.save()
            messages.success(request,'Your item has been saved')
            return redirect(reverse('sharing:share_item'))
    else:
        itemForm = ItemForm(initial={'type': request.GET.get('type')})
        shareForm = ShareForm()
    friends = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.FRIENDS,
        RelationshipTypes.GUEST_FRIENDS,                                              
    ])   
    groups = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.GROUP_OWNER,
        RelationshipTypes.GROUP_MEMBER,                         
    ])     
    context = {
        'current' : getCurrentUser(request),
        'itemForm' : itemForm,
        'shareForm' : shareForm,
        'friends' : friends,
        'groups' : groups,
    }
    return render(request, 'sharing/share_item.html', context)
