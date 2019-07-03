from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from accounts import views
from django.contrib.auth import views as auth_views #login用のview


urlpatterns = [
    url(r'^login/$' , views.LoginView.as_view() , name='login'),
    url(r'^logout/$' , views.logout , name='logout'),
]
