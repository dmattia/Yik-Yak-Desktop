from django.conf.urls import patterns, include, url

urlpatterns = [
	url(r'^profile/$', 'userprofile.views.user_profile'),
]
