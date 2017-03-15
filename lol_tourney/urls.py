"""lol_tourney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse

from webapp import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$', views.home, name="index"),
    url(r'^tournaments/$', views.new_tournament_view, name="new_tournament"),
    url(r'^profile/$', views.user_profile_view, name="user_profile"),
    url(r'^remove/(?P<tournament_id>[0-9]+)/', views.remove_from_tournament, name='remove_user'),
    url(r'bootstrap/',views.bootstrap_index, name='bootstrap_index'),
    url(r'tournaments/(?P<tournament_id>[0-9]+)/', views.tournament_detail_view, name="tournament_detail"),
    url(r'riot.txt', lambda r:HttpResponse('50d23f43-950d-4a55-ac72-c14325ec166f', content_type='text/plain')),
]
