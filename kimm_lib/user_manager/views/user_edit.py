from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

from user_manager.forms.user_form import User_Form
from user_manager.models.user import User


from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from django import forms

class UserEditView(UpdateView):
    template_name ='user_manager/user_create.html'
    model = User
    form_class = User_Form
    success_url=reverse_lazy('user_list', kwargs={'mode': 'all'})

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        password_check= form.cleaned_data.get('password_check')
        if password == password_check:
            result = super().form_valid(form)
            messages.success(
                self.request, 'ユーザ編集成功です')
            return result
        else:
            result = super().form_invalid(form)
            messages.warning(
                self.request,'パスワードチェックしてください！'
                )
            return result

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['is_active'].widget = forms.HiddenInput()
        context['form'].fields['leave_date'].widget = forms.HiddenInput()
        return context
