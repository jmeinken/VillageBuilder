from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RequestResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=120)
    
    def clean(self):
        cleaned_data = super(RequestResetPasswordForm, self).clean()
        email = cleaned_data.get("email")
        users = User.objects.all().filter(username=email)
        if users.count() == 0:
            self.add_error('email', 'That email was not found in our system.')
            
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    resubmit_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
        
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        new_password = cleaned_data.get("new_password")
        resubmit_password = cleaned_data.get("resubmit_password")
        if new_password != resubmit_password:
            self.add_error('resubmit_password', 'Password values didn\'t match.')
            
            
            
            
            
            
            
            