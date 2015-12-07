from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *




class ItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # the sharingWith field has to be set dynamically
        participant = kwargs.pop('participant', None)
        shareLists = ShareList.objects.all().filter(owner=participant.member)
        shareListOptions = []
        if shareLists.count() != 0:
            for shareList in shareLists:
                shareListOptions.append([shareList.id, shareList.name])
        shareOptions = [
            ['all_friends', 'All Friends'],
            ['custom', 'Custom'],
        ]
        if len(shareListOptions) != 0:
            shareOptions.append(['Share Lists:', shareListOptions])
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields["sharingWith"] = forms.ChoiceField(choices=shareOptions)
        instance = kwargs.get('instance', None)
        if instance:
            if instance.share_type == 'share_list':
                self.fields["sharingWith"].initial = instance.sharelist.id
            else:
                self.fields["sharingWith"].initial = instance.share_type
    
    class Meta:
        model = Item
        fields = ['type','title', 'description', 'image', 'thumb', 'to_borrow', 'to_keep',]

    # sharingWith = forms.ChoiceField(choices=SHARE_OPTIONS)
    CREATE_SHARE_LIST = (
        ('no', 'No',),
        ('yes', 'Yes',), 
    )
    createShareList = forms.ChoiceField(widget=forms.RadioSelect, choices=CREATE_SHARE_LIST, initial='no')
    shareListName = forms.CharField(max_length=60, label="Share List Name", required=False)

class KeywordForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        setKeywords = kwargs.pop('setKeywords', None)
        super(KeywordForm, self).__init__(*args, **kwargs)
        for itemType in SHARE_CATEGORIES:
            fieldName = 'keywords_' + itemType[0]
            self.fields[fieldName] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=itemType[2], required=False)  
            self.fields[fieldName].initial = setKeywords     

