from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from user_page.forms.private_update_form import PrivateUpdateForm
from user_manager.models.user import User
from operator_manager.models.operator import Operator
from book_rental.models.rental import Rental
from book_manager.forms import BookInfoForm , BookForm , SearchForm ,SearchForm2


from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check


import datetime

def user_my_page(request):
    #一般ユーザーチェック
    c = usercheck(request)
    if c is not None:
        return c
    #idの取得
    id = request.session['id']
    user = User.objects.get(id=id, is_active=True)

    params = {'user':user }

    return render(request, 'user_page/user_my_page.html', params)





def my_user_edit(request):
    #一般ユーザーチェック
    c = usercheck(request)
    if c is not None:
        return c
    #idの取得
    id = request.session['id']
    #userの取得
    user = User.objects.get(id=id)

    if request.method == 'GET':
        form = PrivateUpdateForm(instance=user)
        params = {
        'form':form
        }
        return render(request, 'user_page/my_user_edit.html', params)

    if request.method == 'POST':
        password = request.POST['password']
        password_check= request.POST['password_check']
        if password == password_check:
            form = PrivateUpdateForm(request.POST, instance=user)
            form.save()
            user = User.objects.get(id=id, is_active=True)

            params = {'user':user, 'word': '編集に成功しました' }

            return render(request, 'user_page/user_my_page.html', params)
        else:
            form = PrivateUpdateForm(instance=user)
            params = {
            'form':form,
            'word':'※PasswordとPassword checkが異なります'
            }
            return render(request, 'user_page/my_user_edit.html', params)
