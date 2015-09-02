from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from relationships.helpers import *
from account.models import Member, Participant

from .models import Message

class NewMessageForm(forms.ModelForm):
    # field1 = forms.ModelChoiceField(queryset=, empty_label="(Nothing)")
    
    def __init__(self, *args, **kwargs):
        participant = kwargs.pop('participant', None)
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = getUnreciprocatedFriendsAndGuests(participant)
    
    class Meta:
        model = Message
        fields = ['recipient', 'body']
        labels = {
            'body': 'Message',
        }
        
