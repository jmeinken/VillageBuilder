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
    url(r'^request_list/', views.request_list, name='request_list'),
    url(r'^request/([0-9]*)', views.request, name='request'),
    url(r'^post_request/', views.post_request, name='post_request'),
    url(r'^edit_request/', views.edit_request, name='edit_request'),
    url(r'^delete_request/', views.delete_request, name='delete_request'),
    url(r'^complete_request/', views.complete_request, name='complete_request'),
    url(r'^uncomplete_request/', views.uncomplete_request, name='uncomplete_request'),
    url(r'^post_request_comment/', views.post_request_comment, name='post_request_comment'),
    url(r'^edit_request_comment/', views.edit_request_comment, name='edit_request_comment'),
    url(r'^delete_request_comment/', views.delete_request_comment, name='delete_request_comment'),
]













