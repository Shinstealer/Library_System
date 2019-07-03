from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from book_rental import views
from django.contrib.auth import views as auth_views #login用のview


urlpatterns = [
    path('rental/<int:pk>' , views.rental , name = 'rental'),
    path('book_return/<int:pk>' , views.book_return , name = 'book_return'),
    path('return_check/<int:pk>' , views.return_check , name = 'return_check'),
    path('wish_book/<int:pk>' , views.wish_book , name = 'wish_book'),
    path('wish_cancel/<int:pk>' , views.wish_cancel , name = 'wish_cancel'),
    path('overdue', views.overdue, name = 'overdue'),
    url(r'^user_index/$' , views.UserIndex.as_view() , name='user_index'),
    url(r'^user_bookinfo_list/(?P<mode>\w+)/$' , views.BookInfoListView.as_view() , name='user_bookinfo_list'),
    url(r'^user_bookinfo_detail/(?P<pk>\d+)/$', views.BookInfoDetailView.as_view(),name='book_rental_bookinfo_detail'),
]
