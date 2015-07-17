from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

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
        ('person', 'person'),
        ('guest', 'guest'),
        ('group', 'group'),
    )
    user = models.ForeignKey(User)
    participant_type = models.CharField(max_length=6, choices=PARTICIPANT_TYPES)


class Member(models.Model):
    PHONE_TYPE_CHOICES = (
      ("mobile", "mobile"),
      ("home", "home"),
      ("work", "work"),
    )
    member = models.OneToOneField('Participant')
    full_address = models.CharField(max_length=400)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    street = models.CharField(max_length=50, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_type = models.CharField(max_length=20, blank=True, null=True, choices=PHONE_TYPE_CHOICES)
    share_email = models.BooleanField()
    share_address = models.BooleanField()
    share_phone = models.BooleanField()
    user_pic_medium = models.CharField(max_length=100, blank=True, null=True)
    user_pic_small = models.CharField(max_length=100, blank=True, null=True)
    
    def get_user_pic(self):
        if self.user_pic_medium:
            return '/static/uploads/user_pics/' + self.user_pic_medium
        else:
            return '/static/img/generic-user.png'



class Guest(models.Model):
    guest = models.OneToOneField('Participant')
    code = models.CharField(max_length=60)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


    
    
class Group(models.Model):
    group = models.OneToOneField('Member')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)


        
        
class Person(models.Model):
    person = models.OneToOneField('Member')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


        

