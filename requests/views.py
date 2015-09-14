import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string


from account.models import Participant
from main.helpers import getCurrentUser
from .models import *
from requests.helpers import *
from relationships.helpers import *


@login_required
def post_request(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        body = request.POST.get("body")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        myrequest = Request(member=currentParticipant.member, body=body)
        myrequest.save()
        return redirect(url)
    return redirect('login')

@login_required
@csrf_exempt
def edit_request(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        body = request.POST.get("body")
        requestId = request.POST.get("request_id")
        myrequest = Request.objects.get(id=requestId)
        myrequest.body = body
        myrequest.save()
        return redirect(url)
    return redirect('login')

@login_required
@csrf_exempt
def delete_request(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        requestId = request.POST.get("request_id")
        myrequest = Request.objects.get(id=requestId)
        myrequest.delete()
        data=requestId
        return HttpResponse(json.dumps(data), content_type = "application/json")
    
@login_required
@csrf_exempt
def complete_request(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        requestId = request.POST.get("request_id")
        myrequest = Request.objects.get(id=requestId)
        myrequest.complete = True
        myrequest.save()
        context = {
            'current' : getCurrentUser(request),
            'requests' : getSingleRequest(requestId)['requests']
            }
        html = render_to_string('requests/request_list.html', context)
        data = {
            'request_id' : requestId,
            'html' : html,
        }
        return HttpResponse(json.dumps(data), content_type = "application/json")
    
@login_required
@csrf_exempt
def uncomplete_request(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        requestId = request.POST.get("request_id")
        myrequest = Request.objects.get(id=requestId)
        myrequest.complete = False
        myrequest.save()
        context = {
            'current' : getCurrentUser(request),
            'requests' : getSingleRequest(requestId)['requests']
            }
        html = render_to_string('requests/request_list.html', context)
        data = {
            'request_id' : requestId,
            'html' : html,
        }
        return HttpResponse(json.dumps(data), content_type = "application/json")
    
@login_required
@csrf_exempt
def delete_request_comment(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        commentId = request.POST.get("comment_id")
        comment = RequestComment.objects.get(id=commentId)
        comment.delete()
        data=commentId
        return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
@csrf_exempt
def edit_request_comment(request):
    if request.method == "POST":
        body = request.POST.get("body")
        commentId = request.POST.get("comment_id")
        comment = RequestComment.objects.get(id=commentId)
        comment.body = body
        comment.save()
        context = {
            'current' : getCurrentUser(request),
            'comment' : comment,
            }
        html = render_to_string('requests/blocks/commentblock.html', context)
        data = {
            'comment_id' : commentId,
            'html' : html,
        }
        return HttpResponse(json.dumps(data), content_type = "application/json")
    return redirect('login')

@login_required
@csrf_exempt
def post_request_comment(request):
    if request.method == "POST":
        body = request.POST.get("body")
        requestId = request.POST.get("request_id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        comment = RequestComment(member=currentParticipant.member, body=body, request_id=requestId)
        comment.save()
        context = {
            'current' : getCurrentUser(request),
            'comment' : comment,
            }
        html = render_to_string('requests/blocks/commentblock.html', context)
        data = {
            'request_id' : requestId,
            'html' : html,
        }
        return HttpResponse(json.dumps(data), content_type = "application/json")
    return redirect('login')


@login_required
def request_list(request):
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    start = request.GET.get("start")
    end = request.GET.get("end")
    requestList = getRequestList(currentParticipant, start, end)
    requests = requestList['requests']
    totalCount = requestList['total_count']
    if totalCount > int(end):
        moreRequests = True
    else:
        moreRequests = False
    context = {
        'current' : getCurrentUser(request),
        'requests' : requests,
    }
    html = render_to_string('requests/request_list.html', context)
    data = {
        'html' : html,
        'moreRequests' : moreRequests,
        'maxRequest' : end,
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
def request(request, requestId):
    '''Be careful not to overwrite Django 'request' object with something else called request'''
    # check permission to view this request
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    singleRequest = getSingleRequest(requestId)['requests']
    rel = getRelationship(currentParticipant, singleRequest[0]['request'].member.participant)
    if rel != RelationshipTypes.FRIENDS and rel != RelationshipTypes.SELF:
        raise Http404("Page does not exist")
    context = {
        'requests' : singleRequest,
        'current' : getCurrentUser(request),
        'expand_comments' : True,
    }
    return render(request, 'requests/request.html', context)
        
