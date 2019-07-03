from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from operator_manager import views
from django.contrib.auth import views as auth_views #login用のview


urlpatterns = [
    #path('' , views.Index.as_view() , name = 'index'),
    url(r'^check_operator/(?P<pk>\d+)$' , views.CheckOperator.as_view() , name='check_operator'),
    url(r'^complete_operator/' , views.CompleteOperatorView.as_view() , name='complete_operator'),
    url(r'^operator_list/(?P<mode>\w+)/$' , views.OperatorListView.as_view() , name='operator_list'),
    url(r'^operator_list/$' , views.OperatorListView.as_view() , name='operator_list'),
    url(r'^operator_detail/(?P<pk>\d+)$' , views.OperatorDetailView.as_view() , name='operator_detail'),
]
urlpatterns += [
    url(r'^operator_create/$' , views.OperatorCreateView.as_view() , name='operator_create'),
    url(r'^operator_edit/(?P<pk>\d+)/$' , views.OperatorEditView.as_view() , name='operator_edit'),
    
]
