from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from relationships.helpers import getReciprocatedFriendsAndGuests, RelationshipTypes
from account.models import Member, Participant

from .models import Message

class NewMessageForm(forms.ModelForm):
    # field1 = forms.ModelChoiceField(queryset=, empty_label="(Nothing)")
    
    def __init__(self, currentParticipant, *args, **kwargs):
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = getReciprocatedFriendsAndGuests(currentParticipant)
    
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        
class NewConversationMessageForm(forms.ModelForm):
    # field1 = forms.ModelChoiceField(queryset=, empty_label="(Nothing)")
    
    #def __init__(self, recipient, *args, **kwargs):
    #    super(NewConversationMessageForm, self).__init__(*args, **kwargs)
        #self.fields['recipient'].initial = recipient
        
    def __init__(self, participantId, *args, **kwargs):
        super(NewConversationMessageForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Participant.objects.all().filter(id=participantId)
        self.fields['recipient'].empty_label = None
    
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        