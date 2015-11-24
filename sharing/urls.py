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
    url(r'^share_item/', views.share_item, name='share_item'),
    url(r'^upload_image/', views.upload_image, name='upload_image'),
    url(r'^items/', views.items, name='items'),
    url(r'^my_items/', views.my_items, name='my_items'),
    url(r'^item/([0-9]*)', views.item, name='item'),
    url(r'^public_item/([a-zA-Z0-9]*)', views.public_item, name='public_item'),
    url(r'^make_item_public/', views.make_item_public, name='make_item_public'),
    url(r'^edit_item/([0-9]*)', views.edit_item, name='edit_item'),
    url(r'^edit_sharelist/([0-9]*)', views.edit_sharelist, name='edit_sharelist'),
    url(r'^delete_sharelist', views.delete_sharelist, name='delete_sharelist'),
    url(r'^delete_item', views.delete_item, name='delete_item'),
    url(r'^quick_share', views.quick_share, name='quick_share'),
]













