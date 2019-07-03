from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from user_manager import views
from django.contrib.auth import views as auth_views #login用のview

urlpatterns = [
    #path('' , views.Index.as_view() , name = 'index'),
    url(r'^user_create/$' , views.UserCreateView.as_view() , name='user_create'),
    url(r'^user_edit/(?P<pk>\d+)/$' , views.UserEditView.as_view() , name='user_edit'),
    url(r'^check_user/(?P<pk>\d+)/$' , views.CheckUserView.as_view() , name='check_user'),
    url(r'^complete_user/$' , views.CompleteUserView.as_view() , name='cpmplete_user'),
    url(r'^error_user/$' , views.ErrorUserView.as_view() , name='error_user'),
    url(r'^user_list/(?P<mode>\w+)/$' , views.UserListView.as_view() , name='user_list'),
    url(r'^user_detail/(?P<pk>\d+)/$', views.UserDetailView.as_view() , name='user_detail'),

]
