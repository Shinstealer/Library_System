from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from user_page import views
from django.contrib.auth import views as auth_views #login用のview


urlpatterns = [
    path('history/<int:no>' , views.history , name = 'history'),
]

urlpatterns += [
    #path('' , views.Index.as_view() , name = 'index'),
    url(r'^private_info_update/(?P<pk>\d+)/$' , views.UserPrivateInfoUpdateView.as_view() , name='private_info_update'),
    url(r'^user_page_index/$' , views.UserPageIndex.as_view() , name='user_page_index'),
    path('user_my_page', views.user_my_page, name = 'user_my_page'),
    path('my_user_edit', views.my_user_edit, name = 'my_user_edit'),

]
