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
from django.contrib import admin


urlpatterns = [
    #direct links to views
    url(r'login/', 'main.views.login_view', name='login'),
    url(r'logout/', 'main.views.logout_view', name='logout'),
    url(r'request_reset_password/', 'main.views.request_reset_password', name='request_reset_password'),
    url(r'reset_password/([a-zA-Z0-9]*)', 'main.views.reset_password', name='reset_password'),
    
    #note: pages in main do not have a namespace 
    url(r'^$', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace="account")),
    url(r'^relationships/', include('relationships.urls', namespace="relationships")),
    url(r'^alerts/', include('alerts.urls', namespace="alerts")),
    url(r'^requests/', include('requests.urls', namespace="requests")),
    url(r'^pm/', include('pm.urls', namespace="pm")),
    url(r'^sharing/', include('sharing.urls', namespace="sharing")),
]










