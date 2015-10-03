from django.conf.urls import url, include
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='blogList'),
    url(r'^top/', views.top, name='topYaks'),
]
