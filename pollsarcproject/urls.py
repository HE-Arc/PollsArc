"""pollsarcproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, path

from pollsarcapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create_poll_form', views.create_poll_form, name='create_poll_form'),
    path('create_poll', views.create_poll),
    path('poll/<int:id>', views.show_poll, name='poll'),
    path('search_users/<str:name>', views.search_users),
    path('register', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search_polls/<str:name>', views.search_polls),
    path('accounts/<str:username>', views.user_profile, name="profile"),
    path('avatar/', include('avatar.urls')),
    path('add_user_vote', views.add_user_vote, name='add_user_vote'),
]
