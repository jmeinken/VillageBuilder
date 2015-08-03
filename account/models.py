from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings


# User Model:
# username *
# first_name
# last_name
# email
# password *
# groups
# user_permissions
# is_staff
# is_active
# is_superuser
# last_login (auto)
# date_joined (auto)
# ---
# get_username()
# is_authenticated()
# get_full_name()
# get_short_name()
# set_password(pw)
# check_password(pw)
# email_user(subject, message, from_email)



class Participant(models.Model):
    PARTICIPANT_TYPES = (
        ('member', 'member'),
        ('guest', 'guest'),
        ('group', 'group'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=PARTICIPANT_TYPES)
    
    def get_name(self, length='full'):
        if self.type == 'group':
            return self.group.title
        else:
            if length=='full':
                return self.user.get_full_name()
            else:
                return self.user.get_short_name()
            
    def get_email(self):
        if self.type == 'group' and self.group.email:
            return self.group.email
        else:
            return self.user.email
        
    def get_image(self):
        if self.type == 'member' and self.member.image:
            return '/static/uploads/user_pics/' + self.member.image
        if self.type == 'group' and self.group.image:
            return '/static/uploads/user_pics/' + self.group.image
        return '/static/img/generic-user.png'
        
    def get_thumb(self):
        if self.type == 'member' and self.member.thumb:
            return '/static/uploads/user_pics/' + self.member.thumb
        if self.type == 'group' and self.group.thumb:
            return '/static/uploads/user_pics/' + self.group.thumb
        else:
            return '/static/img/generic-user.png'
        
    def get_display_address(self):
        if self.type == 'guest':
            return '(guest account)'
        if self.type == 'group':
            if self.group.neighborhood:
                return self.group.neighborhood
            if self.group.city:
                return self.group.city
            return self.group.owner.city
        if self.type == 'member':
            if self.member.neighborhood:
                return self.member.street + ' (' + self.member.neighborhood + ')'
            else:
                return self.member.street + ' (' + self.member.city + ')'

    def get_phone(self):
        if self.type == 'guest':
            return ''
        if self.type == 'group':
            if self.group.phone_number:
                if self.group.phone_type:
                    return self.group.phone_number + ' (' + self.group.phone_type + ')'
                else:
                    return self.group.phone_number
        if self.type == 'member':
            if self.member.phone_number:
                if self.member.phone_type:
                    return self.member.phone_number + ' (' + self.member.phone_type + ')'
                else:
                    return self.member.phone_number
        else:
            return ''
        
    def get_public(self):
        result = {
            'id' : self.id,
            'type' : self.type,
            'name' : self.get_name(),
            'display_address' : self.get_display_address(),
            'image' : self.get_image(),
            'thumb' : self.get_thumb(),
        }
        if self.type == 'group':
            result['owner'] = self.group.owner.participant.get_public()
        return result
    
    def get_private(self, currentUser):
        result = self.get_public()
        result['email'] = ''
        result['phone'] = ''
        return result
        


# need non-auto pk field so that it can be set to the same value as participant
class Member(models.Model):
    PHONE_TYPE_CHOICES = (
      ("mobile", "mobile"),
      ("home", "home"),
      ("work", "work"),
    )
    id = models.IntegerField(primary_key=True)
    participant = models.OneToOneField('Participant', on_delete=models.CASCADE)
    full_address = models.CharField(max_length=600)
    # address1 = models.CharField(max_length=50, blank=True, null=True)
    # address2 = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=60)
    neighborhood = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=60)
    # state = models.CharField(max_length=2, blank=True, null=True)
    # zip_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_type = models.CharField(max_length=20, blank=True, null=True, choices=PHONE_TYPE_CHOICES)
    share_email = models.BooleanField()
    share_phone = models.BooleanField()
    image = models.CharField(max_length=30, blank=True, null=True)
    thumb = models.CharField(max_length=30, blank=True, null=True)
    
    def get_user_pic(self):
        if self.image:
            return '/static/uploads/user_pics/' + self.image
        else:
            return '/static/img/generic-user.png'
    
    def get_display_address(self):
        if self.neighborhood:
            return self.street + ' (' + self.neighborhood + ')'
        else:
            return self.street + ' (' + self.city + ')'
        
    def get_phone(self):
        if self.phone_number:
            if self.phone_type:
                return self.phone_number + ' (' + self.phone_type + ')'
            else:
                return self.phone_number
        else:
            return ''

class Guest(models.Model):
    id = models.IntegerField(primary_key=True)
    participant = models.OneToOneField('Participant', on_delete=models.CASCADE)
    code = models.CharField(max_length=60)
    created_by = models.ForeignKey('Member')
    
    def get_user_pic(self):
        return '/static/img/generic-user.png'


    
    
class Group(models.Model):
    PHONE_TYPE_CHOICES = (
      ("mobile", "mobile"),
      ("home", "home"),
      ("work", "work"),
    )
    id = models.IntegerField(primary_key=True)
    participant = models.OneToOneField('Participant', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    neighborhood = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_type = models.CharField(max_length=20, blank=True, null=True, choices=PHONE_TYPE_CHOICES)
    email = models.CharField(max_length=120, blank=True, null=True)
    website = models.CharField(max_length=240, blank=True, null=True)
    image = models.CharField(max_length=30, blank=True, null=True)
    thumb = models.CharField(max_length=30, blank=True, null=True)
    owner = models.ForeignKey('Member', on_delete=models.CASCADE)


        
        



        

