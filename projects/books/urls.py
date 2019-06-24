from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LoginView , LogoutView
from django.contrib.auth import views as auth_views
from .views import * 
from .forms import LoginForm

app_name ='books'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    url(r'^signup/$', signup, name='signup'),
    
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    ]
