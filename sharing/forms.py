from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['type','title', 'description', 'image', 'thumb']
        
class ShareForm(forms.Form):
    OPTIONS = (
        ('all_friends', 'All Friends'),
        ('all_friends_groups', 'All Friends and All Groups'),
        ('custom', 'Create New Custom List'),
        ('My Share Lists:', (
                ('Share List 1', 'Share List 1'),
                ('Share List 2', 'Share List 2'),
            )
        ),
    )
    sharingWith = forms.ChoiceField(choices=OPTIONS)