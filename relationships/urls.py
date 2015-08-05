"""villagebuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'add-friend/', views.add_friend, name='add-friend'),
    url(r'create-guest/', views.create_guest, name='create-guest'),
    url(r'remove-friend/', views.remove_friend, name='remove-friend'),
    url(r'remove-guest-friend/', views.remove_guest_friend, name='remove-guest-friend'),
    url(r'relationships/', views.relationships, name='relationships'),
    url(r'participant_search/', views.participant_search, name='participant_search'),
    url(r'email_search/', views.email_search, name='email_search'),
    
    url(r'^join_group/', views.join_group, name='join_group'),
    url(r'^unjoin_group/', views.unjoin_group, name='unjoin_group'),
    url(r'^add_to_group/', views.add_to_group, name='add_to_group'),
    url(r'^remove_from_group/', views.remove_from_group, name='remove_from_group'),
    url(r'^add_group_members/', views.add_group_members, name='add_group_members'),
]













