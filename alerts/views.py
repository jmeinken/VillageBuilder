import json
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from account.models import Participant
from .helpers import *




@login_required
@csrf_exempt
def alerts(request):
    user = request.user
    currentParticipant = Participant.objects.get(user=user, type='member')
    if request.method == "POST":
        action = request.POST.get("action")
        if action == 'reset_count':
            time.sleep(10)
            resetAlertCount(currentParticipant)
        if action == 'delete_alert':
            deleteAlert(request.POST.get("alert_id"))
    alerts = getAlerts(currentParticipant)
    context = {
            'alerts' : alerts['alerts'],
            'alertCount' : alerts['count'],
        }
    html = render_to_string('alerts/alerts.html', context)
    data = {
        'html' : html,
        'count' : alerts['count']
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")
