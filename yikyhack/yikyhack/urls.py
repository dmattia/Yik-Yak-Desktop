"""yikyhack URL Configuration

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
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.contrib import admin
from blog import views, regbackend

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', regbackend.MyRegistrationView.as_view(), name="register"),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name='home-index'),
    url(r'R/([0-9a-zA-Z]+)/', views.viewYak, name='yak'),
    url(r'^blog/', include('blog.urls')),
]
