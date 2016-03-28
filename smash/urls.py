"""smash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from tournaments import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.TournamentsView.as_view()),
    url(r'^results/(?P<pk>[0-9]+)/', views.ResultsView.as_view()),
    url(r'^tournaments/(?P<pk>[0-9]+)/', views.MatchesView.as_view()),
    url(r'^tournaments/', views.TournamentsView.as_view()),
    url(r'^profile/(?P<pk>[0-9]+)/', views.ProfileView.as_view()),
    url(r'^leaderboard/', views.LeaderboardView.as_view()),
    url(r'^signup/', views.SignupView.as_view()),
    url(r'^data_entry/', views.DataEntryView.as_view()),
]
