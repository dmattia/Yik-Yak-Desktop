from django.conf.urls import url, include
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='blogList'),
    url(r'^top/$', views.top, name='topYaks'),
    url(r'^myYaks/$', views.myYaks, name='myYaks'),
    url(r'^myTop/$', views.myTopYaks, name='myTopYaks'),
    url(r'R/([0-9a-zA-Z]+)/', views.viewYak, name='yak'),
    url(r'search/([0-9a-zA-Z]+)/', views.search, name='search'),
]
