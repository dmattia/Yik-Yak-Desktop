from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # blog views
    url(r'^$', views.index, name='home-index'),
    url(r'R/([0-9a-zA-Z]+)/', views.viewYak, name='yak'),
    url(r'^blog/', include('blog.urls')),
    # user auth views
    url(r'^accounts/login/$', 'yikyhack.views.login'),
    url(r'^accounts/auth/$', 'yikyhack.views.auth_view'),
    url(r'^accounts/logout/$', 'yikyhack.views.logout'),
    url(r'^accounts/loggedin/$', 'yikyhack.views.loggedin'),
    url(r'^accounts/invalid/$', 'yikyhack.views.invalid_login'),
    # user registration
    url(r'^accounts/register/$', 'yikyhack.views.register_user'),
    url(r'^accounts/register_success/$', 'yikyhack.views.register_success'),
]
