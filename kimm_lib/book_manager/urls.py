from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views #login用のview


urlpatterns = [
    path('' , views.Index.as_view() , name = 'index'),
    url(r'^bookinfo_create/$' , views.BookInfoCreateView.as_view() , name='bookinfo_create'),
    url(r'^book_create/(?P<pk>\d+)/$' , views.BookCreateView.as_view() , name='book_create'),
    url(r'^isbn_search/$' , views.isbnSearch , name='isbnsearch'),
    url(r'^book_detail/(?P<pk>\d+)/$', views.BookDetailView.as_view(),name='book_detail'),
    url(r'^bookinfo_update/(?P<pk>\d+)/$', views.BookInfoUpdateView.as_view(),name='bookinfo_update'),
    url(r'^book_update/(?P<pk>\d+)/$', views.BookUpdateView.as_view(),name='book_update'),
    url(r'^bookinfo_list/(?P<mode>\w+)/$' , views.BookInfoListView.as_view() , name='bookinfo_list'),
    url(r'^book_list/(?P<mode>\w+)/$' , views.BookListView.as_view() , name='book_list'),
    url(r'^bookinfo_detail/(?P<pk>[0-9]+)/$' , views.BookInfoDetailView.as_view() , name='bookinfo_detail'),
    url(r'^check_book/(?P<pk>\d+)$' , views.CheckBookView.as_view() , name='check_book'),
    url(r'^complete_book$' , views.CompleteBookView.as_view() , name='complete_book'),
    url(r'^check_bookinfo/(?P<pk>\d+)$' , views.CheckBookInfoView.as_view() , name='check_bookinfo'),
    url(r'^error_bookinfo$' , views.ErrorBookInfoView.as_view() , name='error_bookinfo'),
    url(r'^complete_bookinfo$' , views.CompleteBookInfoView.as_view() , name='complete_bookinfo'),
]
