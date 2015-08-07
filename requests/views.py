import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from account.models import Participant
from .models import *


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
def delete_request_comment(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        commentId = request.POST.get("comment_id")
        comment = RequestComment.objects.get(id=commentId)
        comment.delete()
        data=commentId
        return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
def edit_request_comment(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        body = request.POST.get("body")
        commentId = request.POST.get("comment_id")
        comment = RequestComment.objects.get(id=commentId)
        comment.body = body
        comment.save()
        return redirect(url)
    return redirect('login')

@login_required
def post_request_comment(request):
    if request.method == "POST":
        url = request.POST.get("redirect")
        body = request.POST.get("body")
        requestId = request.POST.get("request_id")
        currentParticipant = Participant.objects.get(user=request.user, type='member')
        comment = RequestComment(member=currentParticipant.member, body=body, request_id=requestId)
        comment.save()
        return redirect(url)
    return redirect('login')


@login_required
def request_list(request):
    return True
