import json
import threading

from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import Http404

from main.helpers import getCurrentUser, handle_uploaded_file, ifset
from relationships.helpers import *
from email_system.helpers import email_new_item
from .forms import *
from .helpers import *

@login_required
@transaction.atomic
def edit_item(request, itemId):
    # verify approval to view item
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    item = Item.objects.get(pk=itemId)
    if item.sharer != currentParticipant.member:
        raise Http404("Item not available")
    if request.method == "POST":
        itemForm = ItemForm(request.POST, instance=item, participant=currentParticipant)
        keywordForm = KeywordForm(request.POST)
        if itemForm.is_valid() and keywordForm.is_valid():
            item = itemForm.save(commit=False)
            sharingWith = itemForm.cleaned_data['sharingWith']
            if sharingWith=='all_friends' or sharingWith=='all_friends_groups' or sharingWith=='custom':
                item.share_type = sharingWith
            else:
                item.share_type = 'share_list'
                item.sharelist_id = sharingWith
            item.save()
            ItemKeyword.objects.all().filter(item=item).delete()
            ItemSharee.objects.all().filter(item=item).delete()
            ItemGroup.objects.all().filter(item=item).delete()
            # save keywords
            keywordFieldName = 'keywords_' + item.type
            keywords = keywordForm.cleaned_data[keywordFieldName]
            for keyword in keywords:
                itemKeyword = ItemKeyword(item=item, keyword=keyword)
                itemKeyword.save()
            # save group sharing selections
            groupIds = request.POST.getlist("groups[]")
            for groupId in groupIds:
                record = ItemGroup(item=item, group_id=groupId)
                record.save()
            # save new custom list as share list
            shareListName = itemForm.cleaned_data['shareListName']
            if sharingWith=='custom':
                if itemForm.cleaned_data['createShareList'] == 'yes' and shareListName != '':
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
                    ItemSharee.objects.all().filter(item=item).delete()
                    for participantId in custom:
                        record = ItemSharee(item=item, sharee_id=int(participantId))
                        record.save()
            messages.success(request,'Your item "' + item.title + '" has been saved')
            return redirect(reverse('sharing:item', args=[itemId]))
    setKeywords = ItemKeyword.objects.all().filter(item=item).values_list('keyword', flat=True)
    itemForm = ItemForm(instance=item, participant=currentParticipant)
    keywordForm = KeywordForm(setKeywords=setKeywords)
    friends = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.FRIENDS,
        RelationshipTypes.GUEST_FRIENDS,                                              
    ])   
    groups = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.GROUP_OWNER,
        RelationshipTypes.GROUP_MEMBER,                         
    ])   
    sharees = item.itemsharee_set.values_list('sharee_id', flat=True)
    shareeGroups = item.itemgroup_set.values_list('group_id', flat=True)
    shareLists = ShareList.objects.all().filter(owner=currentParticipant.member)
    print(sharees)
    print(shareeGroups)
    context = {
        'current' : getCurrentUser(request),
        'item' : item,  
        'friends' : friends,
        'groups' : groups,  
        'itemForm' : itemForm, 
        'keywordForm' : keywordForm, 
        'itemImage' : item.get_image(),
        'sharees' : sharees,
        'shareeGroups' : shareeGroups,
        'shareLists' : shareLists,
    }
    return render(request, 'sharing/share_item.html', context)

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
            if sharingWith=='all_friends' or sharingWith=='custom':
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
            # save group sharing selections
            groupIds = request.POST.getlist("groups[]")
            for groupId in groupIds:
                record = ItemGroup(item=item, group_id=groupId)
                record.save()
            # save new custom list as share list
            shareListName = itemForm.cleaned_data['shareListName']
            if sharingWith=='custom':
                if itemForm.cleaned_data['createShareList'] == 'yes' and shareListName != '':
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
            # messages.success(request,'Your item "' + item.title + '" has been saved')
            context = {
                 'item' : item    
            }
            t = threading.Thread(target=email_new_item, args=(request,item,))
            t.start()
            messages.success(request, render_to_string('sharing/blocks/share_confirm.html', context))
            return redirect(reverse('sharing:item', args=[item.id]))
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
        'itemImage' : '/static/img/generic-item.png',
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
    filters = {
        'category' : request.GET.get('category'),
        'sharer' : request.GET.get('sharer'),
        'group' : request.GET.get('group'),
        'search_terms' : request.GET.get('search_terms'),
        'search_scope' : ifset(request.GET.get('search_scope'), 'title'),
        'has_image' : request.GET.get('has_image'),
    }
    # print(filters['search_scope'])
    category = request.GET.get('category');
    items = getItemsForParticipant(currentParticipant)
    items = filterItems(
        items,
        category = filters['category'],
        sharerId = filters['sharer'],
        groupId = filters['group'],
        searchTerms = filters['search_terms'], 
        searchScope = filters['search_scope'],
        hasImage = filters['has_image'],      
    )
    context = {
        'current' : getCurrentUser(request),
        'items' : items,
        'friends' :  getReciprocatedFriends(currentParticipant),
        'groups' : getReciprocatedGroups(currentParticipant),
        'categories' : SHARE_CATEGORIES,
        'filters' : filters,
    }
    return render(request, 'sharing/items.html', context)

