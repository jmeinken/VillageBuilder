from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Member

class AccountInfoForm(forms.ModelForm):
    resubmit_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
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
        if password != resubmit_password:
            self.add_error('resubmit_password', 'Password values didn\'t match.')
        if email == '':
            self.add_error('email', 'This field is required.')
        if first_name == '':
            self.add_error('first_name', 'This field is required.')
        if last_name == '':
            self.add_error('last_name', 'This field is required.')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_address', 'street', 'city', 'neighborhood', 'latitude', 'longitude']
        
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_address', 'street', 'city', 'neighborhood', 'share_email', 'share_address', 'share_phone',
                  'phone_number', 'phone_type', 'user_pic_medium']
        labels = {
            'share_email': 'Allow friends to see my email address',
            'share_address': 'Allow friends to see my full mailing address',
            'share_phone': 'Allow friends to see my phone number',
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
        if new_password != resubmit_password:
            self.add_error('resubmit_password', 'Password values didn\'t match.')
        
class MemberPrivacyForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['share_email', 'share_address', 'share_phone',]
        labels = {
            'share_email': 'Allow friends to see my email address',
            'share_address': 'Allow friends to see my full mailing address',
            'share_phone': 'Allow friends to see my phone number',
        }
        
class MemberPhoneForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone_number', 'phone_type',]

class MemberDisplayAddressForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['street', 'city', 'neighborhood']



        
