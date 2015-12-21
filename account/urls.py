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
    url(r'account_info/', views.account_info, name='account_info'),
    url(r'address/', views.address, name='address'),
    url(r'personal_info/', views.personal_info, name='personal_info'),
    url(r'confirmation/', views.confirmation, name='confirmation'),
    
    #url(r'new_facebook_account/', views.new_facebook_account, name='new_facebook_account'),
    
    url(r'create_group/', views.create_group, name='create_group'),
    url(r'edit_group/([0-9]*)', views.edit_group, name='edit_group'),
    url(r'delete_group/', views.delete_group, name='delete_group'),
    
    url(r'account/', views.account, name='account'),
    
    url(r'upload_image/', views.upload_image, name='upload_image'),
    url(r'view/([0-9]*)', views.view, name='view'),
    
]













