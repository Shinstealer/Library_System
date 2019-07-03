"""kimm_lib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path , include
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book_manager/', include('book_manager.urls')),
    path('operator_manager/', include('operator_manager.urls')),
    path('accounts/', include('accounts.urls')),
    path('user_manager/',include('user_manager.urls')),
    path('book_rental/', include('book_rental.urls')),
    path('user_page/',include('user_page.urls')),
    path('reviews/',include('reviews.urls')),
]
