from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Member, Group

class AccountInfoForm(forms.ModelForm):
    resubmit_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    facebook_id = forms.CharField(max_length=128, widget=forms.TextInput)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'resubmit_password']
        widgets = {
            'password': forms.PasswordInput,
        }
    
    # using default User model, so extra validation must be performed in the form 
    def clean(self):
        cleaned_data = super(AccountInfoForm, self).clean()
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        password = cleaned_data.get("password")
        resubmit_password = cleaned_data.get("resubmit_password")
        if password and len(password) < 8:
            self.add_error('password', 'Password must be at least 8 characters.')
        if password != resubmit_password:
            self.add_error('resubmit_password', 'Password values didn\'t match.')
        if email == '':
            self.add_error('email', 'This field is required.')
        if first_name == '':
            self.add_error('first_name', 'This field is required.')
        if last_name == '':
            self.add_error('last_name', 'This field is required.')
        if User.objects.all().filter(email=email).count() != 0:
            self.add_error('email', 'An account already exists with this email.')

class FacebookAccountInfoForm(forms.ModelForm):
    facebook_id = forms.CharField(max_length=128, widget=forms.TextInput)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        



class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'description',]

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'description', 'neighborhood', 'city', 
                  'email', 'website', 'image', 'thumb']



class AddressForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_address', 'street', 'city', 'neighborhood', 'state', 'zip_code', 'latitude', 'longitude']
        
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_address', 'street', 'city', 'neighborhood', 'state', 'zip_code',
                  'share_email',
                  'share_street', 'image', 'thumb',]
        labels = {
            'full_address' : 'Location (not public)',
            'share_street': 'Allow people to see my street name',
            'share_email': 'Allow friends to see my email address',
        }
        
class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        
    def clean(self):
        cleaned_data = super(UserEmailForm, self).clean()
        email = cleaned_data.get("email")
        if email == '':
            self.add_error('email', 'This field is required.')
        
class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',]
        
    def clean(self):
        cleaned_data = super(UserNameForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name == '':
            self.add_error('first_name', 'This field is required.')
        if last_name == '':
            self.add_error('last_name', 'This field is required.')
        
class UserPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    resubmit_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(UserPasswordForm, self).clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        resubmit_password = cleaned_data.get("resubmit_password")
        if not self.user.check_password(old_password):
            self.add_error('old_password', 'Old password was incorrect.')
        if new_password and len(new_password) < 8:
            self.add_error('new_password', 'Password must be at least 8 characters.')
        if new_password != resubmit_password:
            self.add_error('resubmit_password', 'Password values didn\'t match.')
        
class MemberPrivacyForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['share_street', 'share_email']
        labels = {
            'share_street': 'Allow people to see my street name',
            'share_email': 'Allow friends to see my email address',
        }
        
class MemberEmailForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['email_friend_requests', 'email_pm', 'email_requests', 'email_request_comments', 'email_shared_items', ]
        labels = {
            'email_friend_requests': 'You receive a friend request',
            'email_pm': 'You receive a private message',
            'email_requests': 'Your friend posts a new request', 
            'email_request_comments': 'New comment on a request you\'re watching', 
            'email_shared_items': 'New item shared with you',
        }
        widgets = {
            'email_friend_requests': forms.RadioSelect,
            'email_pm': forms.RadioSelect,
            'email_requests': forms.RadioSelect,
            'email_request_comments': forms.RadioSelect,
            'email_shared_items': forms.RadioSelect,
        }
        


class MemberDisplayAddressForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['street', 'neighborhood', 'city', ]
        help_texts = {
            'neighborhood': 'leave blank to use city',
        }
        
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    resubmit_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        new_password = cleaned_data.get("new_password")
        resubmit_password = cleaned_data.get("resubmit_password")
        if new_password and len(new_password) < 8:
            self.add_error('new_password', 'Password must be at least 8 characters.')
        if new_password != resubmit_password:
            self.add_error('resubmit_password', 'Password values didn\'t match.')



        
