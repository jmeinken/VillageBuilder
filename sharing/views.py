import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from main.helpers import getCurrentUser, handle_uploaded_file
from relationships.helpers import *
from .forms import *
from .helpers import *

@login_required
@transaction.atomic
def share_item(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    if request.method == "POST":
        itemForm = ItemForm(request.POST, participant=currentParticipant)
        keywordForm = KeywordForm(request.POST)
        if itemForm.is_valid() and keywordForm.is_valid():
            item = itemForm.save(commit=False)
            item.sharer = currentParticipant.member
            sharingWith = itemForm.cleaned_data['sharingWith']
            if sharingWith=='all_friends' or sharingWith=='all_friends_groups' or sharingWith=='custom':
                item.share_type = sharingWith
            else:
                item.share_type = 'share_list'
                item.sharelist_id = sharingWith
            item.save()
            # save keywords
            keywordFieldName = 'keywords_' + item.type
            keywords = keywordForm.cleaned_data[keywordFieldName]
            for keyword in keywords:
                itemKeyword = ItemKeyword(item=item, keyword=keyword)
                itemKeyword.save()
            # save new custom list as share list
            shareListName = itemForm.cleaned_data['shareListName']
            if sharingWith=='custom' and itemForm.cleaned_data['createShareList'] == 'yes' and shareListName != '':
                custom = request.POST.getlist("custom_list[]")
                shareList = ShareList(name=shareListName, owner=currentParticipant.member)
                shareList.save()
                for participantId in custom:
                    record = ShareListSharee(shareList=shareList, sharee_id=int(participantId))
                    record.save()
                item.share_type = 'share_list'
                item.sharelist = shareList
                item.save()
            else:
                custom = request.POST.getlist("custom_list[]")
                for participantId in custom:
                    record = ItemSharee(item=item, sharee_id=int(participantId))
                    record.save()
            messages.success(request,'Your item "' + item.title + '" has been saved')
            return redirect(reverse('sharing:share_item'))
    else:
        itemForm = ItemForm(initial={'type': request.GET.get('type')}, participant=currentParticipant)
        keywordForm = KeywordForm()
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
        'friends' : friends,
        'groups' : groups,
        'keywordForm' : keywordForm,
    }
    return render(request, 'sharing/share_item.html', context)

@login_required
@csrf_exempt
def upload_image(request):
    response = {}
    if request.method == "POST" and request.is_ajax():
        if 'image' in request.FILES:
            imagePath = handle_uploaded_file(request.FILES['image'], 'item_pics')
            thumbPath = handle_uploaded_file(request.FILES['thumb'], 'item_pics')
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

@login_required
def items(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')

    context = {
        'current' : getCurrentUser(request),
        'items' : getItemsForParticipant(currentParticipant),   
        'friends' :  getReciprocatedFriends(currentParticipant),
        'groups' : getReciprocatedGroups(currentParticipant),
        'categories' : SHARE_CATEGORIES,
    }
    return render(request, 'sharing/items.html', context)
