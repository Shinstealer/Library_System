from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from reviews import views
from django.contrib.auth import views as auth_views #login用のview


urlpatterns = [
    path('book_review/<int:pk>' , views.book_review , name = 'book_review'),
]