@login_required
def my_items(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    items = getItemsSharedByCurrentMember(currentParticipant.member)
    shareLists = ShareList.objects.all().filter(owner=currentParticipant.member)
    context = {
        'current' : getCurrentUser(request),
        'items' : items,
        'shareLists' : shareLists,
        'shareCategories' : SHARE_CATEGORIES,
    }
    return render(request, 'sharing/my_items.html', context)

@login_required
def item(request, itemId):
    # verify approval to view item
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    items = getItemsForParticipant(currentParticipant)
    myItems = getItemsSharedByCurrentMember(currentParticipant.member)
    item = Item.objects.get(pk=itemId)
    if not item in items and not item in myItems:
        raise Http404("Item not available")
    context = {
         'current' : getCurrentUser(request),
         'item' : item,      
         'sharer' : getParticipantFull(item.sharer.id, currentParticipant),
         'RelationshipTypes' : RelationshipTypes,
         
    }
    return render(request, 'sharing/item.html', context)

def public_item(request, itemCode):
    # if logged in and item is shared with current participant, should forward to 'item'
    if len(itemCode) != 30:
        raise Http404('Item not available')
    item = Item.objects.get(code=itemCode)
    if not item or not item.public:
        raise Http404("Item not found")
    og = {}
    og['no_url'] = True
    og['title'] = item.title
    og['description'] = (item.sharer.participant.get_name('short') +
        ' is sharing this item with you on VillageBuilder, a website that' +
        ' lets you share resources with friends.  Click the link to borrow this'
        ' item from ' + item.sharer.participant.get_name('short') + '.'
    )
    if item.image:
        og['image'] = 'https://villagebuilder.net' + item.get_image()
    context = {
         'item' : item,      
         'sharer' : getParticipant(item.sharer.id),
         'og' : og,
    }
    return render(request, 'sharing/public_item.html', context)

@login_required
@csrf_exempt
def make_item_public(request):
    if request.method == "POST":
        itemId = request.POST.get('item_id')
        item = Item.objects.get(pk=itemId)
        # don't let someone make an item public that doesn't belong to them
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        if not item in getItemsSharedByCurrentMember(currentParticipant.member):
            raise Http404("Item not found")
        if not item.public:
            item.code = createRandomString(30)
            item.public = True
            item.save()
        response = 'https://villagebuilder.net' + reverse('sharing:public_item', args=[item.code])
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
    raise Http404("Item not found")

@login_required
@transaction.atomic
def delete_item(request):
    if request.method == "POST":
        itemId = request.POST.get('item_id')
        item = Item.objects.all().get(pk=itemId)
        itemName = item.title
        item.delete()
        messages.success(request, 'Your item "' + itemName + '" has been removed.')
    return redirect(reverse('sharing:my_items'))
        

@login_required
@transaction.atomic
def delete_sharelist(request):
    if request.method == "POST":
        shareListId = request.POST.get('sharelist_id')
        shareList = ShareList.objects.get(pk=shareListId)
        shareeIds = ShareListSharee.objects.all().filter(shareList=shareList).values_list('sharee_id', flat=True)
        items = Item.objects.all().filter(sharelist=shareList)
        for item in items:
            item.sharelist = None
            item.share_type = 'custom'
            item.save()
            for shareeId in shareeIds:
                itemSharee = ItemSharee(item=item, sharee_id=shareeId)
                itemSharee.save()
        shareList.delete()
        messages.success(request, '''
            The share list has been deleted.
            Any items using that share list have been converted
            to custom-shared items using the same people.
        ''')
    return redirect(reverse('sharing:my_items'))
        

@login_required
@transaction.atomic
def edit_sharelist(request, shareListId):
    shareListId = int(shareListId)
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    shareList = ShareList.objects.get(pk=shareListId)
    if request.method == "POST":
        shareListName = request.POST.get('share_list_name')
        shareListMemberIds = request.POST.getlist('participants[]')
        shareList.name = shareListName
        shareList.save()
        shareListSharees = shareList.sharelistsharee_set.all()
        shareListSharees.delete()
        for memberId in shareListMemberIds:
            shareListSharee = ShareListSharee(shareList=shareList, sharee_id=memberId)
            shareListSharee.save()
        messages.success(request, 'Changes to "' + shareList.name + '" have been saved.')
    friends = getRelations(currentParticipant, currentParticipant, [
        RelationshipTypes.FRIENDS,                                         
    ])      
    shareeIds = shareList.sharelistsharee_set.values_list('sharee_id', flat=True)
    context = {
        'current' : getCurrentUser(request),
        'shareList' : shareList,
        'shareeIds' : shareeIds,
        'friends' :  friends,
    }
    return render(request, 'sharing/edit_sharelist.html', context)

@login_required
@transaction.atomic
def quick_share(request):
    currentParticipant = Participant.objects.get(user=request.user, type='member')
    item_lists = getQuickShareItems()
    active_items = Item.objects.filter(sharer=currentParticipant.member)
    active_item_titles = []
    for active_item in active_items:
        active_item_titles.append(active_item.title)
    if request.method == "POST":
        shared_items = []
        removed_items = []
        for item_list in item_lists:
            for category in item_list:
                for item in item_list[category]:
                    title = item_list[category][item]
                    if request.POST.get(item):
                        if not title in active_item_titles:
                            new_item = Item(
                                sharer = currentParticipant.member,
                                share_type = 'all_friends',
                                type = 'stuff',
                                title = title,
                                description = request.POST.get(item + '_description')                
                            )
                            new_item.save()
                            for keyword in getQuickShareKeywords(category, item):
                                itemKeyword = ItemKeyword(item=new_item, keyword=keyword)
                                itemKeyword.save()
                            shared_items.append(title)
                    else:
                        if title in active_item_titles:
                            existing_items = Item.objects.filter(title=title)
                            for existing_item in existing_items:
                                existing_item.delete()
                            removed_items.append(title)
        message = '<strong>The following new items have been shared:</strong> ' + ', '.join(shared_items)
        if removed_items:
            message = message + '<br><br>  <strong>The following existing items have been removed:</strong> ' + ', '.join(removed_items)
        messages.success( request, message)
    
    active_items = Item.objects.filter(sharer=currentParticipant.member)
    active_item_titles = []
    for active_item in active_items:
        active_item_titles.append(active_item.title)
    context = {
        'current' : getCurrentUser(request),
        'item_lists' : item_lists,
        'active_item_titles' : active_item_titles
    }
    return render(request, 'sharing/quick_share.html', context)

















